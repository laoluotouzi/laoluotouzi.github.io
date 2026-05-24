"""Data models for the static blog generator."""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional


@dataclass
class Post:
    """Represents a single blog post."""
    title: str
    date: date
    source_path: Path
    description: str = ""
    banner: str = ""
    tags: list[str] = field(default_factory=list)
    comments: bool = True
    content_html: str = ""
    url: str = ""

    def __post_init__(self):
        if not self.url:
            self.url = f"/posts/{self.date.year}/{self.date.month:02d}/{self.date.strftime('%Y%m%d')}/"


@dataclass
class Tag:
    """Represents a tag with its associated posts."""
    name: str
    slug: str
    posts: list[Post] = field(default_factory=list)


@dataclass
class Archive:
    """Represents a year or year-month archive."""
    year: int
    month: Optional[int] = None
    posts: list[Post] = field(default_factory=list)

    @property
    def url(self) -> str:
        if self.month:
            return f"/archive/{self.year}/{self.month:02d}/"
        return f"/archive/{self.year}/"

    @property
    def title(self) -> str:
        if self.month:
            return f"{self.year}年{self.month:02d}月"
        return f"{self.year}年"
