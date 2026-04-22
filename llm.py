import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate(messages):
    client = Groq(api_key=os.getenv("API"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages)
    
    return response.choices[0].message.content