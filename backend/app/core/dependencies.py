"""Core dependency injection providers.

This module will provide database session and authentication user dependencies
in Phase 3 (Database) and Phase 4 (Authentication).
"""

from typing import Generator


def get_db_placeholder() -> Generator:
    """Placeholder dependency for future database session injection."""
    yield None
