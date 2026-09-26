# LITERA — Digital Literacy & Learning Platform

LITERA is a modern digital literacy and educational platform designed for high-school and university students. The platform provides curriculum-aligned courses, modules, lessons, quizzes, learning progress tracking, bookmarks, achievements, and community discussions.

---

## 🏗️ Architecture & Technology Stack

* **Frontend**: React 18, Vite, TypeScript (Strict), Tailwind CSS, React Router v6, TanStack Query v5, Axios
* **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2
* **Database**: PostgreSQL 15+ (Local native instance, port 5432)
* **Authentication**: Stateless JWT + Argon2id password hashing (Phase 4)
* **Environment**: Native Windows development (PowerShell, no Docker)

---

## 📁 Repository Structure

```
litera/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/v1/           # Versioned REST endpoints (health, etc.)
│   │   ├── core/             # Settings, security, exceptions, dependencies
│   │   ├── models/           # SQLAlchemy ORM models (Phase 3)
│   │   ├── schemas/          # Pydantic v2 schemas
│   │   ├── services/         # Encapsulated business logic
│   │   ├── config.py         # Application configuration & .env loader
│   │   └── main.py           # FastAPI application entrypoint & CORS
│   ├── tests/                # Pytest suite
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/                 # React SPA (Vite + TypeScript)
│   ├── src/
│   │   ├── components/       # Layout & UI components
│   │   ├── pages/            # Application views (Home, etc.)
│   │   ├── routes/           # React Router route configuration
│   │   ├── services/         # Axios API clients & TanStack Query fetchers
│   │   ├── types/            # TypeScript domain interfaces
│   │   ├── App.tsx           # Application layout shell
│   │   ├── main.tsx          # React DOM entrypoint & QueryClientProvider
│   │   └── index.css         # Tailwind CSS directives
│   ├── package.json          # Node dependencies & build scripts
│   ├── vite.config.ts        # Vite configuration
│   └── tailwind.config.js    # Tailwind styling configuration
├── docs/                     # Architectural & Engineering Documentation
│   ├── architecture.md       # High-level architecture & RBAC model
│   ├── database.md           # Database schemas, ERD, and constraints
│   ├── api.md                # REST API contract & endpoints specification
│   └── development.md        # Windows local environment setup guide
├── .gitignore                # Global Git ignore rules
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start (Native Windows PowerShell)

### 1. Backend Setup

Open a Windows PowerShell terminal:

```powershell
# Navigate to backend
cd d:\litera\backend

# Initialize virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create .env from template (if not already present)
Copy-Item .env.example .env

# Run FastAPI development server
uvicorn app.main:app --reload --port 8000
```

* **Interactive API Documentation (Swagger)**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
* **Alternative API Documentation (ReDoc)**: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
* **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### 2. Frontend Setup

Open a second Windows PowerShell terminal:

```powershell
# Navigate to frontend
cd d:\litera\frontend

# Install dependencies
npm install

# Create .env from template (if not already present)
Copy-Item .env.example .env

# Run Vite development server
npm run dev
```

* **Web Application**: [http://localhost:5173](http://localhost:5173)

---

## 📖 Detailed Documentation

* [docs/architecture.md](docs/architecture.md) — System architecture, client-server data flow, RBAC, and AI sandbox.
* [docs/database.md](docs/database.md) — Complete ERD diagram and 18 entity schemas.
* [docs/api.md](docs/api.md) — RESTful endpoints inventory and payload contracts.
* [docs/development.md](docs/development.md) — Windows setup, PostgreSQL installation, and development guidelines.

---

## 🚦 Phase Roadmap

* [x] **Phase 0**: Master Project Context
* [x] **Phase 1**: Architecture & ERD Planning
* [x] **Phase 2**: Project Foundation (FastAPI + React Vite TS + Tailwind + TanStack Query)
* [ ] **Phase 3**: Database & Migrations
* [ ] **Phase 4**: Authentication & RBAC
* [ ] **Phase 5**: Courses & Lessons
* [ ] **Phase 6**: Progress Tracking
* [ ] **Phase 7**: Quizzes & Scoring
* [ ] **Phase 8**: Student Dashboard
* [ ] **Phase 9**: Community Discussions & Likes
* [ ] **Phase 10**: Admin Management & Analytics
* [ ] **Phase 11**: Testing & Refactoring
* [ ] **Phase 12**: AI Layer (Optional Auxiliary Service)
* [ ] **Phase 13**: Final Audit & Production Readiness
