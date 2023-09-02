from pathlib import Path
from multilogging import multilogger
from typing import List

import json
import re

version = "2.2.3"
current_dir = Path(__file__).resolve().parent
uvdiviner_dir = Path.home() / ".uvdiviner"
data_dir = uvdiviner_dir / "data"
_divination_cachepath = data_dir / "divination.json"
logger = multilogger(name="Dicer Girl", payload="utils")

def init():
    if not uvdiviner_dir.exists():
        logger.info("UVDiviner 文件夹未建立, 建立它.")
        uvdiviner_dir.mkdir()
    if not data_dir.exists():
        logger.info("UVDiviner 数据文件夹未建立, 建立它.")
        data_dir.mkdir()
    if not _divination_cachepath.exists():
        logger.info("UVDiviner 数据存储文件未建立, 建立它.")
        with open(_divination_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")

def format_msg(message, begin=None, zh_en=False) -> List[str]:
    """ 骰娘指令拆析为`list`的方法 """
    msg = format_str(message, begin=begin).split(" ")
    outer = []
    regex = r'(\d+)|([a-zA-Z\u4e00-\u9fa5]+)' if not zh_en else r"(\d+)|([a-zA-Z]+)|([\u4e00-\u9fa5]+)"

    for m in msg:
        m = re.split(regex, m)
        m = list(filter(None, m))
        outer += m

    msg = outer
    msg = list(filter(None, msg))
    logger.debug(msg)
    return msg

def format_str(message: str, begin=None) -> str:
    """ 骰娘指令转义及解析 """
    regex = r"[<\[](.*?)[\]>]"
    msg = re.sub("\s+", " ", re.sub(regex, "", str(message).lower())).strip(" ")
    logger.debug(msg)

    if begin:
        if isinstance(begin, str):
            begin = [begin, ]
        elif isinstance(begin, tuple):
            begin = list(begin)

        begin.sort(reverse=True)
        for b in begin:
            msg = msg.replace(b, "").lstrip(" ")

    logger.debug(msg)
    return msg

def get_group_id(event):
    try:
        return str(event.group_id)
    except Exception as error:
        logger.exception(error)
        logger.warning(f"超出预计的错误, 将 Group ID 设置为 0.")
        return "0"

def get_user_id(event):
    try:
        return str(event.get_user_id())
    except Exception as error:
        logger.exception(error)
        logger.warning(f"超出预计的错误, 将 User ID 设置为 0.")
        return "0"

def load_limit() -> dict:
    data = open(_divination_cachepath, "r").read()
    if data:
        return json.loads(data)
    else:
        return {}

def minus_limit(event):
    datas = load_limit()
    datas[get_group_id(event)][get_user_id(event)]["limit"] -= 1
    file = open(_divination_cachepath, "w")
    json.dump(datas, file)

def reset_limit():
    datas: dict = json.loads(open(_divination_cachepath, "r").read())
    for group, users in datas.items():
        for user in users.keys():
            datas[group][user]["limit"] = 2

def get_limit(event):
    return load_limit()[get_group_id(event)][get_user_id(event)]["limit"]

def has_user(event):
    datas = load_limit()
    if not has_group(event):
        return False
    
    if not hasattr(datas, get_user_id(event)):
        return False
    
    return True

def has_group(event):
    datas = load_limit()
    if not hasattr(datas, get_group_id(event)):
        return False
    
    return True

def get_users():
    users = []
    for group in load_limit():
        users += [user for user in group.keys()]

    return users

def get_groups():
    groups = load_limit().keys()
    if len(groups) == 1:
        if groups[0] == "0":
            return False
    
    return groups

def set_user(event):
    datas = load_limit()
    if not has_group(event):
        datas[get_group_id(event)] = {}
    
    datas[get_group_id(event)][get_user_id(event)] = {
        "limit": 2
    }

    file = open(_divination_cachepath, "w")
    json.dump(datas, file)