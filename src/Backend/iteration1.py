from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import os

load_dotenv()

client = ElevenLabs(api_key = os.getenv("ELEVENLABS_API_KEY"))

OUTPUT_FOLDER = "static/audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def pronounce_name(name):
    """Generate pronunciation audio and returns file path"""
    filename = f"{name.replace(' ', '_')}.mp3"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    #Generate voice
    audio = client.text_to_speech.convert(
        text=name,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2"
    )

    with open(filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filepath

