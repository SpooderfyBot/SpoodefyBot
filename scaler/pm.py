import time
import logging
import typing as t
import threading
import multiprocessing as mp

from datetime import datetime


def get_chunk(cluster_no: int, shard_count: int):
    return tuple(range(shard_count * cluster_no, (shard_count * cluster_no) + shard_count))


logger = logging.getLogger("bot-scale")


class Worker:
    def __init__(self, caller: t.Callable, *args, **kwargs):
        self._caller = caller
        self._shutdown_queue = mp.Queue(maxsize=1)
        self._process: t.Optional[mp.Process] = None

        self._args = args

        kwargs['shutdown'] = self._shutdown_queue
        self._kwargs = kwargs

        self._cb: t.Optional[t.Callable] = None
        self.__watcher_thread: t.Optional[threading.Thread] = None
        self.__terminate_watcher = False
        self.__exec_limit = 0

    @property
    def cluster(self):
        return self._kwargs.get("cluster_no")

    def set_complete_callback(self, fn: t.Callable):
        self._cb = fn

    def __watch(self):
        if self._process is None:
            raise TypeError("Process is None when expecting a running process")

        try:
            while self._process.is_alive() and not self.__terminate_watcher:
                time.sleep(1)
        except ValueError:  # process died and we rechecked
            pass

        if self._cb is not None and not self.__terminate_watcher:
            self.__exec_limit += 1
            if self.__exec_limit >= 3:
                raise RuntimeError("Child raised exception to many times")
            self._cb(self)

    def wait(self):
        running = True
        while running:
            try:
                running = self._process.is_alive()
                if self.__terminate_watcher:
                    return
            except ValueError:  # process died and we rechecked
                pass
            time.sleep(1)

    def start(self):
        self._process = mp.Process(
            target=self._caller,
            args=self._args,
            kwargs=self._kwargs,
        )
        self._process.start()
        time.sleep(1)
        self.__watcher_thread = threading.Thread(target=self.__watch)
        self.__watcher_thread.start()

    def shutdown(self):
        self._shutdown_queue.put(None, block=True)
        self.__terminate_watcher = True

        if self._process is not None and self._process.is_alive():
            try:
                self._process.join(timeout=60)
                self._process.close()
            except mp.TimeoutError:
                self._process.kill()

        if self.__watcher_thread is not None and self.__watcher_thread.is_alive():
            self.__watcher_thread.join()

    def restart(self, new_caller: t.Callable):
        self.shutdown()
        self._caller = new_caller
        self.start()


class BotScaler:
    def __init__(
            self,
            get_bot: t.Callable,
            bot_token: str,
            num_workers: int = 1,
            num_shards: int = 1,
            **bot_kwargs,
    ):
        self._token = bot_token
        self.num_workers = num_workers
        self.num_shards = num_shards
        self.total_shards = self.num_workers * self.num_workers

        self._loader = get_bot
        self._temp_cb = self._loader(restart=False)

        self._bot_kwargs = bot_kwargs
        self._exception_count = 0
        self._check_workers = True
        self._workers: t.Dict[int, Worker] = {}

    def start(self):
        for cluster in range(self.num_workers):
            shards = get_chunk(cluster, self.num_shards)

            self.start_worker(cluster=cluster, shards=shards)

            time.sleep(5)

    def start_worker(self, cluster, shards):
        now = datetime.now()
        print(
            f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
            f" Starting cluster: {cluster}"
        )

        worker = Worker(
            self._temp_cb,
            token=self._token,
            shards=shards,
            total_shards=self.total_shards,
            cluster_no=cluster,
            **self._bot_kwargs
        )
        worker.set_complete_callback(self.on_worker_end)
        worker.start()

        self._workers[cluster] = worker

    def on_worker_end(self, worker: Worker):
        now = datetime.now()
        print(
            f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
            f" Cluster completed: {worker.cluster}")

        if not self._check_workers:
            return

        now = datetime.now()
        print(
            f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
            f" Restarting cluster: {worker.cluster}"
        )

        worker.start()

    def shutdown(self):
        for worker in self._workers.values():
            worker.shutdown()
            now = datetime.now()
            print(
                f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
                f" Terminated cluster: {worker.cluster}"
            )

    def restart(self):
        self._temp_cb = self._loader(restart=True)
        self.shutdown()
        self.start()

    def rolling_restart(self, *, delay=2):
        self._temp_cb = self._loader(restart=True)
        for cluster, worker in self._workers.items():
            now = datetime.now()
            print(
                f"[ {now.strftime('%H:%M:%S | %d %b')} ][ WORKER ]"
                f" Restarting cluster: {worker.cluster}"
            )
            worker.restart(self._temp_cb)
            time.sleep(delay)

    def wait_until_finished(self):
        for worker in self._workers.values():
            worker.wait()
