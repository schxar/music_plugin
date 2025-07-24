import asyncio
import os
from netease_download_tool import download_netease_flac
from msst_separate_tool import msst_separate, find_results_dir
from gradio_vocal_process_tool import gradio_process_vocal
from audio_merge_tool import merge_vocal_and_other

def main(song_name: str, choose: str, quality: str):
    print(f"开始处理: {song_name}")
    loop = asyncio.get_event_loop()
    # 1. 下载网易云音乐FLAC
    flac_path = loop.run_until_complete(download_netease_flac(song_name, choose, quality))
    print(f"FLAC下载完成: {flac_path}")
    # 2. 分离得到vocals/other
    other_wav, vocals_wav = msst_separate(flac_path, results_dir=find_results_dir())
    print(f"分离完成:\nother: {other_wav}\nvocals: {vocals_wav}")
    # 修复vocals_wav文件名不精确问题，自动模糊查找
    import glob
    import os
    vocals_dir = os.path.dirname(vocals_wav)
    vocals_base = os.path.splitext(os.path.basename(vocals_wav))[0]
    # 查找同目录下所有 *_vocals.wav 文件
    candidates = glob.glob(os.path.join(vocals_dir, '*_vocals.wav'))
    if not candidates:
        raise FileNotFoundError(f"未找到任何 *_vocals.wav 文件于: {vocals_dir}")
    # 选取与原 vocals_wav 最相似的文件
    import difflib
    best_match = max(candidates, key=lambda x: difflib.SequenceMatcher(None, os.path.basename(x), vocals_base).ratio())
    if not os.path.exists(best_match):
        raise FileNotFoundError(f"模糊查找后仍未找到可用的 vocals wav 文件: {best_match}")
    if best_match != vocals_wav:
        print(f"[提示] 使用模糊匹配到的 vocals wav: {best_match}")
    vocals_wav = best_match
    # 3. Sovits变声
    changed_wav = gradio_process_vocal(vocals_wav)
    print(f"Sovits变声完成: {changed_wav}")
    # 4. 合成最终wav
    base_name = os.path.splitext(os.path.basename(flac_path))[0]
    final_wav = merge_vocal_and_other(changed_wav, other_wav, base_name)
    print(f"最终合成完成: {final_wav}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        song = sys.argv[1]
        choose = sys.argv[2] if len(sys.argv) > 2 else "1"
        quality = sys.argv[3] if len(sys.argv) > 3 else "1"
    else:
        song = input("请输入网易云歌曲名: ").strip()
        while not song:
            song = input("请输入网易云歌曲名: ").strip()
        choose = input("请输入选择（例如：1）：").strip()
        while not choose:
            choose = input("请输入选择（例如：1）：").strip()
        quality = input("请输入音质（例如：1）：").strip()
        while not quality:
            quality = input("请输入音质（例如：1）：").strip()
    main(song, choose, quality)
