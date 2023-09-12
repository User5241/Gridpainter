import time

class Timer(object):
    """docstring for Timer"""
    def __init__(self):
        super(Timer, self).__init__()
        self.start = None
        self.stop = None

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, *args, **kwargs):
        print(f" done in: {time.perf_counter() - self.start}")
