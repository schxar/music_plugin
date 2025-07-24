import os
import requests
import aiohttp
import asyncio
import time
import json
import hashlib

def get_cache_dir():
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def get_json_cache_path(song_name, choose, quality):
    # 用hash避免文件名过长和特殊字符问题
    key = f"{song_name}_{choose}_{quality}"
    key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    cache_dir = get_cache_dir()
    return os.path.join(cache_dir, f"{key_hash}.json")

def is_cache_valid(cache_path, expire_seconds=86400):
    if not os.path.exists(cache_path):
        return False
    mtime = os.path.getmtime(cache_path)
    return (time.time() - mtime) < expire_seconds

async def download_netease_flac(song_name: str, choose: str, quality: str, api_url: str = "https://api.vkeys.cn") -> str:
    """
    搜索网易云音乐并下载FLAC音频到cache目录，返回文件路径。
    :param song_name: 歌曲名
    :param quality: 音质（默认9）
    :param api_url: API地址 
    :return: 下载完成的flac文件路径
    """
    import re
    cache_dir = get_cache_dir()
    # 与 plugin.py 保持一致，去除括号及特殊符号
    safe_song_name = re.sub(r'[\\/:*?"<>|()（）\[\]{}]', '', song_name)
    flac_path = os.path.join(cache_dir, f"{safe_song_name}.flac")
    if os.path.exists(flac_path):
        return flac_path

    json_cache_path = get_json_cache_path(song_name, choose, quality)
    data = None

    if is_cache_valid(json_cache_path):
        # 读取缓存
        with open(json_cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # 请求API并缓存
        async with aiohttp.ClientSession() as session:
            params = {
                "word": song_name,
                "quality": quality,
                "choose": choose
            }
            async with session.get(f"{api_url}/v2/music/netease", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    with open(json_cache_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
                else:
                    raise Exception(f"API请求失败: {response.status}")

    if data.get("code") == 200 and data.get("data", {}).get("url"):
        url = data["data"]["url"]
        real_song_name = data["data"].get("song", song_name)
        safe_song_name = re.sub(r'[\\/:*?"<>|()（）\[\]{}]', '', real_song_name)
        flac_path = os.path.join(cache_dir, f"{safe_song_name}.flac")
        if os.path.exists(flac_path):
            return flac_path
        # 下载文件
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(flac_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return flac_path
    else:
        raise Exception(f"API未返回有效音频链接: {data}")

if __name__ == "__main__":
    import sys
    song = sys.argv[1] if len(sys.argv) > 1 else "晴天"
    loop = asyncio.get_event_loop()
    try:
        flac_file = loop.run_until_complete(download_netease_flac(song, "netease", "9"))
        print(f"下载完成: {flac_file}")
    except Exception as e:
        print(f"下载失败: {e}")
