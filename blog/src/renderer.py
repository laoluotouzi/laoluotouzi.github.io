"""Page rendering with Jinja2 templates."""

import math
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from models import Archive, Post, Tag


def tag_slug(name: str) -> str:
    """Convert a tag name to a URL-safe slug."""
    return urllib.parse.quote(name)


def truncate(text: str, length: int = 200) -> str:
    """Truncate text to a given length with ellipsis."""
    if len(text) <= length:
        return text
    return text[:length] + "..."


def create_env(templates_dir: Path) -> Environment:
    """Create and configure Jinja2 environment."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=True,
    )
    env.filters["tag_slug"] = tag_slug
    env.filters["truncate"] = truncate
    return env


def render_posts(env: Environment, posts: list[Post], dist_dir: Path) -> None:
    """Render individual post detail pages."""
    template = env.get_template("post.html")
    for post in posts:
        output_dir = dist_dir / "posts" / str(post.date.year) / f"{post.date.month:02d}" / post.date.strftime("%Y%m%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        html = template.render(post=post)
        (output_dir / "index.html").write_text(html, encoding="utf-8")


def render_index(env: Environment, posts: list[Post], dist_dir: Path, per_page: int = 10) -> None:
    """Render homepage with pagination."""
    template = env.get_template("index.html")
    total_pages = math.ceil(len(posts) / per_page)

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * per_page
        end = start + per_page
        page_posts = posts[start:end]

        pagination = {
            "current": page_num,
            "total": total_pages,
            "has_prev": page_num > 1,
            "has_next": page_num < total_pages,
            "prev_url": "/" if page_num == 2 else f"/page/{page_num - 1}/",
            "next_url": f"/page/{page_num + 1}/",
        }

        html = template.render(posts=page_posts, pagination=pagination)

        if page_num == 1:
            output_path = dist_dir / "index.html"
        else:
            output_dir = dist_dir / "page" / str(page_num)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "index.html"

        output_path.write_text(html, encoding="utf-8")


def render_tags(env: Environment, posts: list[Post], dist_dir: Path) -> None:
    """Render tag index and individual tag pages."""
    # Build tag index
    tag_map: dict[str, Tag] = {}
    for post in posts:
        for tag_name in post.tags:
            slug = tag_slug(tag_name)
            if slug not in tag_map:
                tag_map[slug] = Tag(name=tag_name, slug=slug)
            tag_map[slug].posts.append(post)

    tags = sorted(tag_map.values(), key=lambda t: len(t.posts), reverse=True)

    # Render tags index page
    tags_index_template = env.get_template("tags_index.html")
    tags_dir = dist_dir / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)
    html = tags_index_template.render(tags=tags)
    (tags_dir / "index.html").write_text(html, encoding="utf-8")

    # Render individual tag pages
    tag_template = env.get_template("tag.html")
    for tag in tags:
        tag_dir = tags_dir / tag.slug
        tag_dir.mkdir(parents=True, exist_ok=True)
        html = tag_template.render(tag=tag, posts=tag.posts)
        (tag_dir / "index.html").write_text(html, encoding="utf-8")


def render_archives(env: Environment, posts: list[Post], dist_dir: Path) -> None:
    """Render year and year-month archive pages."""
    archive_template = env.get_template("archive.html")

    # Group by year and month
    by_year: dict[int, list[Post]] = defaultdict(list)
    by_year_month: dict[tuple[int, int], list[Post]] = defaultdict(list)

    for post in posts:
        by_year[post.date.year].append(post)
        by_year_month[(post.date.year, post.date.month)].append(post)

    archive_dir = dist_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Render year archives
    for year, year_posts in sorted(by_year.items(), reverse=True):
        archive = Archive(year=year)
        year_dir = archive_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        html = archive_template.render(archive=archive, posts=year_posts)
        (year_dir / "index.html").write_text(html, encoding="utf-8")

    # Render month archives
    for (year, month), month_posts in sorted(by_year_month.items(), reverse=True):
        archive = Archive(year=year, month=month)
        month_dir = archive_dir / str(year) / f"{month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        html = archive_template.render(archive=archive, posts=month_posts)
        (month_dir / "index.html").write_text(html, encoding="utf-8")
