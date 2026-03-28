from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gemini import extract_intent
from actions import execute_actions
import os
import uvicorn
import logging

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

# 2. Process Intent Engine
@app.post("/process")
def process_input(data: InputData):
    """Takes messy human input and returns structured analysis and simulated actions."""
    try:
        logger.info(f"Incoming Request: {data.text}")
        
        # 1. AI Intent Analysis with Triple-Fallback
        intent_analysis = extract_intent(data.text)
        logger.info(f"AI Response: {intent_analysis}")
        
        # 2. Simulated Action Execution
        executed_actions = execute_actions(intent_analysis)
        logger.info(f"Simulated Actions: {executed_actions}")

        return {
            "input": data.text,
            "intent_analysis": intent_analysis,
            "executed_actions": executed_actions
        }
    except Exception as e:
        logger.error(f"Error processing input: {e}")
        # Secondary fallback case to ensure it NEVER crashes with 500 error
        return {
            "input": data.text,
            "intent_analysis": {
                "intent": "critical_error",
                "condition": "processing error",
                "severity": "high",
                "actions": ["call ambulance", "seek help"]
            },
            "executed_actions": ["🚑 Ambulance called (simulated) (emergency fallback)"]
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