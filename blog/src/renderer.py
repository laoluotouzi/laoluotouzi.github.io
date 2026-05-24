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


def build_sidebar_context(posts: list[Post]) -> dict:
    """Build context data for the right sidebar widgets."""
    # Recent 5 posts
    recent_posts = posts[:5]

    # Top 20 tags by count
    tag_counts: dict[str, int] = {}
    for post in posts:
        for tag_name in post.tags:
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    sidebar_tags = [{"name": name, "slug": tag_slug(name), "count": count} for name, count in top_tags]

    # Archive years with counts
    by_year: dict[int, int] = defaultdict(int)
    for post in posts:
        by_year[post.date.year] += 1
    archive_years = sorted(
        [{"year": y, "count": c} for y, c in by_year.items()],
        key=lambda x: x["year"],
        reverse=True,
    )

    return {
        "sidebar": {
            "recent_posts": recent_posts,
            "tags": sidebar_tags,
            "archive_years": archive_years,
        }
    }


def render_posts(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None) -> None:
    """Render individual post detail pages."""
    template = env.get_template("post.html")
    ctx = sidebar_context or {}
    for post in posts:
        output_dir = dist_dir / "posts" / str(post.date.year) / f"{post.date.month:02d}" / post.date.strftime("%Y%m%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        html = template.render(post=post, **ctx)
        (output_dir / "index.html").write_text(html, encoding="utf-8")


def render_index(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None, per_page: int = 10) -> None:
    """Render homepage with pagination."""
    template = env.get_template("index.html")
    total_pages = math.ceil(len(posts) / per_page)
    ctx = sidebar_context or {}

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

        html = template.render(posts=page_posts, pagination=pagination, **ctx)

        if page_num == 1:
            output_path = dist_dir / "index.html"
        else:
            output_dir = dist_dir / "page" / str(page_num)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "index.html"

        output_path.write_text(html, encoding="utf-8")


def render_tags(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None) -> None:
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

    ctx = sidebar_context or {}

    # Render tags index page
    tags_index_template = env.get_template("tags_index.html")
    tags_dir = dist_dir / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)
    html = tags_index_template.render(tags=tags, **ctx)
    (tags_dir / "index.html").write_text(html, encoding="utf-8")

    # Render individual tag pages
    tag_template = env.get_template("tag.html")
    for tag in tags:
        tag_dir = tags_dir / tag.slug
        tag_dir.mkdir(parents=True, exist_ok=True)
        html = tag_template.render(tag=tag, posts=tag.posts, **ctx)
        (tag_dir / "index.html").write_text(html, encoding="utf-8")


def render_archives(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None) -> None:
    """Render archive index, year, and year-month archive pages."""
    archive_template = env.get_template("archive.html")

    # Group by year and month
    by_year: dict[int, list[Post]] = defaultdict(list)
    by_year_month: dict[tuple[int, int], list[Post]] = defaultdict(list)

    for post in posts:
        by_year[post.date.year].append(post)
        by_year_month[(post.date.year, post.date.month)].append(post)

    archive_dir = dist_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Render archive index page
    archive_index_template = env.get_template("archive_index.html")
    archives: dict[int, dict] = {}
    for year, year_posts in sorted(by_year.items(), reverse=True):
        months = sorted(
            {m for (y, m) in by_year_month if y == year}
        )
        archives[year] = {
            "total": len(year_posts),
            "months": [(m, len(by_year_month[(year, m)])) for m in months],
        }
    ctx = sidebar_context or {}
    html = archive_index_template.render(archives=archives, **ctx)
    (archive_dir / "index.html").write_text(html, encoding="utf-8")

    # Render year and month archives
    for year, year_posts in sorted(by_year.items(), reverse=True):
        archive = Archive(year=year)
        year_dir = archive_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        html = archive_template.render(archive=archive, posts=year_posts, **ctx)
        (year_dir / "index.html").write_text(html, encoding="utf-8")

    for (year, month), month_posts in sorted(by_year_month.items(), reverse=True):
        archive = Archive(year=year, month=month)
        month_dir = archive_dir / str(year) / f"{month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        html = archive_template.render(archive=archive, posts=month_posts, **ctx)
        (month_dir / "index.html").write_text(html, encoding="utf-8")
