import os
import requests
import aiohttp
import asyncio

def get_cache_dir():
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

async def download_netease_flac(song_name: str, choose: str, quality: str, api_url: str = "https://api.vkeys.cn") -> str:
    """
    搜索网易云音乐并下载FLAC音频到cache目录，返回文件路径。
    :param song_name: 歌曲名
    :param quality: 音质（默认9）
    :param api_url: API地址 
    :return: 下载完成的flac文件路径
    """
    async with aiohttp.ClientSession() as session:
        params = {
            "word": song_name,
            "quality": quality,
            "choose": choose
        }
        async with session.get(f"{api_url}/v2/music/netease", params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("code") == 200 and data.get("data", {}).get("url"):
                    url = data["data"]["url"]
                    real_song_name = data["data"].get("song", song_name)
                    # 清理非法文件名字符
                    import re
                    safe_song_name = re.sub(r'[\\/:*?"<>|]', '_', real_song_name)
                    cache_dir = get_cache_dir()
                    flac_path = os.path.join(cache_dir, f"{safe_song_name}.flac")
                    # 下载文件
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(flac_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    return flac_path
                else:
                    raise Exception(f"API未返回有效音频链接: {data}")
            else:
                raise Exception(f"API请求失败: {response.status}")

if __name__ == "__main__":
    import sys
    song = sys.argv[1] if len(sys.argv) > 1 else "晴天"
    loop = asyncio.get_event_loop()
    try:
        flac_file = loop.run_until_complete(download_netease_flac(song))
        print(f"下载完成: {flac_file}")
    except Exception as e:
        print(f"下载失败: {e}")
