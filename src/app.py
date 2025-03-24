from flask import Flask, send_file, request, jsonify
import os
from gtts import gTTS
from deep_translator import GoogleTranslator

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure 'data' directory exists

def translate_to_hindi(text):
    """ Translates English text to Hindi. """
    return GoogleTranslator(source="en", target="hi").translate(text)

@app.route("/generate_tts")
def generate_tts():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name required"}), 400

    input_file = os.path.join(DATA_DIR, f"{company}_summary.txt")
    output_file = os.path.join(DATA_DIR, f"{company}_summary.mp3")

    if not os.path.exists(input_file):
        return jsonify({"error": f"Summary file {input_file} not found"}), 404

    with open(input_file, "r", encoding="utf-8") as f:
        summary_text = f.read()

    hindi_summary = translate_to_hindi(summary_text)
    tts = gTTS(text=hindi_summary, lang="hi")
    tts.save(output_file)

    return jsonify({"message": "TTS generated", "mp3_file": f"/fetch_tts?company={company}"})

@app.route("/fetch_tts")
def fetch_tts():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name required"}), 400

    file_path = os.path.join(DATA_DIR, f"{company}_summary.mp3")
    
    if not os.path.exists(file_path):
        return jsonify({"error": "MP3 file not found"}), 404

    return send_file(file_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
