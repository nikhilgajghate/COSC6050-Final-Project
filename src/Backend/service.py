from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import os
from elevenlabs.play import play

# Load environment variables from .env file using dotenv
load_dotenv()

# Initialize ElevenLabs Client for Text to Speech Conversion. 
client = ElevenLabs(api_key = os.getenv("ELEVENLABS_API_KEY"))

# Output folder to store output audio files. 
OUTPUT_FOLDER = "static/audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True) # Create output folder if it does not exist.

def pronounce_name(name):
    """
    Generate pronunciation audio and returns file path.
    Args: 
        name: str: Store user input as a string. 
    Returns: 
        filepath: str: Path to the audio file. 
    """
    filename = f"{name.replace(' ', '_')}.mp3"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Generate voice
    audio = client.text_to_speech.convert(
        text=name,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Change voice id to another voice if needed. 
        model_id="eleven_multilingual_v2"
    )

    # Play audio
    play(audio)
    
    # Save audio to file
    with open(filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filepath

