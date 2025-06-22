import aiohttp
import aiofiles
import base64
import os
import asyncio

async def download_and_save_audio(audio_url, song, singer, ext):
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "music_cache")
    os.makedirs(cache_dir, exist_ok=True)
    file_name = f"{song}_{singer}{ext}"
    file_name = file_name.replace("/", "_").replace("\\", "_")
    cache_path = os.path.join(cache_dir, file_name)
    async with aiohttp.ClientSession() as session:
        async with session.get(audio_url) as resp:
            if resp.status == 200:
                content = await resp.read()
                async with aiofiles.open(cache_path, "wb") as f:
                    await f.write(content)
                print(f"{file_name}下载完毕，已保存到: {cache_path}")
                async with aiofiles.open(cache_path, "rb") as f:
                    audio_bytes = await f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                print(f"Base64长度: {len(audio_base64)}")
            else:
                print("音频下载失败，无法发送音频")

if __name__ == "__main__":
    url = "http://m8.music.126.net/20250622052813/c66ace2414a345eb327ae8f27112fae6/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/27285438055/8edc/348f/5658/fb8b972b74472078bad641dc4d51e0bc.flac?vuutv=Dp0LzAXnsuzK3lsRWXc3fhhYMGG7BCm+ZJQD+1QfDeqIu/w0bl83lBA9kRrftJqkEzX2zTvs0QbBjGhcnaTutjF6NU+pkhtW4YeQtn8elCY="
    asyncio.run(download_and_save_audio(url, "测试歌曲", "测试歌手", ".flac"))
