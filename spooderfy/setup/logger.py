from datetime import datetime


class Logger:
    CLUSTER_ID = 0

    @classmethod
    def set_cluster(cls, number: int):
        cls.CLUSTER_ID = number

    @classmethod
    def log(cls, *args):
        now = datetime.now()
        print(f"[ {now.strftime('%H:%M:%S | %d %b')} ][ CLUSTER {cls.CLUSTER_ID:2d}  ]", *args)
