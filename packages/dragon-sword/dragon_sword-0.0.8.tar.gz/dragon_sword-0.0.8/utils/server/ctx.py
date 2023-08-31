from utils.time import get_now_stamp_float, get_stamp_after


class Context:
    def __init__(self, timeout, start=get_now_stamp_float()):
        self._start = start
        self._deadline = get_stamp_after(self._start, second=timeout)
        self.timeout = timeout

    def timeoutd(self, now=get_now_stamp_float()) -> bool:
        return now >= self._deadline
