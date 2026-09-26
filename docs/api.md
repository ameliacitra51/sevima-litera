# LITERA — REST API Specification & Contract

## 1. API Architecture & Standards

* **Base URL**: `http://localhost:8000/api/v1`
* **Protocol**: HTTP/1.1 (JSON request and response bodies)
* **Authentication**: Bearer Token in `Authorization` header (`Authorization: Bearer <JWT>`)
* **Date & Time Format**: ISO 8601 UTC string (`YYYY-MM-DDTHH:MM:SSZ`)

### 1.1 Standard HTTP Status Codes
* `200 OK`: Request succeeded; returns resource or collection.
* `201 Created`: Resource successfully created.
* `204 No Content`: Action succeeded; empty body (e.g. DELETE, toggle like).
* `400 Bad Request`: Malformed payload or validation error.
* `401 Unauthorized`: Missing, invalid, or expired JWT token.
* `403 Forbidden`: Authenticated user lacks required role (e.g., student calling admin route).
* `404 Not Found`: Target resource does not exist.
* `409 Conflict`: Unique constraint violation (e.g. duplicate email, slug conflict).
* `422 Unprocessable Entity`: Pydantic schema validation failure.
* `500 Internal Server Error`: Unhandled server exception.

### 1.2 Standard Response Envelopes

#### Paginated Collection Response
```json
{
  "items": [],
  "total": 120,
  "page": 1,
  "page_size": 20,
  "total_pages": 6
}
```

#### Standard Error Response
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested course slug 'digital-safety-101' was not found",
    "details": []
  }
}
```

---

## 2. API Endpoint Inventory

### 2.1 Authentication (`/auth`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Public | Register a new student account |
| `POST` | `/auth/login` | Public | Authenticate with credentials and receive JWT |
| `POST` | `/auth/logout` | Authenticated | Terminate session / invalidate client token |
| `GET` | `/auth/me` | Authenticated | Retrieve current user profile and role |

#### `POST /auth/register`
* **Request**:
  ```json
  {
    "email": "student@example.com",
    "username": "learning_pilot",
    "full_name": "Citra Amalia",
    "password": "SecurePassword123!"
  }
  ```
* **Response (201 Created)**:
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "student@example.com",
    "username": "learning_pilot",
    "full_name": "Citra Amalia",
    "role": "STUDENT",
    "created_at": "2026-09-26T10:00:00Z"
  }
  ```

#### `POST /auth/login`
* **Request**:
  ```json
  {
    "email": "student@example.com",
    "password": "SecurePassword123!"
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "student@example.com",
      "username": "learning_pilot",
      "full_name": "Citra Amalia",
      "role": "STUDENT"
    }
  }
  ```

---

### 2.2 Users & Profile (`/users`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/users/profile` | Authenticated | Get current authenticated user details |
| `PUT` | `/users/profile` | Authenticated | Update user full_name or preferences |
| `PUT` | `/users/password` | Authenticated | Change user password (verifies old password) |

---

### 2.3 Categories (`/categories`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/categories` | Public | List all categories with course count |
| `GET` | `/categories/{slug}` | Public | Get single category and its published courses |

---

### 2.4 Courses & Enrollment (`/courses`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/courses` | Public | Search/filter courses (`category`, `level`, `search`, `page`, `page_size`) |
| `GET` | `/courses/{slug}` | Public | Course detail, syllabus overview, and enrollment status |
| `POST` | `/courses/{id}/enroll` | Student | Enroll current student into course |
| `GET` | `/courses/{id}/progress` | Student | Get course completion percentage and completed lesson IDs |

#### `GET /courses/{slug}` Response (200 OK)
```json
{
  "id": "8f3b6c2a-9e12-4f3b-b789-0123456789ab",
  "title": "Critical Thinking in the AI Era",
  "slug": "critical-thinking-in-the-ai-era",
  "description": "Learn to critically evaluate digital media and AI outputs.",
  "thumbnail_url": "/assets/thumbnails/critical-thinking.webp",
  "level": "BEGINNER",
  "category": {
    "id": "111e8400-e29b-41d4-a716-446655440001",
    "name": "Critical Thinking",
    "slug": "critical-thinking"
  },
  "modules": [
    {
      "id": "222e8400-e29b-41d4-a716-446655440002",
      "title": "Module 1: Detecting Cognitive Bias",
      "order_index": 1,
      "lessons": [
        {
          "id": "333e8400-e29b-41d4-a716-446655440003",
          "title": "Confirmation Bias in Search Algorithms",
          "slug": "confirmation-bias-search",
          "order_index": 1,
          "duration_minutes": 7,
          "has_quiz": true
        }
      ]
    }
  ],
  "is_enrolled": true,
  "progress_percentage": 25.0
}
```

---

### 2.5 Lessons & Progress (`/lessons`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/lessons/{id}` | Student | Retrieve lesson content (Markdown), navigation context, and quiz info |
| `POST` | `/lessons/{id}/complete` | Student | Toggle or mark lesson as completed |
| `POST` | `/lessons/{id}/bookmark` | Student | Add lesson to bookmarks |
| `DELETE` | `/lessons/{id}/bookmark` | Student | Remove lesson from bookmarks |

---

### 2.6 Quizzes & Scoring (`/quizzes`)

