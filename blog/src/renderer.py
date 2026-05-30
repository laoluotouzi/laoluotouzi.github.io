"""Page rendering with Jinja2 templates."""

import math
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from models import Archive, HistoryItem, Post, Tag


def tag_slug(name: str) -> str:
    """Convert a tag name to a URL-safe slug."""
    return urllib.parse.quote(name)


def truncate(text: str, length: int = 200) -> str:
    """Truncate text to a given length with ellipsis."""
    if len(text) <= length:
        return text
    return text[:length] + "..."


def create_env(templates_dir: Path, version: str = "") -> Environment:
    """Create and configure Jinja2 environment."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=True,
    )
    env.filters["tag_slug"] = tag_slug
    env.filters["truncate"] = truncate
    env.globals["version"] = version
    return env


def _build_page_range(current: int, total: int, window: int = 2) -> list:
    """Build a page range list with ellipsis for large page counts.

    Returns a list like [1, '...', 4, 5, 6, '...', 10] where '...' represents a gap.
    Shows at most 5 page numbers.
    """
    if total <= 5:
        return list(range(1, total + 1))

    pages = [1]

    if current <= 3:
        mid_start, mid_end = 2, min(4, total - 1)
    elif current >= total - 2:
        mid_start, mid_end = max(2, total - 3), total - 1
    else:
        mid_start, mid_end = current - 1, current + 1

    if mid_start > 2:
        pages.append("...")
    pages.extend(range(mid_start, mid_end + 1))
    if mid_end < total - 1:
        pages.append("...")
    pages.append(total)

    return pages


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
    for i, post in enumerate(posts):
        prev_post = posts[i + 1] if i + 1 < len(posts) else None
        next_post = posts[i - 1] if i - 1 >= 0 else None
        output_dir = dist_dir / "blog" / str(post.date.year) / f"{post.date.month:02d}" / post.date.strftime("%Y%m%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        html = template.render(post=post, prev_post=prev_post, next_post=next_post, **ctx)
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

        # Build page number list with ellipsis for large page counts
        page_range = _build_page_range(page_num, total_pages)
        pages = []
        for p in page_range:
            if p == "...":
                pages.append({"type": "ellipsis"})
            else:
                pages.append({
                    "type": "page",
                    "number": p,
                    "url": "/" if p == 1 else f"/page/{p}/",
                    "is_current": p == page_num,
                })

        pagination = {
            "current": page_num,
            "total": total_pages,
            "has_prev": page_num > 1,
            "has_next": page_num < total_pages,
            "prev_url": "/" if page_num == 2 else f"/page/{page_num - 1}/",
            "next_url": f"/page/{page_num + 1}/",
            "pages": pages,
        }

        html = template.render(posts=page_posts, pagination=pagination, **ctx)

        if page_num == 1:
            output_path = dist_dir / "index.html"
        else:
            output_dir = dist_dir / "page" / str(page_num)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "index.html"

        output_path.write_text(html, encoding="utf-8")


def render_tags(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None, per_page: int = 10) -> None:
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

    # Render individual tag pages with pagination
    tag_template = env.get_template("tag.html")
    for tag in tags:
        total_pages = math.ceil(len(tag.posts) / per_page)

        for page_num in range(1, total_pages + 1):
            start = (page_num - 1) * per_page
            end = start + per_page
            page_posts = tag.posts[start:end]

            # Build page number list
            page_range = _build_page_range(page_num, total_pages)
            pages = []
            for p in page_range:
                if p == "...":
                    pages.append({"type": "ellipsis"})
                else:
                    pages.append({
                        "type": "page",
                        "number": p,
                        "url": f"/tags/{tag.name}/" if p == 1 else f"/tags/{tag.name}/page/{p}/",
                        "is_current": p == page_num,
                    })

            pagination = {
                "current": page_num,
                "total": total_pages,
                "has_prev": page_num > 1,
                "has_next": page_num < total_pages,
                "prev_url": f"/tags/{tag.name}/" if page_num == 2 else f"/tags/{tag.name}/page/{page_num - 1}/",
                "next_url": f"/tags/{tag.name}/page/{page_num + 1}/",
                "pages": pages,
            }

            html = tag_template.render(tag=tag, posts=page_posts, pagination=pagination, **ctx)

            if page_num == 1:
                tag_dir = tags_dir / tag.name
                tag_dir.mkdir(parents=True, exist_ok=True)
                (tag_dir / "index.html").write_text(html, encoding="utf-8")
            else:
                page_dir = tags_dir / tag.name / "page" / str(page_num)
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / "index.html").write_text(html, encoding="utf-8")


def render_archives(env: Environment, posts: list[Post], dist_dir: Path, sidebar_context: dict = None, per_page: int = 10) -> None:
    """Render archive index, year, and year-month archive pages with pagination."""
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
            {m for (y, m) in by_year_month if y == year},
            reverse=True,
        )
        archives[year] = {
            "total": len(year_posts),
            "months": [(m, len(by_year_month[(year, m)])) for m in months],
        }
    ctx = sidebar_context or {}
    html = archive_index_template.render(archives=archives, **ctx)
    (archive_dir / "index.html").write_text(html, encoding="utf-8")

    def _render_archive_pages(archive: Archive, all_posts: list[Post], base_dir: Path) -> None:
        """Render archive pages with pagination."""
        total_pages = math.ceil(len(all_posts) / per_page)
        total_posts = len(all_posts)

        for page_num in range(1, total_pages + 1):
            start = (page_num - 1) * per_page
            end = start + per_page
            page_posts = all_posts[start:end]

            # Build page number list
            page_range = _build_page_range(page_num, total_pages)
            base_url = archive.url
            pages = []
            for p in page_range:
                if p == "...":
                    pages.append({"type": "ellipsis"})
                else:
                    pages.append({
                        "type": "page",
                        "number": p,
                        "url": base_url if p == 1 else f"{base_url}page/{p}/",
                        "is_current": p == page_num,
                    })

            pagination = {
                "current": page_num,
                "total": total_pages,
                "has_prev": page_num > 1,
                "has_next": page_num < total_pages,
                "prev_url": base_url if page_num == 2 else f"{base_url}page/{page_num - 1}/",
                "next_url": f"{base_url}page/{page_num + 1}/",
                "pages": pages,
            }

            html = archive_template.render(archive=archive, posts=page_posts, total_posts=total_posts, pagination=pagination, **ctx)

            if page_num == 1:
                base_dir.mkdir(parents=True, exist_ok=True)
                (base_dir / "index.html").write_text(html, encoding="utf-8")
            else:
                page_dir = base_dir / "page" / str(page_num)
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / "index.html").write_text(html, encoding="utf-8")

    # Render year archives with pagination
    for year, year_posts in sorted(by_year.items(), reverse=True):
        archive = Archive(year=year)
        year_dir = archive_dir / str(year)
        _render_archive_pages(archive, year_posts, year_dir)

    # Render month archives with pagination
    for (year, month), month_posts in sorted(by_year_month.items(), reverse=True):
        archive = Archive(year=year, month=month)
        month_dir = archive_dir / str(year) / f"{month:02d}"
        _render_archive_pages(archive, month_posts, month_dir)


def _extract_history_items(posts: list[Post], docs_dir: Path = None) -> list[HistoryItem]:
    """Extract portfolio snapshot images from markdown source files.

    Scans docs/blog/YYYY/MM/YYYYMMDD.md for images with alt text containing
    "目前持仓" or "持仓股票明细", then links them to the corresponding Post.
    """
    if docs_dir is None:
        return []

    blog_dir = docs_dir / "blog"
    if not blog_dir.exists():
        return []

    # Build a lookup from date string (YYYYMMDD) to Post
    post_by_datekey: dict[str, Post] = {}
    for post in posts:
        key = post.date.strftime("%Y%m%d")
        post_by_datekey[key] = post

    _MD_IMG_PATTERN = re.compile(
        r'!\[(?:目前持仓|持仓股票明细[^\]]*)\]\(([^)]+)\)',
    )

    items: list[HistoryItem] = []
    for md_file in blog_dir.rglob("*.md"):
        if not md_file.stem.isdigit() or len(md_file.stem) != 8:
            continue
        content = md_file.read_text(encoding="utf-8")
        match = _MD_IMG_PATTERN.search(content)
        if not match:
            continue

        datekey = md_file.stem
        # Convert relative path like ../../../attachments/YYYY/MM/YYYYMMDD/1.png
        # to site-absolute path like /attachments/YYYY/MM/YYYYMMDD/1.png
        raw_path = match.group(1)
        clean_path = raw_path.replace("../", "")
        if not clean_path.startswith("attachments/"):
            clean_path = "attachments/" + clean_path
        image_url = "/" + clean_path

        post = post_by_datekey.get(datekey)
        if post is None:
            from datetime import date as date_type
            try:
                d = date_type(int(datekey[:4]), int(datekey[4:6]), int(datekey[6:8]))
            except ValueError:
                continue
            post = Post(
                title=f"老罗投资周记-{datekey}",
                date=d,
                source_path=md_file,
                url=f"/blog/{d.year}/{d.month:02d}/{datekey}/",
            )

        items.append(HistoryItem(post=post, image_url=image_url))

    items.sort(key=lambda x: x.date, reverse=True)
    return items


def render_history(env: Environment, items: list[HistoryItem], dist_dir: Path, sidebar_context: dict = None, per_page: int = 10) -> None:
    """Render history pages with year tabs, each year with its own pagination."""
    if not items:
        return

    ctx = sidebar_context or {}
    history_dir = dist_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    template = env.get_template("history.html")

    # Group items by year
    by_year: dict[int, list[HistoryItem]] = defaultdict(list)
    for item in items:
        by_year[item.date.year].append(item)

    years = sorted(by_year.keys(), reverse=True)
    current_year = years[0] if years else None
    year_counts = {y: len(by_year[y]) for y in years}

    def _render_year_pages(year: int, year_items: list[HistoryItem], is_default: bool = False) -> None:
        total_pages = math.ceil(len(year_items) / per_page)
        base_url = "/history/" if is_default else f"/history/{year}/"

        for page_num in range(1, total_pages + 1):
            start = (page_num - 1) * per_page
            end = start + per_page
            page_items = year_items[start:end]

            page_range = _build_page_range(page_num, total_pages)
            pages = []
            for p in page_range:
                if p == "...":
                    pages.append({"type": "ellipsis"})
                else:
                    p_url = base_url if p == 1 else f"{base_url}page/{p}/"
                    pages.append({
                        "type": "page",
                        "number": p,
                        "url": p_url,
                        "is_current": p == page_num,
                    })

            pagination = {
                "current": page_num,
                "total": total_pages,
                "has_prev": page_num > 1,
                "has_next": page_num < total_pages,
                "prev_url": base_url if page_num == 2 else f"{base_url}page/{page_num - 1}/",
                "next_url": f"{base_url}page/{page_num + 1}/",
                "pages": pages,
            }

            html = template.render(
                items=page_items, year=year, years=years, year_counts=year_counts,
                year_total=len(year_items), total_items=len(items),
                pagination=pagination, **ctx,
            )

            if is_default:
                if page_num == 1:
                    (history_dir / "index.html").write_text(html, encoding="utf-8")
                else:
                    page_dir = history_dir / "page" / str(page_num)
                    page_dir.mkdir(parents=True, exist_ok=True)
                    (page_dir / "index.html").write_text(html, encoding="utf-8")
            else:
                if page_num == 1:
                    year_dir = history_dir / str(year)
                    year_dir.mkdir(parents=True, exist_ok=True)
                    (year_dir / "index.html").write_text(html, encoding="utf-8")
                else:
                    page_dir = history_dir / str(year) / "page" / str(page_num)
                    page_dir.mkdir(parents=True, exist_ok=True)
                    (page_dir / "index.html").write_text(html, encoding="utf-8")

    # Render all years, each at /history/{year}/
    for year in years:
        _render_year_pages(year, by_year[year])

    # Also render current year as the default /history/ page
    if current_year:
        _render_year_pages(current_year, by_year[current_year], is_default=True)


def render_about(env: Environment, page: dict, dist_dir: Path, sidebar_context: dict = None) -> None:
    """Render the about page."""
    template = env.get_template("about.html")
    ctx = sidebar_context or {}
    about_dir = dist_dir / "about"
    about_dir.mkdir(parents=True, exist_ok=True)
    html = template.render(page=page, **ctx)
    (about_dir / "index.html").write_text(html, encoding="utf-8")
