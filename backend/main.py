from pathlib import Path
from dotenv import load_dotenv

# Repo root .env (running from backend/ leaves cwd as backend)
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gemini import extract_intent
from actions import execute_actions
import os
import uvicorn
import logging
import json
from typing import Optional

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IntentOS")

app = FastAPI(title="IntentOS Backend")

# 1. Add CORS Middleware (Allow all for MVP robustness)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok", "app": "IntentOS"}

# 2. Process Intent Engine (Multimodal & Identity Aware)
@app.post("/process")
async def process_input(
    text: str = Form(""),
    intent_hint: str = Form(None),
    lat: float = Form(None),
    lng: float = Form(None),
    user_details: str = Form(None), # JSON string from Google Login
    file: Optional[UploadFile] = File(None)
):
    """Takes text + media + identity + location and returns orchestrated intelligence."""
    try:
        logger.info(f"Incoming Request: {text} | Hint: {intent_hint}")
        
        # Parse User Details if provided
        user_info = {}
        if user_details:
            try:
                user_info = json.loads(user_details)
            except:
                logger.warning("Could not parse user_details JSON")

        # Read File Data if provided
        media_bytes = None
        media_type = None
        if file:
            media_bytes = await file.read()
            media_type = file.content_type
            logger.info(f"File Received: {file.filename} ({media_type})")

        # 1. AI Intent Analysis with Triple-Fallback
        intent_analysis = extract_intent(
            user_input=text, 
            media_file=media_bytes, 
            media_type=media_type,
            intent_hint=intent_hint
        )
        logger.info(f"AI Response: {intent_analysis}")
        
        # 2. Real-World Action Orchestration
        # Pass location and user info for actual mapping and mailing
        executed_actions = await execute_actions(
            analysis=intent_analysis,
            lat=lat,
            lng=lng,
            user_info=user_info
        )
        logger.info(f"Orchestrated Actions: {executed_actions}")

        return {
            "input": text,
            "intent_analysis": intent_analysis,
            "executed_actions": executed_actions,
            "user_context": user_info
        }
    except Exception as e:
        logger.error(f"Critical error processing input: {e}")
        return {
            "input": text,
            "intent_analysis": {
                "intent": "emergency_fallback",
                "condition": "processing failure",
                "severity": "high",
                "immediate_actions": ["Call emergency services", "Identify safe location"],
                "simulated_resolutions": ["Emergency signal dispatched"]
            },
            "executed_actions": ["🚨 System Fallback: Call local emergency line immediately."]
        }

# 3. Serve Frontend Static Files
# We check if frontend directory exists (relative to backend for Docker packaging)
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_root():
    """Serves the index.html from frontend or health status if not found."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "message": "Backend running, frontend not found in ./frontend/"}

if __name__ == "__main__":
    # 4. Required for Cloud Run: bind to 0.0.0.0 and use PORT from ENV
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting world-class intent analysis server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)