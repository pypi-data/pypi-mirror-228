from multiprocessing import Queue
from queue import Empty
from threading import Event
from typing import Any

from utils.log import logger
from .ctx import Context


class _QManager:
    def __init__(self):
        super().__init__()
        self.in_q: Queue
        self.out_q: Queue
        self.signal_q: Queue
        self.log_q: Queue
        self._qs = ("in_q", "out_q", "signal_q", "log_q")

        self._log_q_stop = Event()
        self.start_log()

    def init_log_q(self, q: Queue):
        self.log_q = q

    def init_task_q(self, input: Queue, output: Queue):
        self.in_q = input
        self.out_q = output

    def init_signal_q(self, q: Queue):
        self.signal_q = q

    def close(self):
        for q in self._qs:
            if not hasattr(self, q):
                continue
            o = getattr(self, q)
            o.close()
            o.join_thread()

    def empty_task(self):
        self.in_q = Queue()
        self.out_q = Queue()

    def add_task(self, item, timeout=30 * 60):
        self.in_q.put((item, Context(timeout)))

    def get_task(self) -> type[Any, Context]:
        try:
            item, ctx = self.in_q.get()
        except Empty:
            logger.error("QManager get_task q empty")
            return None, None
        return item, ctx

    def get_a_task(self) -> type[Any, Context]:
        item, ctx = self.in_q.get_nowait()
        return item, ctx

    def log(self, s):
        self._log_q_stop.wait()
        self.log_q.put_nowait(s)

    # 原来是为了暂停写日志，目前不需要
    def pause_log(self):
        self._log_q_stop.clear()

    def start_log(self):
        self._log_q_stop.set()

    def log_empty(self) -> bool:
        return self.log_q.empty()

    @property
    def task_num(self) -> int:
        return self.in_q.qsize()

    def __del__(self):
        self.close()


QManager = _QManager()
