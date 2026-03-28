# Local development

These steps assume you are at the **repository root** (the directory that contains `src/` and `Dockerfile`).

## 1. Clone and enter the project

```bash
git clone <your-repo-url> IntentOS
cd IntentOS
```

## 2. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r src/backend/requirements.txt
```

## 3. Environment variables

Copy the template and edit values (file stays local; it is gitignored):

```bash
cp .env.template .env
```

Edit `.env` and set at least:

- `GEMINI_API_KEY` — from [Google AI Studio](https://aistudio.google.com/apikey)
- `MAPS_API_KEY` — Google Maps key with **Elevation API** enabled
- `GMAIL_USER` — Gmail address used to send alert mail
- `GMAIL_APP_PASSWORD` — 16-character Gmail app password (spaces optional)

Optional:

- `EMERGENCY_EMAIL_TO` — if set, overrides the recipient for emergency emails (defaults to `GMAIL_USER`)

The app loads `.env` from the **repository root** when you run `main.py` from `src/backend/` (see `src/backend/main.py`).

## 4. Run the server

From the repository root:

```bash
cd src/backend
python main.py
```

Or with explicit port:

```bash
PORT=8080 python main.py
```

Open **http://localhost:8080** in a browser.

Health check:

```bash
curl -s http://localhost:8080/health
```

## 5. Optional: proportional-response checks

Integration-style tests (mock external APIs) expect imports from `src/backend`:

```bash
cd src/backend
python verify_proportional_response.py
```

You should see `PASS` lines for high and low severity paths.

## 6. Optional: local Docker (same layout as Cloud Run)

From the **repository root** (where `Dockerfile` lives):

```bash
docker build -t intent-os:local .
docker run --rm -p 8080:8080 \
  --env-file .env \
  intent-os:local
```

Then open http://localhost:8080 .
