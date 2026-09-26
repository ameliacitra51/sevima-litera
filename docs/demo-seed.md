# Demo Seed Data

Seeder demo berada di `backend/scripts/seed_demo_data.py`. Seeder ini dijalankan setelah migration dan bersifat **idempotent**: menjalankannya berulang kali tidak menghapus data dan tidak menggandakan record berdasarkan email, slug, atau urutan module/lesson.

## Menjalankan di Windows PowerShell

```powershell
cd D:\litera\backend
.\.venv\Scripts\Activate.ps1
python scripts\seed_demo_data.py
```

Seeder akan membuat dua akun lokal, dua category, dua course published, empat module, dan delapan lesson jika record tersebut belum ada.

## Akun demo default

```text
Admin:   admin@litera.local / Admin12345!
Student: student@litera.local / Student12345!
```

Credential tersebut hanya untuk development lokal. Ganti dengan environment variable jika perlu:

```powershell
$env:LITERA_DEMO_ADMIN_PASSWORD = "password-lokal-anda"
$env:LITERA_DEMO_STUDENT_PASSWORD = "password-lokal-student"
python scripts\seed_demo_data.py
```

Seeder tidak menjalankan `DROP`, tidak menghapus tabel, dan tidak mengganti password user yang sudah ada. Untuk database yang sudah memiliki data dengan slug/email sama, record existing akan dipakai.

## Prasyarat

Jalankan migration terlebih dahulu:

```powershell
alembic upgrade head
```

Pastikan PostgreSQL berjalan dan `DATABASE_URL` di `backend/.env` mengarah ke database `litera`.
