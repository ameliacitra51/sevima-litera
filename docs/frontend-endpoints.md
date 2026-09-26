# Frontend Endpoint Integration

Frontend sekarang terhubung ke seluruh endpoint backend yang tersedia pada Phase 3–4.

| Halaman | Endpoint |
|---|---|
| Home health status | `GET /api/v1/health` |
| Register | `POST /api/v1/auth/register` |
| Login | `POST /api/v1/auth/login` |
| Profile | `GET /api/v1/auth/me` |
| Logout | `POST /api/v1/auth/logout` |
| Course catalog | `GET /api/v1/courses` |
| Course detail | `GET /api/v1/courses/{slug}` |
| Lesson detail | `GET /api/v1/lessons/{lesson_id}` |

## Routes frontend

```text
/
/login
/register
/profile
/courses
/courses/:slug
/lessons/:lessonId
```

State server dikelola dengan TanStack Query. JWT disimpan di `localStorage` dengan key `litera_token`, lalu Axios request interceptor mengirimkannya sebagai Bearer token. Konten lesson Markdown dirender menggunakan `react-markdown`.

## Menjalankan frontend

```powershell
cd frontend
npm install
npm run dev
```

Pastikan backend aktif di `http://localhost:8000` dan `frontend/.env` berisi:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Data dummy

Jalankan seeder dari folder backend sebelum membuka halaman `/courses`:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
python scripts\seed_demo_data.py
```
