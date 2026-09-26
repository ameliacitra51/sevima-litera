# Phase 5b — Admin Catalog API

Phase ini menambahkan pengelolaan catalog oleh user dengan role `ADMIN`.

## Authorization

Semua endpoint di bawah membutuhkan:

```text
Authorization: Bearer <admin_access_token>
```

User `STUDENT` akan menerima `403 FORBIDDEN`.

## Endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/api/v1/admin/categories` | Daftar category |
| POST | `/api/v1/admin/categories` | Membuat category |
| PATCH | `/api/v1/admin/categories/{id}` | Mengubah category |
| GET | `/api/v1/admin/courses` | Daftar semua course termasuk draft |
| POST | `/api/v1/admin/courses` | Membuat course |
| PATCH | `/api/v1/admin/courses/{id}` | Mengubah course |
| DELETE | `/api/v1/admin/courses/{id}` | Menghapus course beserta module/lesson turunannya |
| POST | `/api/v1/admin/courses/{id}/modules` | Membuat module |
| PATCH | `/api/v1/admin/modules/{id}` | Mengubah module |
| DELETE | `/api/v1/admin/modules/{id}` | Menghapus module beserta lesson |
| POST | `/api/v1/admin/modules/{id}/lessons` | Membuat lesson Markdown |
| PATCH | `/api/v1/admin/lessons/{id}` | Mengubah lesson |
| DELETE | `/api/v1/admin/lessons/{id}` | Menghapus lesson |

Slug menggunakan format lowercase kebab-case. `order_index` harus unik dalam parent-nya; database conflict dikembalikan sebagai `409 RESOURCE_CONFLICT`.

## Contoh membuat course

```json
{
  "category_id": "<category-uuid>",
  "title": "Digital Safety Essentials",
  "slug": "digital-safety-essentials",
  "description": "Learn practical habits for safer accounts and devices.",
  "level": "BEGINNER",
  "status": "DRAFT"
}
```

## Verification

Admin authorization, payload validation, route registration, authentication, public catalog, model, dan health tests: **25 passed**.

Frontend public catalog dan Admin Dashboard sudah tersedia pada route `/admin`. Admin dapat membuat course, menambah module, menambah lesson Markdown, mengubah judul, dan menghapus resource. Endpoint backend juga tersedia dari Swagger di `/api/v1/docs`.
