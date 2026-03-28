# IntentOS setup overview

IntentOS is a FastAPI backend plus a static frontend. Source code lives under `src/`:

| Path | Role |
|------|------|
| `src/backend/` | Python app (`main.py`), API routes, Gemini/actions/email integration |
| `src/frontend/` | Static assets served at `/` and `/static/` |

Configuration uses environment variables (see `.env.template` at the repository root). For production on Google Cloud Run, set the same variables in the Cloud Run service.

## Prerequisites (all environments)

- **Python 3.11+** for local runs
- **Google Cloud SDK (`gcloud`)** for Cloud Run deployment
- **APIs and credentials** used by the app:
  - [Google AI Studio](https://aistudio.google.com/) — Gemini API key (`GEMINI_API_KEY`)
  - [Google Cloud Console](https://console.cloud.google.com/) — Maps Elevation API key (`MAPS_API_KEY`)
  - Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) for SMTP (`GMAIL_USER`, `GMAIL_APP_PASSWORD`)

## Security

- Do **not** commit real API keys, Gmail passwords, or `.env` files. The repository includes `.env.template` only.
- If keys were ever shared in chat, issue logs, or screenshots, **rotate** them in Google Cloud / AI Studio / Google Account and update Cloud Run env vars.

## Detailed guides

| Document | Contents |
|----------|----------|
| [LOCAL.md](LOCAL.md) | Virtualenv, install dependencies, run the server locally, optional checks |
| [CLOUDRUN.md](CLOUDRUN.md) | Enable GCP APIs, IAM, create keys, build with the root `Dockerfile`, deploy to Cloud Run |

Start with [LOCAL.md](LOCAL.md) for development and [CLOUDRUN.md](CLOUDRUN.md) when you are ready to deploy.
