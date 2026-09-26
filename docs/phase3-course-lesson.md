# Phase 3 — Course & Lesson Database Foundation

## Scope

Phase ini menambahkan fondasi katalog pembelajaran:

- `categories`: pengelompokan course.
- `courses`: metadata course, status publikasi, dan level.
- `modules`: kelompok lesson berurutan di dalam course.
- `lessons`: konten Markdown berurutan di dalam module.

Authentication/user model belum tersedia pada source saat ini, sehingga `creator_id` pada rancangan awal ditunda sampai Phase Authentication/User dibuat. API admin dan endpoint publik juga tetap menjadi tahap berikutnya.

## Migration

Jalankan dari folder `backend`:

```powershell
alembic upgrade head
```

Untuk membatalkan migration terakhir:

```powershell
alembic downgrade -1
```

## Integrity rules

- UUID digunakan untuk primary key.
- `courses.slug` unik secara global.
- `courses.category_id` wajib dan `ON DELETE RESTRICT`.
- Module diurutkan unik berdasarkan `(course_id, order_index)`.
- Lesson diurutkan unik berdasarkan `(module_id, order_index)`.
- Slug lesson unik di dalam module berdasarkan `(module_id, slug)`.
- Penghapusan course menghapus module dan lesson turunannya melalui `ON DELETE CASCADE`.
- Level course dibatasi ke `BEGINNER`, `INTERMEDIATE`, atau `ADVANCED`.
- Status course dibatasi ke `DRAFT`, `PUBLISHED`, atau `ARCHIVED`.

## Verification

- Unit test katalog: `8 passed` bersama health tests.
- Alembic offline SQL berhasil dibuat untuk seluruh tabel dan constraint.
- PostgreSQL live tetap diperlukan untuk menjalankan migration terhadap database sebenarnya.
