import os
import socket
import platform
import threading


def is_win() -> bool:
    """
    是否运行在windows下
    :return:
    """
    return platform.system().lower() == 'windows'


def is_linux() -> bool:
    """
    是否运行在linux下
    :return:
    """
    return platform.system().lower() == 'linux'


def fix_win_focus():
    """
    防止鼠标误触导致阻塞，但也会导致不响应ctrl+c
    :return:
    """
    print(f"patch windows console")
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


def cur_pid() -> int:
    return os.getpid()


def cur_tid() -> int:
    return threading.currentThread().ident


def get_host_ip() -> str:
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
