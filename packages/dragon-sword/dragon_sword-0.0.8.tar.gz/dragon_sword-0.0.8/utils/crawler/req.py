import requests
from fake_useragent import UserAgent
from utils.file import dump_b_f, load_f_line


def download_file(u: str, filepath: str) -> list[str]:
    res = requests.get(u, headers={
        "User-Agent": UserAgent.chrome,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    })
    dump_b_f(filepath, res.content)
    lines, _ = load_f_line(filepath)
    return lines
