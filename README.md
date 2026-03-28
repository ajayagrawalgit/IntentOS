# IntentOS

Multi-sensory AI emergency orchestrator: text, images, video, and voice are analyzed with **Google Gemini**, then the backend can run real-world follow-ups: **Maps Elevation** for altitude, **Gmail SMTP** for alerts, and **Google Identity (GIS)** on the client for verified sign-in. The stack is **FastAPI** + static frontend, packaged in **Docker** and deployed to **Google Cloud Run**.

**Live demo:** [intent-os (Cloud Run)](https://intent-os-217442463149.us-central1.run.app)

---

## Features

- **Multimodal analysis**: Gemini (`gemini-2.0-flash` with fallbacks) interprets text plus optional image, video, or audio uploads.
- **Severity-aware actions**: Higher-severity intents trigger elevation lookup when coordinates exist and automated emergency emails.
- **Configurable Alerts**: Users can configure multiple emergency email recipients via the UI.
- **Persistent Profiles**: Emergency contacts are saved to **Google Cloud Firestore** and automatically loaded when the user signs in with Google.
- **Identity**: Google Sign-In (GIS) in the UI so requests carry verified user context and enable persistent profile features.
- **Location**: Browser geolocation feeds lat/lng into `/process` with manual retry support for better reliability.
- **Voice**: Record and playback before submit (MediaRecorder).
- **UI**: Dark glassmorphic layout with real-time feedback on location and contact status.

---

## Google services used

| Service | Role |
|---------|------|
| [Google AI (Gemini)](https://ai.google.dev/) | Intent extraction and multimodal reasoning (`GEMINI_API_KEY`) |
| [Maps Elevation API](https://developers.google.com/maps/documentation/elevation) | Altitude from lat/lng (`MAPS_API_KEY`) |
| [Gmail SMTP](https://support.google.com/mail/answer/7126229) | Outbound alert email (`GMAIL_USER`, `GMAIL_APP_PASSWORD`; optional `EMERGENCY_EMAIL_TO`) |
| [Google Identity Services](https://developers.google.com/identity/gsi/web) | Sign-in with Google (OAuth client ID in `src/frontend/index.html`) |
| [Cloud Run](https://cloud.google.com/run) | Serverless container hosting (`Dockerfile` at repo root) |

Enable APIs, IAM, keys, and deploy steps are documented in **[docs/CLOUDRUN.md](docs/CLOUDRUN.md)**.

---

## Repository layout

| Path | Description |
|------|-------------|
| `src/backend/` | FastAPI app (`main.py`), Gemini, actions, email |
| `src/frontend/` | Static assets (HTML, CSS, JS, `assets/`) served by the backend |
| `Dockerfile` | Root build context for Cloud Run (`gcloud run deploy --source .`) |
| `docs/` | Documentation: start with **[docs/README.md](docs/README.md)**, then [LOCAL.md](docs/LOCAL.md) and [CLOUDRUN.md](docs/CLOUDRUN.md) |
| `.env.template` | Example environment variable names (copy to `.env` locally) |

---

## Prerequisites

Python **3.11+**, a **Google Cloud** project with billing (for Cloud Run) and **`gcloud`**, plus Gemini, Maps (Elevation), and Gmail app credentials. Security and credential handling are summarized in **[docs/README.md](docs/README.md)**; creation and rotation details are in **[docs/CLOUDRUN.md](docs/CLOUDRUN.md)**.

Never commit real secrets. Use `.env` locally (gitignored) and Cloud Run env vars or Secret Manager in production.

---

## Documentation

The **[docs/](docs/)** folder is the documentation home. **[docs/README.md](docs/README.md)** is the setup overview (layout, prerequisites, security, and links to the guides below).

| Document | Contents |
|----------|----------|
| [docs/README.md](docs/README.md) | Setup overview, `src/` layout, prerequisites, security |
| [docs/LOCAL.md](docs/LOCAL.md) | Virtualenv, install, run `main.py`, health check, optional Docker |
| [docs/CLOUDRUN.md](docs/CLOUDRUN.md) | `gcloud` project, APIs, IAM, keys, production deploy |

---

## Quick start (local)

From the repository root:

```bash
cp .env.template .env
# Edit .env with your GEMINI_API_KEY, MAPS_API_KEY, GMAIL_USER, GMAIL_APP_PASSWORD

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r src/backend/requirements.txt

cd src/backend
python main.py
```

Open **http://localhost:8080**. Health: `curl -s http://localhost:8080/health`

Optional checks (mocked APIs):

```bash
cd src/backend && python verify_proportional_response.py
```

Step-by-step local options (including Docker) are in **[docs/LOCAL.md](docs/LOCAL.md)**.

---

## Deploy to Cloud Run

Build context is the **repository root** (the `Dockerfile` copies `src/backend` and `src/frontend`). From the repo root:

```bash
export GEMINI_API_KEY="your-key"
export MAPS_API_KEY="your-key"
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"

gcloud config set project YOUR_GCP_PROJECT_ID

gcloud run deploy intent-os \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY},MAPS_API_KEY=${MAPS_API_KEY},GMAIL_USER=${GMAIL_USER},GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}"
```

Full checklist (API enablement, IAM for Cloud Build, OAuth origins for GIS) is in **[docs/CLOUDRUN.md](docs/CLOUDRUN.md)**.

---

## Tech stack

- **Runtime**: Python 3.11, FastAPI, Uvicorn  
- **Frontend**: HTML, CSS, JavaScript (vanilla)  
- **Container**: Docker (slim Python base)  
- **Cloud**: Google Cloud Run (source deploy + Artifact Registry via Cloud Build)

---

## Future work

Ideas for extending the system (not implemented in-tree):

- Persist uploads with **Cloud Storage**
- Async fan-out of alerts with **Pub/Sub**
- Retrieval-augmented guidance with **Vertex AI Search** or similar

---

## License

See [LICENSE](LICENSE).


---
A project made for
<img width="1056" height="331" alt="image" src="https://github.com/user-attachments/assets/97c14ba5-e65b-4404-a5c6-6142b6a7412a" />
