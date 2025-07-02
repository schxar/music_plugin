from pydub import AudioSegment
import os

def merge_vocal_and_other(vocal_wav: str, other_wav: str, base_name: str = None) -> str:
    """
    合并变换后vocal和other音轨，返回合成后的wav路径。
    :param vocal_wav: 变换后人声wav路径
    :param other_wav: 乐器轨道wav路径
    :param base_name: 基础文件名，用于生成输出文件名
    :return: 合成后wav路径
    """
    if not os.path.exists(vocal_wav):
        raise FileNotFoundError(f"vocal_wav不存在: {vocal_wav}")
    if not os.path.exists(other_wav):
        raise FileNotFoundError(f"other_wav不存在: {other_wav}")
    audio1 = AudioSegment.from_file(vocal_wav, format="wav")
    audio2 = AudioSegment.from_file(other_wav, format="wav")
    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]
    combined = audio1.overlay(audio2)
    output_path = os.path.join(os.path.dirname(vocal_wav), f"{base_name}_changed.wav") if base_name else os.path.join(os.path.dirname(vocal_wav), "combined.wav")
    combined.export(output_path, format="wav")
    return output_path

if __name__ == "__main__":
    # 示例用法
    v = os.path.join(os.path.dirname(__file__), 'cache', 'gradio_output.wav')
    o = os.path.join(os.path.dirname(__file__), 'cache', 'test_other.wav')
    try:
        out = merge_vocal_and_other(v, o)
        print(f"合成完成: {out}")
    except Exception as e:
        print(f"合成失败: {e}")
