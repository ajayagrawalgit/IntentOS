# IntentOS v7 - Project Portfolio & Setup Guide

**Mission**: A multi-sensory AI emergency orchestrator that sees, hears, and acts with precision using Google's world-class cloud infrastructure.

---

## 🏗️ Google Services Portfolio (The "Judge's Guide")

IntentOS demonstrates the combined power of **5+ Google Cloud Services** in a unified, mission-critical application:

1.  **Google Gemini (Multimodal)**: Uses `gemini-2.0-flash` for high-speed analysis of Text, Images, Video, and Voice.
2.  **Google Identity (GIS)**: Integrated "Sign in with Google" for secure, verified sender identification.
3.  **Google Maps (Elevation API)**: Real-world GPS-to-Altitude mapping to assist in rescue scenarios.
4.  **Google Gmail API (SMTP)**: Automated emergency dispatch via Gmail's secure SMTP infrastructure.
5.  **Google Cloud Run**: Serverless container hosting for the unified FastAPI/Frontend stack.
6.  **Human-Centric Design**: Voice Verification (Listen-back) and Custom Imagery for intuitive emergency use.

---

## 🛠️ Local Setup Instructions (Manual)

Follow these steps to run IntentOS on your local development machine.

### 1. Prerequisites
- Python 3.11+
- A Google Cloud Project with Billing Enabled.
- API Key from [Google AI Studio](https://aistudio.google.com/).

### 2. Environment Configuration
Create a `.env` file in the `backend/` directory or export these in your shell:
```bash
export GEMINI_API_KEY="AIzaSy..."
export MAPS_API_KEY="AIzaSy..."
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

### 3. Installation & Run
```bash
# Navigate to backend
cd backend

# Create Virtual Environment (Optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Start Server
python3 main.py
```
**Access**: Open `http://localhost:8080` in your browser.

---

## ☁️ Cloud Deployment Log (History of Commands)

Below is the exact log of commands used to successfully deploy IntentOS to Google Cloud Run during this session:

### 1. Project Initialization
```bash
gcloud config set project autonomous-mote-491605-q5
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com
```

### 2. IAM & Permissions (Fix for Build Errors)
```bash
# Granting necessary permissions to the Compute Service Account
gcloud projects add-iam-policy-binding autonomous-mote-491605-q5 \
  --member=serviceAccount:217442463149-compute@developer.gserviceaccount.com \
  --role=roles/cloudbuild.builds.builder

gcloud projects add-iam-policy-binding autonomous-mote-491605-q5 \
  --member=serviceAccount:217442463149-compute@developer.gserviceaccount.com \
  --role=roles/storage.admin
```

### 3. Final Production Deployment
```bash
gcloud run deploy intent-os \
  --source backend/ \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY="$GEMINI_API_KEY",MAPS_API_KEY="$MAPS_API_KEY",GMAIL_USER="$GMAIL_USER",GMAIL_APP_PASSWORD="$GMAIL_APP_PASSWORD"
```

---

## 🎯 Future Roadmap (Bonus Suggestions)
To further maximize Google Service points, the following can be integrated:
- **Google Cloud Storage**: Transition from ephemeral memory to permanent storage for user-uploaded videos/evidence.
- **Google Cloud Pub/Sub**: Use for asynchronous dispatch of multiple emergency alerts to external systems.
- **Vertex AI Search**: Index historical incident data for improved context-aware AI safety advice.
