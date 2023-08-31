import logging
from queue import Empty

from utils.server import QManager, MultiM

"""
Note that on Windows child processes will only inherit the level of the parent process’s logger –
any other customization of the logger will not be inherited.

This is related to the lack of fork() on Windows.
Multiprocessing on Windows is implemented by launching a
new process and executing the whole Python file once again to
retrieve global variables (like your worker function).
This is called "spawning".
"""


class MultiProcessingHandler(logging.Handler):
    def __init__(self, name, sub_handler):
        super().__init__()

        if sub_handler is None:
            sub_handler = logging.StreamHandler()
        self.sub_handler = sub_handler

        self.setLevel(self.sub_handler.level)
        self.setFormatter(self.sub_handler.formatter)
        self.filters = self.sub_handler.filters

        self._is_closed = False
        MultiM.add_t(name, self.receive)

        # The thread handles receiving records asynchronously.
        # self._receive_thread = threading.Thread(target=self._receive, name=name)
        # self._receive_thread.daemon = True
        # self._receive_thread.start()

    def setFormatter(self, fmt):
        super().setFormatter(fmt)
        self.sub_handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                if self._is_closed and QManager.log_empty():
                    break

                record = QManager.log_q.get(timeout=0.2)
                self.sub_handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except (EOFError, OSError):
                break  # The queue was closed by child?
            except Empty:
                pass  # This periodically checks if the logger is closed.
            except:
                from sys import stderr
                from traceback import print_exc

                print_exc(file=stderr)
                raise

        # QManager.log_q.close()
        # QManager.log_q.join_thread()

    def _send(self, s):
        QManager.log(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified. Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe.
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self._send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        if not self._is_closed:
            self._is_closed = True
            # self._receive_thread.join(5.0)  # Waits for receive queue to empty.

            self.sub_handler.close()
            super().close()
