"""Pagination helpers shared by public catalogue endpoints."""

from math import ceil


def total_pages(total: int, page_size: int) -> int:
    return ceil(total / page_size) if total else 0
