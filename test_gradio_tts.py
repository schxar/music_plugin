import os
from gradio_vocal_process_tool import gradio_process_vocal_tts

if __name__ == "__main__":
    text = input("请输入要合成的文本：")
    try:
        wav_path = gradio_process_vocal_tts(text)
        print(f"合成完成，输出文件：{wav_path}")
        if os.path.exists(wav_path):
            print("文件存在，可以试听或处理。")
        else:
            print("文件未生成！")
    except Exception as e:
        print(f"处理失败: {e}")
