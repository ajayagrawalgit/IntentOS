from google import genai
from google.genai import types
import os
import json
import re
import base64
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Fallback response if everything fails (must never crash)
DEFAULT_FALLBACK = {
    "intent": "emergency_fallback",
    "condition": "System degradation or API failure",
    "severity": "high",
    "immediate_actions": ["Contact priority emergency services", "Check local surroundings for safety"],
    "simulated_resolutions": ["Emergency signal dispatched to satellites", "GPS lock engaged"]
}

# Corrected Model identifiers (gemini-2.0-flash is the primary world-class model)
MODELS = [
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-pro-latest"
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

def extract_intent(user_input: str, media_file: Optional[bytes] = None, media_type: Optional[str] = None, intent_hint: Optional[str] = None) -> Dict[str, Any]:
    """Tries multiple Gemini models and extracts structured intent data from text and optional media."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        return DEFAULT_FALLBACK

    client = genai.Client(api_key=api_key)

    # 1. Build the Multimodal Payload
    content_parts = []
    
    # Textual Context
    system_instruction = f"""
    You are IntentOS v3, a professional multi-sensory emergency orchestrator.
    Analyze the user's input (Text + optional Image/Video/Audio).
    
    Rules:
    - If an intent hint is provided: "{intent_hint or 'None'}", use it to focus your analysis but overwrite if the data clearly says otherwise.
    - Severity: "low", "medium", or "high".
    - "intent": Precise 1-3 word description.
    - "condition": Detailed analysis of the situation.
    - "immediate_actions": List 1-3 critical life-saving steps the HUMAN must do NOW. (e.g. "Apply pressure", "Move to high ground").
    - "simulated_resolutions": List 1-2 automated steps IntentOS is performing. (e.g. "Ambulance dispatched", "Nearby users notified").
    - Always return JSON ONLY. No conversation.
    """
    
    content_parts.append(system_instruction)
    content_parts.append(f"User Input: {user_input}")

    # Media Content
    if media_file and media_type:
        content_parts.append(types.Part.from_bytes(data=media_file, mime_type=media_type))

    for model_name in MODELS:
        try:
            print(f"DEBUG: Attempting multimodal extraction with {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=content_parts
            )
            
            if response and response.text:
                print(f"SUCCESS: Model {model_name} generated response.")
                return clean_json_response(response.text)
            
        except Exception as e:
            print(f"WARNING: Model {model_name} failed: {e}")
            continue

    return DEFAULT_FALLBACK