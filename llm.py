import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate(messages):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    formatted = []

    for m in messages:
        if hasattr(m, "role"):
            formatted.append({"role": m.role, "content": m.content})
        else:
            formatted.append(m)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=formatted)
    
    return response.choices[0].message.content
