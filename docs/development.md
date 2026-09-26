# LITERA — Local Development & Environment Guide

## 1. Prerequisites (Native Windows Setup)

LITERA is developed natively on Windows without Docker or Docker Compose. Ensure the following tools are installed:

* **OS**: Windows 10 / 11 (64-bit)
* **Shell**: Windows PowerShell (Run as Administrator for initial tool setups if required)
* **Python**: Version 3.11+ (ensure `python` is added to Windows PATH)
* **Node.js**: Version 18.x or 20.x LTS (with npm)
* **PostgreSQL**: Version 15+ installed natively via the official Windows installer
* **Git**: Installed and configured for Windows (`core.autocrlf=true`)
* **API Testing Tool**: Postman, Bruno, or curl

---

## 2. PostgreSQL Setup

1. **Start PostgreSQL Service**:
   Ensure the `postgresql-x64-<version>` service is running in Windows Services (`services.msc`), or execute in PowerShell:
   ```powershell
   Get-Service postgresql*
   ```

2. **Create Database**:
   Open PowerShell or `psql` and create the `litera` database:
   ```powershell
   # Using psql command line
   psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE litera;"
   ```

---

## 3. Backend Setup Walkthrough

### 3.1 Initialize Virtual Environment
From the repository root (`d:\litera`):
```powershell
# Navigate to backend
cd d:\litera\backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (once requirements.txt is provided in Phase 2)
pip install -r requirements.txt
```

> **Note on PowerShell Execution Policy**: If you encounter `PSSecurityException`, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3.2 Configure Backend Environment Variables
Create `.env` inside `backend/` copied from `.env.example`:
```env
# Server
ENVIRONMENT=development
PORT=8000
DEBUG=True

# Database (PostgreSQL)
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/litera

# Security & JWT
SECRET_KEY=generate_a_secure_random_64_char_hex_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]
```

### 3.3 Apply Database Migrations
```powershell
alembic upgrade head
```

### 3.4 Launch FastAPI Development Server
```powershell
uvicorn app.main:app --reload --port 8000
```
* **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
* **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`

---

## 4. Frontend Setup Walkthrough

### 4.1 Install Node Dependencies
Open a second PowerShell terminal:
```powershell
# Navigate to frontend
cd d:\litera\frontend

# Install node dependencies
npm install
```

### 4.2 Configure Frontend Environment Variables
Create `.env` inside `frontend/`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 4.3 Launch Vite Development Server
```powershell
npm run dev
```
* **Local Web Application**: `http://localhost:5173`

---

## 5. Development Invariants & Engineering Rules

1. **Windows Native Command Rule**: Never run Unix-specific tools like `grep`, `awk`, or `cat` in PowerShell instructions without cross-platform compatibility. Prefer PowerShell cmdlets (`Select-String`, `Get-Content`, `Get-ChildItem`).
2. **Database Integrity**: Never modify the database schema via raw manual SQL edits. Always generate an Alembic migration (`alembic revision --autogenerate -m "description"`), review the generated migration file, and apply via `alembic upgrade head`.
3. **No Unapproved Frameworks**: Adhere strictly to the chosen stack:
   * Frontend: React, Vite, TypeScript, Tailwind CSS, React Router, TanStack Query, Axios, React Hook Form, Zod.
   * Backend: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Argon2 (`pwdlib` or `argon2-cffi`), PyJWT.
4. **Git Discipline**:
   * Never commit `.env` or sensitive credentials.
   * Keep `.gitignore` updated for `.venv/`, `node_modules/`, `__pycache__/`, `.dist/`.
   * Commit after each completed phase with clear descriptive messages.
5. **No AI Before Phase 12**: AI modules or dependencies (e.g. `google-genai`) must not be installed or called in earlier phases.
