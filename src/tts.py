import os
from gtts import gTTS
from deep_translator import GoogleTranslator

def translate_to_hindi(text):
    """
    Translates English text to Hindi using Deep Translator.
    """
    return GoogleTranslator(source="en", target="hi").translate(text)

def text_to_speech(company, lang="hi"):
    """
    Reads the summarized sentiment report, translates it to Hindi,
    and converts it into speech. Saves the speech as an MP3 file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory
    input_file = os.path.join(base_dir, f"data/{company}_summary.txt")
    output_file = os.path.join(base_dir, f"data/{company}_summary.mp3")

    # Check if the summary file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Summary file {input_file} not found.")
        return

    # Read the summary text
    with open(input_file, "r", encoding="utf-8") as f:
        summary_text = f.read()

    # Translate to Hindi
    hindi_summary = translate_to_hindi(summary_text)
    print(f"📖 Translated Hindi Text:\n{hindi_summary}")

    # Convert Hindi text to speech
    tts = gTTS(text=hindi_summary, lang=lang)
    tts.save(output_file)
    
    print(f"✅ Hindi Speech saved to {output_file}")

    # Play the speech file (Windows: start, Mac: open, Linux: xdg-open)
    os.system(f"start {output_file}" if os.name == "nt" else f"xdg-open {output_file}")

if __name__ == "__main__":
    company_name = "Microsoft"
    text_to_speech(company_name)
