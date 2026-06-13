"""Data models for the static blog generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    pass


@dataclass
class Post:
    """Represents a single blog post."""
    title: str
    date: date
    source_path: Path
    slug: str = ""
    description: str = ""
    banner: str = ""
    tags: list[str] = field(default_factory=list)
    comments: bool = True
    content_html: str = ""
    url: str = ""

    def __post_init__(self):
        if not self.slug:
            self.slug = self.date.strftime("%Y%m%d")
        if not self.url:
            self.url = f"/blog/{self.date.year}/{self.date.month:02d}/{self.slug}/"


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


@dataclass
class HistoryItem:
    """Represents a portfolio snapshot extracted from a weekly journal post."""
    post: Post
    image_url: str

    @property
    def date(self) -> date:
        return self.post.date

    @property
    def title(self) -> str:
        return self.post.title
