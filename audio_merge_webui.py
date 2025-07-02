from flask import Flask, render_template_string, request, send_file
from pydub import AudioSegment
import io

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>音频合成工具</title>
</head>
<body>
    <h2>上传两个音频文件进行合成（叠加）</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="audio1" accept="audio/wav" required><br><br>
        <input type="file" name="audio2" accept="audio/wav" required><br><br>
        <button type="submit">合成并下载</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['audio1']
        file2 = request.files['audio2']
        audio1 = AudioSegment.from_file(file1, format="wav")
        audio2 = AudioSegment.from_file(file2, format="wav")
        # 使两个音频长度一致
        min_len = min(len(audio1), len(audio2))
        audio1 = audio1[:min_len]
        audio2 = audio2[:min_len]
        combined = audio1.overlay(audio2)
        buf = io.BytesIO()
        combined.export(buf, format="wav")
        buf.seek(0)
        return send_file(buf, as_attachment=True, download_name="combined.wav", mimetype="audio/wav")
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
