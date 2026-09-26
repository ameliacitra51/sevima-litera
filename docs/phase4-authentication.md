# Phase 4 — User dan Authentication

## Endpoint

| Method | Endpoint | Access | Fungsi |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Public | Membuat akun Student |
| POST | `/api/v1/auth/login` | Public | Memvalidasi email/password dan mengeluarkan JWT |
| GET | `/api/v1/auth/me` | Bearer token | Mengambil profil user aktif |
| POST | `/api/v1/auth/logout` | Bearer token | Mengakhiri sesi stateless di sisi client |

## Keamanan

Password tidak pernah disimpan plaintext. Password di-hash menggunakan Argon2 melalui `pwdlib[argon2]`. Response user tidak pernah mengandung `password` atau `hashed_password`.

JWT membawa `sub` berupa UUID user, `iat`, dan `exp`. Token dikirim pada header:

```text
Authorization: Bearer <access_token>
```

Logout stateless meminta client menghapus token. Token blacklist belum diperlukan pada tahap ini; jika nanti dibutuhkan invalidasi server-side sebelum expiration, tambahkan storage revocation secara eksplisit.

## User model

Tabel `users` memiliki `email` dan `username` unik, role `STUDENT` atau `ADMIN`, status `is_active`, serta timestamp. Migration juga menambahkan `courses.creator_id` nullable dengan foreign key ke `users.id`. Kolom dibuat nullable agar aman saat migration diterapkan pada database yang sudah memiliki course lama; endpoint admin nantinya dapat mewajibkannya setelah data lama di-backfill.

## Environment

Ganti `SECRET_KEY` development dengan random secret minimal 32 karakter pada `backend/.env` sebelum digunakan di luar development:

```env
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Jangan commit file `.env`; gunakan `.env.example` sebagai template.

## Verification

Authentication, katalog API, model, dan health tests: `20 passed`. Alembic offline berhasil menghasilkan migration catalog kemudian users/creator relation.
