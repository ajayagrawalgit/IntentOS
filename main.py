from fastapi import FastAPI
from pydantic import BaseModel
from gemini import extract_intent
from actions import execute_actions
import os

app = FastAPI()

class InputData(BaseModel):
    text: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/process")
def process_input(data: InputData):
    intent_data = extract_intent(data.text)
    actions = execute_actions(intent_data)

    return {
        "input": data.text,
        "intent_analysis": intent_data,
        "executed_actions": actions
    }

# 👇 Required for Cloud Run
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)