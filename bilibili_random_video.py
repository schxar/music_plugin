import random
from typing import Optional
from bilibili_api import user

FIXED_UID = 488978908  # 固定UP主UID

async def get_random_video_url() -> Optional[str]:
    """
    获取固定UP主的随机视频链接。
    返回: 视频链接字符串，若无视频则返回None。
    """
    u = user.User(uid=FIXED_UID)
    videos = await u.get_videos()
    if not videos or 'list' not in videos or not videos['list']['vlist']:
        return None
    video_list = videos['list']['vlist']
    selected_video = random.choice(video_list)
    bvid = selected_video.get('bvid')
    if not bvid:
        return None
    return f"https://www.bilibili.com/video/{bvid}"
