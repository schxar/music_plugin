import random
from typing import Optional
from bilibili_api import video, user, Credential
import os
import json
import asyncio

# 可选：如需登录凭证支持，自动读取本地 credential 文件
_CREDENTIAL_CONFIG_PATH = "config/bilibili_credential.json"

def _get_credential() -> Optional[Credential]:
    try:
        if os.path.exists(_CREDENTIAL_CONFIG_PATH):
            with open(_CREDENTIAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                return Credential(**config)
    except Exception:
        pass
    return None

async def get_random_video_url(uid: int) -> Optional[str]:
    """
    随机获取指定B站UP主的一个视频链接。
    :param uid: B站UP主uid
    :return: 视频url字符串，失败返回None
    """
    credential = _get_credential()
    try:
        u = user.User(uid=uid, credential=credential if credential else None)
        videos = await u.get_videos()
        if not videos or 'list' not in videos or not videos['list']['vlist']:
            return None
        video_list = videos['list']['vlist']
        selected_video = random.choice(video_list)
        bvid = selected_video['bvid']
        return f"https://www.bilibili.com/video/{bvid}"
    except Exception:
        return None

