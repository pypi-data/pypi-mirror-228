from typing import Callable

from utils.data import decode_gzip, get_ints_in_str, decode_bytes
from utils.errno import Error, OK, TIMEOUT
from utils.file import (
    get_path_last_part,
    get_file_path,
    dump_b_f, dump_f,
    check_file_exist,
    filename_in_dir,
)
from utils.log import logger
from utils.media.m3u8 import M3U8, Segment, load
from utils.time import TimeRecord
from .web import _Web
from .req import download_file


class _WebM3u8ByUrl(_Web):
    def get_m3u8_url(self, m3u8_filter: Callable = None) -> str:
        if m3u8_filter:
            for req in self.driver.requests:
                if not req.response:
                    continue
                if m3u8_filter(req.url):
                    return req.url

        # 一般页面只会有一个<video>
        element = self.find_element("//video")
        if not element:
            logger.error(f"get_m3u8 no element")
            return ""
        return element.get_dom_attribute("data-src")

    def save_m3u8(self, u: str, filepath: str):
        download_file(u, filepath)


class _WebM3u8ByReq(_Web):
    def __init__(self):
        super().__init__()

    def save_m3u8(self, filepath, req, m3u8_filter) -> M3U8:
        req_u = req.url
        res_body = req.response.body
        if not m3u8_filter(req_u):
            return None
        m3u8 = decode_gzip(res_body)
        m3u8, ok = decode_bytes(m3u8)
        if not ok:
            return None
        m3u8_f_path = get_file_path(filepath, get_path_last_part(req_u))
        logger.info(f"save m3u8 {m3u8_f_path}")
        dump_f(m3u8_f_path, m3u8)
        return load(m3u8_f_path)

    def save_ts(self, filepath, req, ts_filter) -> str:
        req_u = req.url
        res_body = req.response.body
        if not ts_filter(req_u):
            return None
        f_name = get_path_last_part(req_u)
        f_path = get_file_path(filepath, f_name)
        if check_file_exist(f_path):
            logger.info(f"save_ts {f_path} exist, will not re save")
        else:
            logger.info(f"save_ts {f_path}")
            dump_b_f(f_path, decode_gzip(res_body))
        return f_name

    def _next_miss_ts(self, exist_ts, m3u8: M3U8) -> tuple[Segment, bool]:
        """
        miss ts信息，是否miss
        """
        if not exist_ts:
            return None, True
        if not m3u8:
            return None, True

        for item in m3u8.segments:
            if item.uri in exist_ts:
                continue
            return item, True
        return None, False

    def _forward(self, curr_ts_name: str, miss_ts: Segment, forward_xpath: str,
                 forward_tr: TimeRecord, forward_step_sec=10):
        """
        视频前进
        """
        # if not forward_tr.gap_up_to(60):
        #     # logger.info(f"forward interval not enough {get_now_stamp() - last_forward_stamp}")
        #     return
        if curr_ts_name is None or not miss_ts:
            # logger.info(f"forward no {curr_ts_name} {miss_ts}")
            return

        ts_duration = miss_ts.duration
        miss_ts_name = miss_ts.uri
        sec = (get_ints_in_str(miss_ts_name)[0] - get_ints_in_str(curr_ts_name)[0]) * ts_duration
        sec = int(sec)
        # logger.info(f"forward compute {miss_ts_name} {curr_ts_name} {sec}")
        # 最少间隔多少分钟，才去快进
        if sec <= 2 * 60:
            return

        forward_tr.record()
        # 留出1分钟，做超时buffer
        num = (sec - 1 * 60) / forward_step_sec
        num = int(num)
        logger.info(f"forward {miss_ts_name} {curr_ts_name} {sec} {num}")
        for i in range(num):
            if not self.click(forward_xpath, timeout=3).ok:
                self.press_keyboard(1)
        return

    def download_ts(self, filepath: str, m3u8_filter: Callable, ts_filter: Callable, forward_xpath: str) -> Error:
        logger.info(f"download {get_path_last_part(filepath)}")
        exist_ts_names = {item for item in filename_in_dir(filepath) if ts_filter(item)}

        # logger.info(f"exist no={exist_ts_names}")
        visited_u = set()
        download_tr = TimeRecord()
        forward_tr = TimeRecord()
        curr_ts_name: str = None
        m3u8: M3U8 = None
        while True:
            if download_tr.gap_up_to(10 * 60):
                return TIMEOUT
            miss_ts, miss = self._next_miss_ts(exist_ts_names, m3u8)
            if not miss:
                logger.info(f"{filepath} all done")
                break

            exist_num = 0
            self._forward(curr_ts_name, miss_ts, forward_xpath, forward_tr)

            for req in self.driver.requests:
                if exist_num >= 10 and m3u8 is not None:
                    logger.info(f"{exist_num} >= 10, break")
                    break
                if req.response and req.url not in visited_u:
                    visited_u.add(req.url)
                    # 保存m3u8文件
                    _m3u8 = self.save_m3u8(filepath, req, m3u8_filter)
                    if _m3u8 is not None:
                        m3u8 = _m3u8
                        download_tr.record()
                        continue

                    # 保存ts文件
                    ts_name = self.save_ts(filepath, req, ts_filter)
                    if ts_name is not None:
                        if ts_name in exist_ts_names:
                            exist_num += 1
                        else:
                            exist_ts_names.add(ts_name)
                        download_tr.record()
                        curr_ts_name = self._max_ts_name(curr_ts_name, ts_name, m3u8)
        return OK

    def _max_ts_name(self, curr: str, new: str, m3u8: M3U8) -> str:
        if m3u8 is None:
            return curr
        files = m3u8.files
        if new not in files:
            return curr
        if curr not in files:
            return new
        return files[max(files.index(curr), files.index(new))]
