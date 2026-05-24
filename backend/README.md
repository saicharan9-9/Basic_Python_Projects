## StudyGenie Backend

### Setup

1. Create and activate a virtualenv (recommended)
2. Install requirements

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

### Environment

Create `.env` in `backend/` or set env vars:

- `OPENAI_API_KEY` required for LLM features
- `FAISS_DIR` default `/workspace/data/faiss`
- `DATABASE_URL` default SQLite at `/workspace/data/studygenie.db`