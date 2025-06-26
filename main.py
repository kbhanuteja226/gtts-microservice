from flask import Flask, request, jsonify, send_from_directory
import os
from gtts import gTTS
import uuid

app = Flask(__name__)

# ✅ Only /tmp is writable on Render Free Tier
AUDIO_FOLDER = "/tmp/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "Missing text"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    # Save TTS audio to /tmp/audio
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    # Return full public URL
    audio_url = request.host_url + "audio/" + filename
    return jsonify({"audio_url": audio_url})

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
