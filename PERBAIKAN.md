# Catatan Perbaikan LITERA

Perbaikan yang sudah diterapkan:

1. Menghapus `baseUrl` yang deprecated dari `frontend/tsconfig.json`.
2. Mengubah alias TypeScript menjadi target relatif:
   `@/*` → `./src/*`.
3. Mengeluarkan `.venv`, `node_modules`, `dist`, cache, `.git`, dan file `.env` dari paket.
4. Dependensi frontend harus dipasang ulang sesuai `package-lock.json` pada komputer tujuan.

## Menjalankan frontend

```powershell
cd frontend
npm install
npm run dev
```

Untuk production build:

```powershell
npm install
npm run build
```

## Menjalankan backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

Pastikan PostgreSQL berjalan di `localhost:5432`, database `litera` sudah dibuat, dan nilai `DATABASE_URL` di `.env` sudah benar sebelum menjalankan test database.
