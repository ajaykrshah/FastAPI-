# FastAPI PDM/Azure/GitHub Service

Production-ready FastAPI service targeting Windows 11 deployment with:
- Real-time GitHub script listing (private repo, PAT) via Git Trees API (no DB storage).
- Shared Basic Auth PDM proxy across multiple base URLs.
- Long-running Azure DevOps Pipelines orchestration with polling + optional SSE.
- Postgres with lean tables + JSONB metadata.
- JSON logs with RotatingFileHandler. Correlation IDs.

## Quickstart (Windows-friendly)

```powershell
# Python 3.11+
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -e ".[dev]"

copy .env.example .env
# edit .env with real credentials

# Initialize DB (optional if DB_CREATE_IF_MISSING=true)
psql < sql/init_database.sql

# Alembic
alembic upgrade head

# Run API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run worker (separate terminal)
python -m app.workers.runner
```

## Endpoints
- `GET /api/v1/scripts?prefix=&pattern=*.py&page=1&pageSize=100`
- `POST /api/v1/pdm/call`
- `POST /api/v1/pipelines/run`
- `GET /api/v1/pipelines/status/{runId}`
- `GET /api/v1/pipelines/stream/{runId}` (SSE)
- `GET /api/v1/products`, CRUD
- `POST /api/v1/products/{id}/run`
- `GET /api/v1/dashboard`

See `sql/init_database.sql` and Alembic migrations for schema.
