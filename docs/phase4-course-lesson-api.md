# Phase 4 — Course dan Lesson API

## Endpoint yang tersedia

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/api/v1/courses` | Daftar course berstatus `PUBLISHED` dengan pagination |
| GET | `/api/v1/courses/{slug}` | Detail course, module, dan lesson yang published |
| GET | `/api/v1/lessons/{lesson_id}` | Detail lesson Markdown dan konteks course |

## Filter daftar course

Endpoint list menerima query berikut:

- `page`: nomor halaman mulai dari 1, default `1`.
- `page_size`: jumlah item 1–100, default `20`.
- `category`: filter berdasarkan slug category.
- `level`: `BEGINNER`, `INTERMEDIATE`, atau `ADVANCED`.
- `search`: pencarian pada judul course.

Contoh:

```text
GET /api/v1/courses?page=1&page_size=10&level=BEGINNER&search=digital
```

Response memakai envelope pagination `items`, `total`, `page`, `page_size`, dan `total_pages`.

## Visibility dan error

Course yang berstatus `DRAFT` atau `ARCHIVED` tidak dikembalikan pada endpoint publik. Lesson yang tidak published atau berada dalam course yang tidak published juga tidak dapat diakses. Kondisi resource tidak ditemukan memakai error envelope existing dengan HTTP `404` dan code `RESOURCE_NOT_FOUND`.

Authentication dan endpoint admin belum diterapkan karena model User/JWT belum tersedia. Endpoint create/update course dan lesson akan ditambahkan setelah Phase Authentication serta admin authorization siap.

## Verification

Unit test API, model, dan health: `13 passed`. Alembic offline generation juga berhasil untuk migration katalog.
