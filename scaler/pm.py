import time
import typing as t
import logging
import traceback

from functools import partial
from concurrent.futures import ProcessPoolExecutor, Future


def get_chunk(cluster_no: int, shard_count: int):
    return tuple(range(shard_count * cluster_no, (shard_count * cluster_no) + shard_count))


logger = logging.getLogger("bot-scale")


class BotScaler:
    def __init__(
            self,
            get_bot: t.Callable,
            num_workers: int = 1,
            num_shards: int = 1,
            **bot_kwargs,
    ):
        self.num_workers = num_workers
        self.num_shards = num_shards
        self.total_shards = self.num_workers * self.num_workers

        self._loader = get_bot
        self._bot_kwargs = bot_kwargs
        self._workers: t.Dict[int, t.Tuple[Future, tuple]] = {}
        self._pool: t.Optional[ProcessPoolExecutor] = None
        self._exception_count = 0

    def start(self, bot_token: str):
        self._pool = ProcessPoolExecutor(max_workers=self.num_workers)

        for cluster_no in range(self.num_workers):
            shards = get_chunk(cluster_no, self.num_shards)

            caller = partial(
                self._loader(),
                token=bot_token,
                shards=shards,
                total_shards=self.total_shards,
                cluster_no=cluster_no,
                **self._bot_kwargs
            )

            fut = self._pool.submit(caller)
            self._workers[cluster_no] = (fut, shards)
        self.watch_workers(bot_token=bot_token)

    def watch_workers(self, bot_token: str):
        while True:
            for i, cluster_no in enumerate(self._workers):
                fut, shards = self._workers[cluster_no]

                if fut.running():
                    continue

                try:
                    res = fut.result()
                    logger.info(f"Cluster {cluster_no}:\n  Finished with result: {res}")
                except Exception as e:
                    logger.critical(f"Exception in worker: {e}")
                    traceback.print_exc()
                    self._exception_count += 1

                    if self._exception_count >= 3:
                        raise e

                caller = partial(
                    self._loader(),
                    token=bot_token,
                    shards=shards,
                    total_shards=self.total_shards,
                    **self._bot_kwargs
                )

                fut = self._pool.submit(caller)
                self._workers[cluster_no] = (fut, shards)
            time.sleep(3)
