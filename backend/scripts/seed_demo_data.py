"""Seed local demo data for LITERA.

This script is intentionally separate from Alembic migrations: demo content is
optional and can be inserted into an already migrated development database.
It is idempotent and never deletes existing records.

Run from backend/:
    python scripts/seed_demo_data.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow `python scripts/seed_demo_data.py` to import the backend app package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import Category, Course, CourseLevel, CourseStatus, Lesson, Module, User, UserRole


ADMIN_EMAIL = os.getenv("LITERA_DEMO_ADMIN_EMAIL", "admin@litera.local")
ADMIN_USERNAME = os.getenv("LITERA_DEMO_ADMIN_USERNAME", "admin_demo")
ADMIN_PASSWORD = os.getenv("LITERA_DEMO_ADMIN_PASSWORD", "Admin12345!")
STUDENT_EMAIL = os.getenv("LITERA_DEMO_STUDENT_EMAIL", "student@litera.local")
STUDENT_USERNAME = os.getenv("LITERA_DEMO_STUDENT_USERNAME", "student_demo")
STUDENT_PASSWORD = os.getenv("LITERA_DEMO_STUDENT_PASSWORD", "Student12345!")


def get_or_create_user(
    db: Session,
    *,
    email: str,
    username: str,
    full_name: str,
    password: str,
    role: UserRole,
) -> tuple[User, bool]:
    user = db.scalar(select(User).where(User.email == email))
    if user is not None:
        return user, False

    user = User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=hash_password(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user, True


def get_or_create_category(
    db: Session, *, name: str, slug: str, description: str, order_index: int
) -> tuple[Category, bool]:
    category = db.scalar(select(Category).where(Category.slug == slug))
    if category is not None:
        return category, False

    category = Category(
        name=name,
        slug=slug,
        description=description,
        order_index=order_index,
    )
    db.add(category)
    db.flush()
    return category, True


def get_or_create_course(
    db: Session,
    *,
    category: Category,
    creator: User,
    title: str,
    slug: str,
    description: str,
    level: CourseLevel,
) -> tuple[Course, bool]:
    course = db.scalar(select(Course).where(Course.slug == slug))
    if course is not None:
        return course, False

    course = Course(
        category=category,
        creator=creator,
        title=title,
        slug=slug,
        description=description,
        level=level,
        status=CourseStatus.PUBLISHED,
    )
    db.add(course)
    db.flush()
    return course, True


def get_or_create_module(
    db: Session, *, course: Course, title: str, description: str, order_index: int
) -> tuple[Module, bool]:
    module = db.scalar(
        select(Module).where(
            Module.course_id == course.id,
            Module.order_index == order_index,
        )
    )
    if module is not None:
        return module, False

    module = Module(
        course=course,
        title=title,
        description=description,
        order_index=order_index,
    )
    db.add(module)
    db.flush()
    return module, True


def get_or_create_lesson(
    db: Session,
    *,
    module: Module,
    title: str,
    slug: str,
    content: str,
    order_index: int,
    duration_minutes: int,
) -> tuple[Lesson, bool]:
    lesson = db.scalar(
        select(Lesson).where(
            Lesson.module_id == module.id,
            Lesson.slug == slug,
        )
    )
    if lesson is not None:
        return lesson, False

    lesson = Lesson(
        module=module,
        title=title,
        slug=slug,
        content=content,
        order_index=order_index,
        duration_minutes=duration_minutes,
        is_published=True,
    )
    db.add(lesson)
    db.flush()
    return lesson, True


def seed_demo_data() -> dict[str, int]:
    """Insert the local demo dataset and return created-record counts."""
    counts = {"users": 0, "categories": 0, "courses": 0, "modules": 0, "lessons": 0}
    db = SessionLocal()
    try:
        admin, created = get_or_create_user(
            db,
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            full_name="LITERA Demo Admin",
            password=ADMIN_PASSWORD,
            role=UserRole.ADMIN,
        )
        counts["users"] += int(created)
        _, created = get_or_create_user(
            db,
            email=STUDENT_EMAIL,
            username=STUDENT_USERNAME,
            full_name="LITERA Demo Student",
            password=STUDENT_PASSWORD,
            role=UserRole.STUDENT,
        )
        counts["users"] += int(created)

        digital, created = get_or_create_category(
            db,
            name="Digital Literacy",
            slug="digital-literacy",
            description="Fundamental skills for safe and effective digital life.",
            order_index=1,
        )
        counts["categories"] += int(created)
        critical, created = get_or_create_category(
            db,
            name="Critical Thinking",
            slug="critical-thinking",
            description="Reasoning skills for evaluating information and claims.",
            order_index=2,
        )
        counts["categories"] += int(created)

        courses = [
            (digital, "Digital Safety Essentials", "digital-safety-essentials", "Learn practical habits for safer accounts, devices, and online communication.", CourseLevel.BEGINNER),
            (critical, "Critical Thinking in the AI Era", "critical-thinking-ai-era", "Practice evaluating claims, sources, and AI-generated information.", CourseLevel.INTERMEDIATE),
        ]
        for category, title, slug, description, level in courses:
            course, created = get_or_create_course(
                db,
                category=category,
                creator=admin,
                title=title,
                slug=slug,
                description=description,
                level=level,
            )
            counts["courses"] += int(created)

            module_specs = [
                (1, "Foundations", "Core concepts and simple habits."),
                (2, "Practical Application", "Apply the ideas to everyday scenarios."),
            ]
            for module_order, module_title, module_description in module_specs:
                module, created = get_or_create_module(
                    db,
                    course=course,
                    title=module_title,
                    description=module_description,
                    order_index=module_order,
                )
                counts["modules"] += int(created)
                lesson_specs = [
                    (1, f"{slug}-intro", f"Introduction to {module_title}", f"# {module_title}\n\nThis demo lesson introduces the key ideas for **{title}**.\n", 7),
                    (2, f"{slug}-practice", "Practice and Reflection", "# Practice\n\nReview the concept, apply it to a real example, and write one reflection.\n", 10),
                ]
                for lesson_order, lesson_slug, lesson_title, content, duration in lesson_specs:
                    _, created = get_or_create_lesson(
                        db,
                        module=module,
                        title=lesson_title,
                        slug=lesson_slug,
                        content=content,
                        order_index=lesson_order,
                        duration_minutes=duration,
                    )
                    counts["lessons"] += int(created)

        db.commit()
        return counts
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    counts = seed_demo_data()
    print(f"Seed completed using database: {settings.DATABASE_URL.split('@')[-1]}")
    print("Created records:")
    for resource, count in counts.items():
        print(f"  {resource}: {count}")
    print("\nDemo login credentials (local development only):")
    print(f"  Admin:   {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"  Student: {STUDENT_EMAIL} / {STUDENT_PASSWORD}")
    print("Change these values with LITERA_DEMO_* environment variables before sharing a database.")


if __name__ == "__main__":
    main()
