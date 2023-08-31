import os
from typing import TextIO

import yaml

from utils.errno import Error, OK, MISS_CONFIG, BROKEN_CONFIG
from utils.log import logger

# 全局配置，不要直接使用。
_GLOBAL_CONFIG: dict
_ConfigPath: str


def get_global_config() -> dict:
    name = "_GLOBAL_CONFIG"
    if name not in locals() and name not in globals():
        return {}
    return _GLOBAL_CONFIG


def get_config_path() -> str:
    return _ConfigPath


def init_conf(config_path: str) -> Error:
    """
    初始化全局配置，建议传入绝对路径
    :param config_path:
    :return:
    """
    global _ConfigPath
    _ConfigPath = config_path
    if not os.path.exists(config_path):
        return MISS_CONFIG
    with open(config_path, "r", encoding="utf-8") as f:
        _, err = _init_conf(f)
    return err


def _init_conf(f: TextIO) -> (str, Error):
    try:
        err = OK
        data = yaml.safe_load(f)
        global _GLOBAL_CONFIG
        _GLOBAL_CONFIG = data
    except yaml.YAMLError:
        logger.error(f"_init_conf get broken yaml")
        data = ""
        err = BROKEN_CONFIG
    return data, err


def _parse(config_path: str) -> (str, Error):
    if not os.path.exists(config_path):
        return "", MISS_CONFIG
    with open(config_path, "r", encoding="utf-8") as f:
        return _init_conf(f)


def get_conf(key: str) -> dict:
    """
    获取配置文件中的一级项，不要直接使用。用model.config中的方法
    :param key:
    :return:
    """
    item = get_global_config().get(key, {})
    if not item:
        logger.error(f"get_conf no {key}, check your config, or will use default config")
    return item


def log_conf() -> list[dict]:
    """
    获取日志配置
    :return:
    """
    return _GLOBAL_CONFIG.get("log", [])


def user_service_name() -> str:
    return "user"


def registry_address() -> tuple[str, str]:
    return "", ""


def set_default(value, obj, field, default):
    if not value:
        setattr(obj, field, default)
    else:
        logger.info(f"{obj.__class__.__name__} {field} use default {default}")
        setattr(obj, field, value)


def get_default(config: dict, name: str, default):
    value = config.get(name)
    if not value:
        logger.info(f"no {name} use default {default}")
        return default
    else:
        return value
