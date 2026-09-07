# NAC API

Lightweight FastAPI service that exposes a model-based encoder from `encoder/encoders.joblib`.

## Requirements

- Python 3.10+ (3.11 recommended)
- See `requirements.txt` for exact packages

## Quick start (local)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn main:app --reload
```

3. Health check:

- `GET /health` — lightweight liveness check (HTTP 200)
- `GET /ready` — optional readiness check (verifies model file presence)

## Model files

The encoder is expected at `encoder/encoders.joblib`. If the file is large avoid committing it and instead download it at startup from cloud storage (S3, GCS) and add the relevant credentials to environment variables.

## Deploying to Render

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Set Render health check path to `/health` and expect `200`

Optional: include a `render.yaml` or `Dockerfile` for infra-as-code or container deployments. See the repo root for examples.

## Monitoring

Use UptimeRobot or similar to monitor `https://<your-service>.onrender.com/health`.

## Notes

- Keep `/health` unauthenticated and fast.
- Use `/ready` for slow readiness checks (model downloads, DB migrations).

Feel free to edit this file to add contributor notes, license, or more run examples.
