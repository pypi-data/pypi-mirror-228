from multiprocessing import Queue
from utils.errno import Error, OK
from .q import QManager


def init_before_server(conf_path: str, in_put: Queue, output: Queue, signal: Queue, log: Queue) -> Error:
    from utils.config import init_conf
    err = init_conf(conf_path)
    if not err.ok:
        return err

    # TODO: remove signal q
    QManager.init_task_q(in_put, output)
    QManager.init_signal_q(signal)
    QManager.init_log_q(log)

    # 初始化日志
    from utils.log import log
    from utils.config import log_conf
    log.init(log_conf())
    return OK
