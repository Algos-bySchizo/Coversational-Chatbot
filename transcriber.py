import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def transcribe(audio_path):
    client = Groq(api_key=os.getenv("API"))

    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(model="whisper-large-v3", file=audio_file, response_format= "text")
        print(f"You said: {result}")
        return result
    