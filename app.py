from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = "AQ.Ab8RN6J6gTtSNVNRIw0T3ndC8SbBkLwF1jN7noojEcvtCAhX4g"

class GrammarInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Grammar Checker API Running"}

@app.post("/check")
def check_grammar(data: GrammarInput):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    prompt = f"""
Correct the grammar of the following sentence.
Return only the corrected sentence.

Sentence:
{data.text}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()

    corrected = result["candidates"][0]["content"]["parts"][0]["text"]

    return {"corrected": corrected}