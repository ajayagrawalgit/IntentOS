# IntentOS - Next-Gen AI Intent Orchestrator

**Production-Ready MVP for AI-Driven Action Analysis**

IntentOS is a world-class AI system that converts messy human text into structured intelligence (JSON) and executes simulated real-world actions. Designed for high availability and mission-critical scenarios, it ensures that human intent is never lost, even during AI model failure.

---

## 🚀 Live Demo
**Link**: [https://intent-os-217442463149.us-central1.run.app](https://intent-os-217442463149.us-central1.run.app)

---

## 🧠 Core Features

### 1. Robust AI Resilience (Triple-Fallback)
The system uses a 3-tier model fallback logic to ensure maximum reliability:
1.  **Primary**: `gemini-2.0-flash` (Highest speed/accuracy)
2.  **Secondary**: `gemini-1.5-flash-latest` (Stable fallback)
3.  **Tertiary**: `gemini-1.5-pro-latest` (Deep reasoning fallback)

### 2. "Never Crash" Architecture
- **Fail-Safe Logic**: If all AI models fail or quota is reached, the system returns a pre-defined, high-priority fallback JSON to ensure critical actions (like calling an ambulance) are still triggered.
- **Regex Parsing**: Robustly extracts JSON from messy or conversational LLM responses, stripping whitespace, markdown (` ```json `), and additional text.

### 3. Premium Glassmorphic UI 
A state-of-the-art frontend built with **Vanilla JS** and **Custom CSS**:
- **Aesthetic**: Dark Obsidian theme, backdrop-filters (blur), and vivid gradients.
- **Performance**: Zero external UI frameworks for sub-100ms load times.
- **UX**: Micro-animations, responsive layout, and real-time JSON payload inspection.

### 4. Direct Cloud Integration
- Deployed via **Google Cloud Run** with a unified container serving both Backend (FastAPI) and Frontend static assets.

---

## 🛠️ Tech Stack
- **Backend**: Python 3.11 + FastAPI
- **AI Engine**: Google Gemini (`google-genai` package)
- **Frontend**: HTML5 + Vanilla Javascript + Modern CSS (Inter & Outfit Google Fonts)
- **Deployment**: Docker + Google Artifact Registry + Cloud Run

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Google Gemini API Key

### Installation

1.  Navigate to the project root:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set environment variables:
    ```bash
    export GEMINI_API_KEY="your-api-key-here"
    ```
4.  Run the application:
    ```bash
    python main.py
    ```
5.  Access the UI:
    Visit `http://localhost:8080` in your browser.

---

## 🐳 Docker and Deployment

### Running Locally with Docker
```bash
docker build -t intent-os ./backend
docker run -p 8080:8080 -e GEMINI_API_KEY="your-key" intent-os
```

### Deploying to Google Cloud Run
```bash
gcloud run deploy intent-os --source backend/ \
--platform managed --region us-central1 \
--set-env-vars GEMINI_API_KEY="your-key" \
--allow-unauthenticated
```

---

## 📂 Project Structure
```text
intent-os/
└── backend/
    ├── main.py           # FastAPI entry point & unified file hosting
    ├── gemini.py         # AI Logic & Fallback Engine
    ├── actions.py        # Action Simulation Logic
    ├── requirements.txt  # Python dependencies
    ├── Dockerfile        # Container configuration
    └── frontend/         # Premium UI assets (served as static files)
        ├── index.html
        ├── app.js
        └── styles.css
```

---

## ⚡ Hackathon Submission Notes
**Project Goal achieved**: Converting messy human text (e.g., "my car engine is smoking on the highway") into structured actionable JSON without ever crashing.

**Key Technical Differentiator**: The combination of regex-based JSON cleaning and a hardcoded emergency fallback layer ensures that **IntentOS** is the most reliable intent classifier for messy real-world inputs.
