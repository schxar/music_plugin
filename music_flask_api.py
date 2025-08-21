from flask import Flask, request, render_template_string, jsonify, send_file
from napcat_client import NapcatClient
from gradio_vocal_process_tool import gradio_process_vocal_tts
import threading
from test_full_pipeline import main
import os

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>网易云音乐处理 & Napcat 语音发送</title>
</head>
<body>
    <h2>网易云音乐处理</h2>
    <form method="post">
        <label>歌曲名: <input type="text" name="song" required></label><br><br>
        <label>选择: <input type="text" name="choose" value="1" required></label><br><br>
        <label>音质: <input type="text" name="quality" value="9" required></label><br><br>
        <input type="submit" value="提交">
    </form>
    <hr>
    <h2>Napcat 语音发送</h2>
    <form method="post" enctype="multipart/form-data">
        <label>上传语音文件: <input type="file" name="voice_file" accept="audio/*" required></label><br><br>
        <label>群号: <input type="text" name="group_id"></label><br><br>
        <label>QQ号: <input type="text" name="user_id"></label><br><br>
        <input type="submit" value="发送">
    </form>
    <hr>
    <h2>TTS 语音合成</h2>
    <form method="post" action="/tts">
        <label>文本: <textarea name="text" rows="4" cols="50" required></textarea></label><br><br>
        <input type="submit" value="合成语音">
    </form>
    {% if result %}
    <h3>处理结果</h3>
    <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
'''

def run_main(song, choose, quality, result_list):
    import io
    import sys
    import asyncio
    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf
    # 修复子线程无 event loop 问题
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        main(song, choose, quality)
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        sys.stdout = sys_stdout
    result_list.append(buf.getvalue())

# Napcat 发送语音功能示例
napcat = NapcatClient()

def send_group_voice(group_id, file_path):
    """
    发送语音到群聊
    """
    return napcat.send_group_record(group_id, file_path)

def send_private_voice(user_id, file_path):
    """
    发送语音到私聊
    """
    return napcat.send_private_record(user_id, file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Napcat 语音发送表单优先判断
        if 'voice_file' in request.files:
            voice_file = request.files['voice_file']
            group_id = request.form.get('group_id', '').strip()
            user_id = request.form.get('user_id', '').strip()
            if voice_file and (group_id or user_id):
                import os, tempfile
                suffix = os.path.splitext(voice_file.filename)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    voice_file.save(tmp)
                    tmp_path = tmp.name
                try:
                    if group_id:
                        result = send_group_voice(int(group_id), tmp_path)
                    elif user_id:
                        result = send_private_voice(int(user_id), tmp_path)
                except Exception as e:
                    result = f"发送失败: {e}"
                finally:
                    os.remove(tmp_path)
            else:
                result = '请上传语音文件并填写群号或QQ号'
        # 网易云音乐处理表单
        elif 'song' in request.form:
            song = request.form.get('song', '').strip()
            choose = request.form.get('choose', '').strip()
            quality = request.form.get('quality', '').strip()
            result_list = []
            t = threading.Thread(target=run_main, args=(song, choose, quality, result_list))
            t.start()
            t.join()
            result = result_list[0] if result_list else '无输出'
    return render_template_string(HTML_FORM, result=result)

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form.get('text') or (request.json and request.json.get('text'))
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        audio_path = gradio_process_vocal_tts(text)
        return send_file(audio_path, mimetype='audio/wav', as_attachment=True, download_name=os.path.basename(audio_path))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tts_demo', methods=['GET'])
def tts_demo():
    html = '''
    <!DOCTYPE html>
    <html lang="zh-cn">
    <head>
        <meta charset="UTF-8">
        <title>TTS语音合成Demo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h2>文字转语音</h2>
        <textarea id="tts_text" rows="4" cols="50" placeholder="请输入要合成的文本..."></textarea><br>
        <button onclick="tts()">合成并播放</button>
        <br><br>
        <audio id="tts_audio" controls style="display:none;"></audio>
        <script>
        function tts() {
            var text = document.getElementById('tts_text').value;
            if (!text) { alert('请输入文本'); return; }
            var formData = new FormData();
            formData.append('text', text);
            fetch('/tts', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error('合成失败');
                return response.blob();
            })
            .then(blob => {
                var audio = document.getElementById('tts_audio');
                audio.src = URL.createObjectURL(blob);
                audio.style.display = '';
                audio.play();
            })
            .catch(err => alert(err));
        }
        </script>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211, debug=True)
