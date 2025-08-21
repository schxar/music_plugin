from flask import Flask, request, send_file, jsonify
import os
from gradio_vocal_process_tool import gradio_process_vocal_tts

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form.get('text') or request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        audio_path = gradio_process_vocal_tts(text)
        return send_file(audio_path, mimetype='audio/wav', as_attachment=True, download_name=os.path.basename(audio_path))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
