import os
import traceback

import ffmpeg as _ffmpeg
from utils.errno import Error, OK, TRANS_MP4, DOWNLOAD
from utils.file import get_path_last_part, get_file_path


def extract_pcm(file_path: str, out: str):
    r = os.system(f"ffmpeg -hide_banner -i {file_path} -f s16le -acodec pcm_s16le -ac 1 -ar 16000 {out}")
    return r


def download_m3u8_with(u: str, filepath: str, refer) -> Error:
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    cmd = (f'ffmpeg -hide_banner -i {u}'
           f' -user_agent "{user_agent}"'
           f' -headers "Referer: {refer}"'
           f' -headers "Accept: */*"'
           f' -headers "Accept-Encoding: gzip, deflate, br"'
           f' -headers "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"'
           f' -headers "Cache-Control: no-cache"'
           f' -headers "Origin: {refer}"'
           f' -headers "Pragma: no-cache"'
           f''' -headers 'Sec-Ch-Ua: "Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"' '''
           f' -headers "Sec-Ch-Ua-Mobile: ?0"'
           f' -headers "Sec-Ch-Ua-Platform: "Linux""'
           f' -headers "Sec-Fetch-Dest: empty"'
           f' -headers "Sec-Fetch-Mode: cors"'
           f' -headers "Sec-Fetch-Site: cross-site"'
           # f' -headers "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"'
           # f' -headers '
           # f' -headers '
           # f' -headers '
           f' {filepath}'
           )
    print(cmd)
    r = os.system(cmd)
    print(r)
    return OK


def download_m3u8(u: str, filepath: str) -> Error:
    try:
        r = _ffmpeg.input(u) \
            .output(filepath, loglevel="quiet") \
            .overwrite_output() \
            .run(capture_stdout=True, capture_stderr=True)
    except _ffmpeg.Error as e:
        print("=====ffmpeg Error")
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
    else:
        if _check_ffmpeg_res(r):
            return OK
    return DOWNLOAD


def merge_local_m3u8(_dir, m3u8_name="index.m3u8", filename=None):
    if not filename:
        filename = get_path_last_part(_dir)
    filename = f"{filename}.mp4"
    cmd = f"ffmpeg " \
          f"-hide_banner -loglevel error " \
          f"-allowed_extensions ALL " \
          f"-i {get_file_path(_dir, m3u8_name)} " \
          f"-c copy {get_file_path(_dir, filename)}"
    r = os.system(cmd)
    print(r)
    return OK


def _check_ffmpeg_res(res) -> bool:
    return len(res) == 2 and res[0] is None and res[1] is None


def trans_to_mp4(_input: str, output: str) -> Error:
    try:
        r = _ffmpeg \
            .input(_input) \
            .output(output, loglevel="quiet") \
            .overwrite_output(capture_stdout=True, capture_stderr=True) \
            .run()
    except _ffmpeg.Error as e:
        print("=====ffmpeg Error")
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
    else:
        if _check_ffmpeg_res(r):
            return OK
    return TRANS_MP4
