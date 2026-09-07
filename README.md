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

3. Health and readiness:

- `GET /health` — lightweight liveness check (HTTP 200)
- `GET /ready` — readiness check (verifies model file presence)

## Usage

Example: encode a sample payload (adjust to your API paths in `main.py`):

```bash
curl -X POST https://<your-host>/encode \
	-H "Content-Type: application/json" \
	-d '{"text": "sample input"}'
```

Example JSON response:

```json
{
	"encoded": [0.12, -0.03, 0.97]
}
```

Replace `/encode` and the payload shape with the actual endpoints and input your `main.py` exposes.

## API Endpoints (suggested)

- `GET /health` — returns 200 when process is up
- `GET /ready` — returns 200 when model files are available
- `POST /encode` — example encoding endpoint (adjust name and payload)

Add authentication only to non-health endpoints. Keep `/health` and `/ready` unauthenticated so external monitors can access them.

## Test data

- Small sample inputs for manual testing: create a local `test_data/` directory and add `sample1.json` with example request bodies.
- If you need public datasets for testing, consider using:
	- Kaggle sample text datasets (https://www.kaggle.com)
	- The "SMS Spam Collection" or small text CSVs for quick throughput tests

To create a minimal `test_data/sample1.json`:

```json
{
	"text": "This is a test input to validate the encoder."
}
```

Load and send it via curl:

```bash
curl -X POST https://<your-host>/encode \
	-H "Content-Type: application/json" \
	-d @test_data/sample1.json
```

## Model files

The encoder is expected at `encoder/encoders.joblib`. If the file is large avoid committing it and instead download it at startup from cloud storage (S3, GCS) and add the relevant credentials to environment variables. Example startup-snippet:

```python
import os
def ensure_model():
		if not os.path.exists("encoder/encoders.joblib"):
				# download from S3/GCS here
				pass
ensure_model()
```

## Deploying to Render

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Set Render health check path to `/health` and expect `200`

Optional: include a `render.yaml` or `Dockerfile` for infra-as-code or container deployments.

## Monitoring

Use UptimeRobot or similar to monitor `https://<your-service>.onrender.com/health`.

## Notes

- Keep `/health` unauthenticated and fast.
- Use `/ready` for slow readiness checks (model downloads, DB migrations).

Contributions, license, and more examples are welcome—edit this file as needed.
