# Deploy to Google Cloud Run

Cloud Run builds from the **repository root** using the root `Dockerfile`, which copies `src/backend/` and `src/frontend/` into the container. Deploy with `--source .` from that directory.

Replace placeholders such as `YOUR_PROJECT_ID`, region, and service name to match your environment.

## 1. Install and authenticate gcloud

```bash
# https://cloud.google.com/sdk/docs/install
gcloud --version
gcloud auth login
gcloud auth application-default login
```

## 2. Select a Google Cloud project

```bash
gcloud projects list
gcloud config set project YOUR_PROJECT_ID
```

Confirm:

```bash
gcloud config get-value project
```

## 3. Enable billing

Billing must be enabled on the project (Console: **Billing** → link a billing account). Without it, Cloud Run and Cloud Build will fail.

## 4. Enable required Google APIs

```bash
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project=YOUR_PROJECT_ID
```

Optional (if you use Maps from the same project for other tooling):

```bash
gcloud services enable maps-backend.googleapis.com --project=YOUR_PROJECT_ID
```

Elevation requests use a **Maps API key** (HTTP API), not necessarily a separate “enable” for Cloud Run, but the key must have **Elevation API** allowed in Google Cloud Console → **APIs & Services** → **Credentials** → your key → **API restrictions**.

## 5. Service account permissions for Cloud Build (source deploy)

Source-based deploys use Cloud Build to build the container. The default Compute Engine service account often needs extra roles on first use.

Find your project number:

```bash
gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)'
```

Grant roles (replace `PROJECT_NUMBER`):

```bash
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)')

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/storage.admin"
```

If deploy still fails with Artifact Registry or Run permissions, grant the Cloud Build service account **Cloud Run Admin** and **Service Account User** on the project per [Cloud Run source deploy troubleshooting](https://cloud.google.com/run/docs/deploying-source-code).

## 6. Create API keys and app secrets (outside GCP)

These values are passed to Cloud Run as environment variables.

### Gemini (`GEMINI_API_KEY`)

1. Open [Google AI Studio](https://aistudio.google.com/apikey).
2. Create an API key and restrict it in AI Studio / Google Cloud if possible.

### Maps Elevation (`MAPS_API_KEY`)

1. Open [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Credentials**.
2. **Create credentials** → **API key**.
3. **Restrict key** → **API restrictions** → restrict to **Elevation API** (and any other Maps APIs you need).
4. Optionally restrict by HTTP referrer or IP for browser vs server use; the backend calls the Elevation API from Cloud Run’s egress IP.

### Gmail SMTP (`GMAIL_USER`, `GMAIL_APP_PASSWORD`)

1. Use a Gmail or Google Workspace account.
2. Enable [2-Step Verification](https://myaccount.google.com/security).
3. Create an [App Password](https://myaccount.google.com/apppasswords) for “Mail”.
4. Use the 16-character password as `GMAIL_APP_PASSWORD` (you may quote it if it contains spaces in shell commands).

Never commit these values to git.

## 7. Deploy from the repository root

The `Dockerfile` must be at the root; build context is `.`.

```bash
cd /path/to/IntentOS
```

Set variables for the deploy command (example — use your real values):

```bash
export GEMINI_API_KEY="your-gemini-key"
export MAPS_API_KEY="your-maps-key"
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

Deploy:

```bash
gcloud run deploy intent-os \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY},MAPS_API_KEY=${MAPS_API_KEY},GMAIL_USER=${GMAIL_USER},GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}" \
  --quiet
```

Notes:

- `--source .` builds with Cloud Build using the root `Dockerfile`.
- For passwords with special characters, prefer storing secrets in [Secret Manager](https://cloud.google.com/secret-manager) and wiring them to Cloud Run; the above is the minimal env-var approach.
- To require authentication, drop `--allow-unauthenticated` and configure IAM invokers.

## 8. After deploy

Get the service URL:

```bash
gcloud run services describe intent-os --region us-central1 --format='value(status.url)'
```

Update env vars without redeploying from source:

```bash
gcloud run services update intent-os \
  --region us-central1 \
  --set-env-vars "GEMINI_API_KEY=NEW_VALUE"
```

## 9. Google Sign-In (GIS) client ID

The frontend embeds a Google Identity **client ID** in `src/frontend/index.html`. For production, ensure the OAuth client’s **Authorized JavaScript origins** include your Cloud Run URL (e.g. `https://YOUR-SERVICE-xxxxx.run.app`). Create or adjust the client under **APIs & Services** → **Credentials** → **OAuth 2.0 Client IDs**.
