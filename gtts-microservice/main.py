from flask import Flask, request, send_file
from gtts import gTTS
import uuid

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return {"error": "No text provided"}, 400

    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")

# For production:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
