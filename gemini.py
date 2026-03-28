import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def extract_intent(user_input):
    prompt = f"""
    You are an emergency intent classifier.

    Return ONLY valid JSON.

    Input: {user_input}

    Output format:
    {{
        "intent": "",
        "condition": "",
        "severity": "",
        "actions": []
    }}
    """

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        return {
            "intent": "unknown",
            "condition": "unknown",
            "severity": "low",
            "actions": ["seek help"]
        }