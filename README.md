# AstraAI Final

AstraAI project workspace with a React + TypeScript + Vite frontend and a FastAPI + SQLite backend. Published project cards include **Preview website** and **Project details** actions.

## Requirements
- Python 3.10 or newer
- Node.js 20 or newer and npm

## Start the backend (PowerShell terminal 1)
```powershell
cd ".\backend"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Backend health check: http://127.0.0.1:8000/api/health
API docs: http://127.0.0.1:8000/docs

## Start the frontend (PowerShell terminal 2)
Open a second terminal at the extracted project folder, then run:
```powershell
cd ".\frontend"
npm install
npm run dev
```
Open the local URL printed by Vite (normally http://localhost:5173). Keep both terminals running.

Client requests and website projects are stored in the local SQLite database `backend/app/astraai.db`. The website preview is a local generated preview, not a publicly hosted website.
