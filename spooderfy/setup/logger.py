from datetime import datetime


class Logger:
    CLUSTER_ID = -1

    @classmethod
    def set_cluster(cls, number: int):
        cls.CLUSTER_ID = number

    @classmethod
    def log(cls, *args):
        now = datetime.now()
        if cls.CLUSTER_ID == -1:
            print(f"[ {now.strftime('%H:%M:%S | %d %b')} ][ RUNTIME SETUP ]", *args)
        else:
            print(f"[ {now.strftime('%H:%M:%S | %d %b')} ][ CLUSTER {cls.CLUSTER_ID:2d}  ]", *args)
