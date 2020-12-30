from datetime import datetime


class Logger:
    CLUSTER_ID = -1

    @classmethod
    def log(cls, *args, runtime=False):
        now = datetime.now()
        if runtime and cls.CLUSTER_ID == -1:
            print(f"[ {now.strftime('%H:%M:%S | %d %b')} ][ RUNTIME SETUP ]", *args)
        elif not runtime:
            print(f"[ {now.strftime('%H:%M:%S | %d %b')} ][ CLUSTER {cls.CLUSTER_ID:2d}  ]", *args)
