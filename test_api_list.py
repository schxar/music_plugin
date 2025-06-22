import aiohttp
import asyncio
import json
import time

async def find_max_choose(song_name, quality=9, max_try=30):
    api_url = "https://api.vkeys.cn/v2/music/netease"
    max_choose = 0
    async with aiohttp.ClientSession() as session:
        for choose in range(1, max_try+1):
            params = {
                "word": song_name,
                "quality": quality,
                "choose": choose
            }
            async with session.get(api_url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # 判断data是否有效（有data且code==200且data字段不为空）
                    if data.get("code") == 200 and data.get("data"):
                        max_choose = choose
                    else:
                        break
                else:
                    break
    return max_choose

async def fetch_with_fallback(song_name, quality, choose):
    api_url = "https://api.vkeys.cn/v2/music/netease"
    params = {"word": song_name, "quality": quality, "choose": choose}
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("code") == 200 and data.get("data"):
                    return {"choose": choose, "data": data}
                else:
                    print(f"choose={choose} 业务异常，尝试降级...")
            else:
                print(f"choose={choose} 网络异常，尝试降级...")
    return None

async def fetch_song_list(song_name, quality=9, max_results=5):
    max_choose = await find_max_choose(song_name, quality)
    print(f"检测到最大choose为: {max_choose}")
    results = []
    # 先尝试最大choose
    fallback_list = [max_choose, 5, 2, 1]
    for c in fallback_list:
        if c < 1:
            continue
        print(f"尝试choose={c}")
        res = await fetch_with_fallback(song_name, quality, c)
        if res:
            results.append(res)
            break
        else:
            print("等待5秒后重试...")
            time.sleep(5)
    # 继续补全1~max_choose的其他项
    async with aiohttp.ClientSession() as session:
        for choose in range(1, max_choose+1):
            if any(r["choose"] == choose for r in results):
                continue
            params = {"word": song_name, "quality": quality, "choose": choose}
            async with session.get("https://api.vkeys.cn/v2/music/netease", params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results.append({"choose": choose, "data": data})
                else:
                    results.append({"choose": choose, "error": resp.status})
    with open("netease_song_list.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("已保存到 netease_song_list.json")

if __name__ == "__main__":
    song = input("请输入要查询的歌曲名：")
    asyncio.run(fetch_song_list(song))
