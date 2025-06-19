from flask import Flask, request, jsonify
import os
from gtts import gTTS
import uuid

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "Missing text"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang=lang)
    filepath = f"static/audio/{filename}"
    os.makedirs("static/audio", exist_ok=True)
    tts.save(filepath)

    audio_url = request.host_url + "audio/" + filename
    return jsonify({"audio_url": audio_url})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
