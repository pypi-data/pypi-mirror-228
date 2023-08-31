import asyncio
import os
import signal
import traceback
from functools import wraps
from multiprocessing import Process
from threading import Thread

from utils.system import is_linux


class Task:
    def __init__(self, handle, name, *args, **kwargs):
        self.handle = handle
        self.args = args
        self.name = name
        self.kwargs = kwargs
        self.init = kwargs.get("init", None)
        self.end = kwargs.get("end", None)


class _MultiM:
    def __init__(self):
        self._p: dict[str, Task] = {}
        self._rp: dict[int, tuple[Task, Process]] = {}
        self._t: dict[str, Task] = {}
        self._rt: dict[int, tuple[Task, Thread]] = {}
        self._killer: GracefulKiller = None

    def add_p(self, name, handler, *args, **kwargs):
        if name in self._p:
            # logger.info(f"MultiM add_p {name} exist")
            return
        self._p[name] = Task(handler, name, *args, **kwargs)

    def add_t(self, name, handler, *args, **kwargs):
        if name in self._t:
            # logger.info(f"MultiM add_t {name} exist")
            return
        self._t[name] = Task(handler, name, *args, **kwargs)

    @property
    def close(self):
        return self._killer and self._killer.kill_now

    def _decorator(self, func, init, end):
        @wraps(func)
        def _fn(*args, **kwargs):
            GracefulKiller(exit_now=True)
            result = None
            if init:
                init()

            try:
                result = func(*args, **kwargs)
            except ErrGracefulKiller:
                print(f"{os.getpid()} grace exit")
            except Exception:
                print(f"{traceback.format_exc()}")

            if end:
                end()
            return result

        return _fn

    def _new_p(self, task) -> Process:
        if is_linux():
            f = self._decorator(task.handle, task.init, task.end)
        else:
            f = task.handle
        p = Process(
            target=f,
            kwargs=task.kwargs,
            args=task.args
        )
        p.start()
        return p

    def _new_t(self, task) -> Thread:
        # 不能使用信号
        # if is_linux():
        #     f = self._decorator(task.handle, task.init, task.end)
        # else:
        f = task.handle
        t = Thread(
            target=f,
            name=task.name,
            kwargs=task.kwargs,
            args=task.args,
        )
        t.daemon = True
        t.start()
        return t

    def start(self):
        print(f"start processes in {os.getpid()}")
        self._killer = GracefulKiller(exit_now=True, handle_child_exit=self.restart_child)
        for task in self._p.values():
            p = self._new_p(task)
            self._rp[p.pid] = (task, p)
            print(f"process {task.name} started {p.pid}")

        for task in self._t.values():
            t = self._new_t(task)
            self._rt[t.ident] = (task, t)
            print(f"thread {task.name} started")

        # 这行给控制台看
        print("server start success")

        try:
            asyncio.new_event_loop().run_forever()
        except ErrGracefulKiller:
            print(f"will join child")

        # for tid, task_t in self._rt.items():
        #     _, t = task_t
        #     print(f"join thread")
        #     t.join()

        for pid, task_p in self._rp.items():
            print(f"{pid} joining")
            _, p = task_p
            p.join(3)
            if p.is_alive():
                p.terminate()
            print(f"{pid} joined")

    @staticmethod
    def get_exit_child_pid():
        cpid, _ = os.waitpid(-1, os.WNOHANG)
        return cpid

    def _restart_child_by_pid(self, pid):
        task_p = self._rp.get(pid)
        if not task_p:
            print(f"restart child no {pid}")
            return
        task, p = task_p
        p.terminate()
        p = self._new_p(task)
        self._rp[pid] = (task, p)

    def restart_child(self, sig, frame):
        try:
            if self.close:
                return
            cpid = self.get_exit_child_pid()
            if cpid == 0:
                print(f"no child process was immediately available")
                return
            print(f"child process-{cpid} exceptionally exit")
            self._restart_child_by_pid(cpid)
        except ChildProcessError:
            print(f"child fail")


MultiM = _MultiM()


class ErrGracefulKiller(Exception):
    pass


class GracefulKiller:
    kill_now = False

    def __init__(self, exit_now=True, handle_child_exit=None):
        if not exit_now:
            handler = self._exit_gracefully
        else:
            handler = self._exit_now
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)
        if is_linux() and handle_child_exit:
            signal.signal(signal.SIGCHLD, handle_child_exit)

    def _exit_now(self, sig, frame):
        self._exit_gracefully(sig, frame)
        raise ErrGracefulKiller(f'Received signal {sig} on line {frame.f_lineno} in {frame.f_code.co_filename}')

    def _exit_gracefully(self, sig, frame):
        self.kill_now = True
