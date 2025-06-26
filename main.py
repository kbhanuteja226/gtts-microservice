from flask import Flask, request, jsonify, send_from_directory
import os
from gtts import gTTS
import uuid

app = Flask(__name__)

# Route to handle TTS request
@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "Missing text"}), 400

    # Create audio directory if it doesn't exist
    os.makedirs("static/audio", exist_ok=True)

    # Generate filename and save file
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("static/audio", filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    # Build and return audio URL
    audio_url = request.host_url + "audio/" + filename
    return jsonify({"audio_url": audio_url})

# Route to serve the generated MP3
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

# Start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