#### Core Security Invariant: Answer Secrecy
When a student requests a quiz via `GET /quizzes/{id}`, the backend **MUST NEVER** include `is_correct` in the response options.

#### `GET /quizzes/{id}`
* **Access**: Authenticated Student / Admin
* **Response (200 OK)**:
```json
{
  "id": "444e8400-e29b-41d4-a716-446655440004",
  "lesson_id": "333e8400-e29b-41d4-a716-446655440003",
  "title": "Check Your Understanding: Confirmation Bias",
  "description": "Answer all questions to complete the module checkpoint.",
  "passing_score": 70,
  "time_limit_minutes": 10,
  "questions": [
    {
      "id": "555e8400-e29b-41d4-a716-446655440005",
      "question_type": "MULTIPLE_CHOICE",
      "prompt": "What is confirmation bias?",
      "points": 10,
      "order_index": 1,
      "options": [
        {
          "id": "666e8400-e29b-41d4-a716-446655440006",
          "option_text": "Seeking information that validates pre-existing beliefs",
          "order_index": 1
        },
        {
          "id": "666e8400-e29b-41d4-a716-446655440007",
          "option_text": "Rejecting all forms of digital communication",
          "order_index": 2
        }
      ]
    }
  ]
}
```

#### `POST /quizzes/{id}/attempts` (Submit Quiz)
* **Access**: Authenticated Student
* **Request**:
```json
{
  "answers": [
    {
      "question_id": "555e8400-e29b-41d4-a716-446655440005",
      "selected_option_id": "666e8400-e29b-41d4-a716-446655440006"
    }
  ]
}
```
* **Response (201 Created)**:
```json
{
  "attempt_id": "777e8400-e29b-41d4-a716-446655440007",
  "quiz_id": "444e8400-e29b-41d4-a716-446655440004",
  "score": 10,
  "max_score": 10,
  "percentage": 100.0,
  "is_passed": true,
  "passing_score": 70,
  "completed_at": "2026-09-26T10:15:00Z",
  "results": [
    {
      "question_id": "555e8400-e29b-41d4-a716-446655440005",
      "selected_option_id": "666e8400-e29b-41d4-a716-446655440006",
      "correct_option_id": "666e8400-e29b-41d4-a716-446655440006",
      "is_correct": true,
      "points_awarded": 10,
      "explanation": "Confirmation bias leads individuals to prioritize information confirming their prior beliefs."
    }
  ]
}
```

#### `GET /quizzes/attempts/{attempt_id}`
* **Access**: Authenticated Student (own attempt) / Admin
* Returns previously submitted attempt summary and question reviews.

---

### 2.7 Community Discussions & Comments (`/discussions`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/discussions` | Public / Auth | List discussions (`course_id`, `search`, `sort`, `page`) |
| `POST` | `/discussions` | Student / Admin | Create a new discussion thread |
| `GET` | `/discussions/{id}` | Public / Auth | Read discussion and its comments |
| `PUT` | `/discussions/{id}` | Author / Admin | Edit discussion title or body |
| `DELETE` | `/discussions/{id}` | Author / Admin | Delete discussion |
| `POST` | `/discussions/{id}/like` | Student / Admin | Toggle like / upvote on discussion |
| `POST` | `/discussions/{id}/comments`| Student / Admin | Post reply to discussion (optional `parent_id`) |
| `DELETE` | `/comments/{id}` | Author / Admin | Delete specific comment |

---

### 2.8 Student Dashboard (`/student`)

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/student/dashboard` | Student | Overview stats: in-progress courses, recent lessons, quiz stats |
| `GET` | `/student/bookmarks` | Student | Paginated list of student's bookmarked lessons |
| `GET` | `/student/achievements`| Student | Badges earned by student and upcoming milestones |

---

### 2.9 Admin Control Plane (`/admin`)

All `/admin/*` routes require `role == 'ADMIN'`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/admin/analytics` | High-level metrics: user count, course enrollments, quiz pass-rates |
| `POST` | `/admin/categories` | Create category |
| `PUT` | `/admin/categories/{id}` | Update category |
| `DELETE`| `/admin/categories/{id}` | Delete category |
| `POST` | `/admin/courses` | Create new course (DRAFT) |
| `PUT` | `/admin/courses/{id}` | Edit course metadata |
| `PUT` | `/admin/courses/{id}/status` | Publish / Archive course |
| `POST` | `/admin/courses/{id}/modules` | Add module to course |
| `PUT` | `/admin/modules/{id}` | Edit module title / reorder |
| `DELETE`| `/admin/modules/{id}` | Delete module |
| `POST` | `/admin/modules/{id}/lessons` | Create lesson |
| `PUT` | `/admin/lessons/{id}` | Edit lesson markdown content |
| `POST` | `/admin/lessons/{id}/quiz` | Create / attach quiz to lesson |
| `POST` | `/admin/quizzes/{id}/questions` | Add question with options & specify `is_correct` |
| `PUT` | `/admin/questions/{id}` | Edit question and options |
| `GET` | `/admin/users` | Paginated user management table |
| `PUT` | `/admin/users/{id}/role` | Update user role (`STUDENT` <-> `ADMIN`) |
| `PUT` | `/admin/users/{id}/status` | Activate / suspend user account |
