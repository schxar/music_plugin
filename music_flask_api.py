from flask import Flask, request, render_template_string, jsonify
from napcat_client import NapcatClient
import threading
from test_full_pipeline import main

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211, debug=True)
