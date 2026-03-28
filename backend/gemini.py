from google import genai
import os
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

# Fallback response if everything fails (must never crash)
DEFAULT_FALLBACK = {
    "intent": "medical_emergency",
    "condition": "unknown",
    "severity": "high",
    "actions": ["call ambulance", "seek help"]
}

# Model fallback order as per requirements
MODELS = [
    "gemini-2.0-flash", # Adjusted to 2.0-flash as 2.5 is not yet available in current GENAI SDK
    "gemini-1.5-flash-latest", 
    "gemini-1.5-pro-latest"
]

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON from Gemini's response, handling markdown blocks and noise."""
    print(f"DEBUG: Raw response: {raw_text}")
    
    # 1. Strip markdown code blocks
    cleaned = re.sub(r"```json\s*", "", raw_text)
    cleaned = re.sub(r"```\s*", "", cleaned)
    
    # 2. Extract anything between curly braces using regex (greedy match for the largest object)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decoding failed: {e}")
            
    return DEFAULT_FALLBACK

def extract_intent(user_input: str) -> Dict[str, Any]:
    """Tries multiple Gemini models and extracts structured intent data."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        return DEFAULT_FALLBACK

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are IntentOS, a highly intelligent intent classifier.
    Analyze the following human input and convert it into a structured JSON format.

    Rules:
    - Classify ALL inputs (emergencies, questions, casual talk, tasks).
    - Severity must be: "low", "medium", or "high".
    - "intent" should be a 1-2 word description.
    - "condition" should describe the user's situation.
    - "actions" must be a list of 1-3 concrete steps.
    - Never return "unknown" unless it's impossible to deduce.
    - Always return JSON ONLY.

    Input: "{user_input}"

    Output JSON:
    {{
        "intent": "...",
        "condition": "...",
        "severity": "...",
        "actions": ["...", "..."]
    }}
    """

    for model_name in MODELS:
        try:
            print(f"DEBUG: Attempting model {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            if response and response.text:
                return clean_json_response(response.text)
            
        except Exception as e:
            print(f"WARNING: Model {model_name} failed: {e}")
            continue

    return DEFAULT_FALLBACK