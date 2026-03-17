# CareerCraft AI

CareerCraft AI is a full-stack career exploration system that collects rich questionnaire signals and produces explainable career recommendations. It supports a database-backed catalog and a free external fallback (Open Skills API) for uncertain scenarios.

## Stack
- Frontend: HTML + CSS + Vanilla JS
- Backend: Flask + Flask-SQLAlchemy
- Database: PostgreSQL
- External fallback: Open Skills API (DataAtWork)

## Project Structure
- `frontend/` - UI, questionnaire flow, scoring, and results
- `backend/` - Flask API, DB models, catalog service, external fallback
- `sql.txt` - Database schema
- `backend/scripts/seed_catalog.py` - Seeds the catalog into Postgres

## Prerequisites
- Python 3.10+
- PostgreSQL 13+
- `pip` in PATH

## 1) Database Setup
Create the database (skip if it already exists):
```bash
psql -U postgres -c "CREATE DATABASE careercraft_ai;"
```

Apply the schema:
```bash
psql -U postgres -d careercraft_ai -f "sql.txt"
```

## One-Command Setup (Windows PowerShell)
```powershell
.\scripts\setup.ps1
```

## 2) Backend Setup
Install dependencies:
```bash
pip install -r "backend/requirements.txt"
```

Update connection string if needed:
- `backend/config.py`

Seed the catalog:
```bash
python "backend/scripts/seed_catalog.py"
```

Start the backend:
```bash
python "backend/app.py"
```

## 3) Frontend Setup
Open the app directly:
```text
frontend/index.html
```

If you want a local server:
```bash
python -m http.server 8080 --directory frontend
```

Then visit:
```text
http://localhost:8080
```

## External Fallback
When internal matching is uncertain, the UI calls:
- `GET /external/suggest?q=...`

This uses the Open Skills API to fetch:
- Suggested job titles
- Related skills
- Related job families

## Common Troubleshooting
- If the backend can't connect to Postgres, confirm:
  - Host/port are correct in `backend/config.py`
  - The DB exists and the schema is applied
- If external fallback fails, check your internet connection

## Scripts
- Seed catalog: `backend/scripts/seed_catalog.py`
