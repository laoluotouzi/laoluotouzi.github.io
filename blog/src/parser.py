"""Markdown parser with frontmatter extraction and path resolution."""

import re
from datetime import date, datetime
from pathlib import Path

import mistune
import yaml
from mistune.plugins.table import table as plugin_table
from mistune.plugins.formatting import mark as plugin_mark
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

from models import Post


class CodeHighlightRenderer(mistune.HTMLRenderer):
    """Custom HTML renderer with Pygments code highlighting."""

    def __init__(self):
        super().__init__(escape=False)

    def block_code(self, code, info=None, **kwargs):
        if not info:
            return f"<pre><code>{mistune.escape(code)}</code></pre>\n"
        try:
            lexer = get_lexer_by_name(info.strip(), stripall=True)
        except Exception:
            lexer = TextLexer(stripall=True)
        formatter = HtmlFormatter(cssclass="highlight", nowrap=False)
        return highlight(code, lexer, formatter)


def create_markdown():
    """Create a configured mistune Markdown instance."""
    renderer = CodeHighlightRenderer()
    md = mistune.Markdown(
        renderer=renderer,
        plugins=[plugin_table, plugin_mark],
    )
    return md


def scan_posts(docs_dir: Path) -> list[Path]:
    """Scan docs/blog/YYYY/MM/ for YYYYMMDD.md files, sorted by name."""
    blog_dir = docs_dir / "blog"
    if not blog_dir.exists():
        return []

    posts = []
    for year_dir in sorted(blog_dir.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir() or not month_dir.name.isdigit():
                continue
            for md_file in sorted(month_dir.glob("*.md")):
                posts.append(md_file)
    return posts


def parse_frontmatter(content: str, filename: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata_dict, body_content)."""
    if not content.startswith("---"):
        # No frontmatter, infer from content
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}, content

    body = parts[2].lstrip("\n")
    return metadata, body


def resolve_relative_paths(html_content: str, source_path: Path, docs_dir: Path) -> str:
    """Resolve relative image/link paths to docs-relative paths.

    Converts paths like ../../../../attachments/... to attachments/...
    """

    def replace_path(match):
        attr = match.group(1)
        raw_path = match.group(2)

        # Skip absolute URLs, anchors, and already-absolute paths
        if raw_path.startswith(("http://", "https://", "#", "mailto:", "/")):
            return f'{attr}"{raw_path}"'

        # Resolve relative path based on source file location
        resolved = (source_path.parent / raw_path).resolve()
        try:
            relative_to_docs = resolved.relative_to(docs_dir.resolve())
            return f'{attr}"/{relative_to_docs}"'
        except ValueError:
            # Path resolved outside docs/ (e.g. ../../../../attachments from docs/blog/2025/01/)
            # MkDocs treats these as relative to docs/, so map them back
            # Extract the last meaningful part (e.g. "attachments/2025/01/...")
            parts = Path(raw_path).parts
            for i, part in enumerate(parts):
                if part == "attachments":
                    fallback = str(Path(*parts[i:]))
                    # Check if this path exists under docs/
                    if (docs_dir / fallback).exists():
                        return f'{attr}"/{fallback}"'
                    break
            return f'{attr}"/{raw_path}"'

    # Match src="..." and href="..." attributes
    pattern = r'((?:src|href)=)"([^"]*)"'
    return re.sub(pattern, replace_path, html_content)


def parse_post(source_path: Path, docs_dir: Path, md: mistune.Markdown) -> Post:
    """Parse a single markdown file into a Post object."""
    content = source_path.read_text(encoding="utf-8")
    filename = source_path.stem  # e.g., "20250104"

    metadata, body = parse_frontmatter(content, filename)

    # Extract date
    post_date = metadata.get("date")
    if isinstance(post_date, date):
        pass
    elif isinstance(post_date, datetime):
        post_date = post_date.date()
    elif isinstance(post_date, str):
        try:
            post_date = datetime.strptime(post_date, "%Y-%m-%d").date()
        except ValueError:
            # Try to infer from filename
            post_date = _date_from_filename(filename)
    else:
        post_date = _date_from_filename(filename)

    # Extract title
    title = metadata.get("title", "")
    if not title:
        # Infer from first heading in body
        heading_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = heading_match.group(1).strip() if heading_match else filename

    # Extract tags
    tags = metadata.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]

    # Convert markdown to HTML
    content_html = md(body)

    # Resolve relative paths
    content_html = resolve_relative_paths(content_html, source_path, docs_dir)

    # Extract banner and resolve its path
    banner = metadata.get("banner", "")
    if banner:
        resolved_banner = (source_path.parent / banner).resolve()
        try:
            banner = f"/{resolved_banner.relative_to(docs_dir.resolve())}"
        except ValueError:
            # Path outside docs/, try fallback to attachments subpath
            parts = Path(banner).parts
            for i, part in enumerate(parts):
                if part == "attachments":
                    fallback = str(Path(*parts[i:]))
                    if (docs_dir / fallback).exists():
                        banner = f"/{fallback}"
                    break

    return Post(
        title=title,
        date=post_date,
        source_path=source_path,
        description=metadata.get("description", ""),
        banner=banner,
        tags=tags,
        comments=metadata.get("comments", True),
        content_html=content_html,
    )


def parse_all_posts(docs_dir: Path) -> list[Post]:
    """Scan and parse all posts, returning them sorted by date descending."""
    paths = scan_posts(docs_dir)
    md = create_markdown()
    posts = [parse_post(p, docs_dir, md) for p in paths]
    posts.sort(key=lambda p: p.date, reverse=True)
    return posts


def parse_about_page(docs_dir: Path) -> dict:
    """Parse the about page from docs/about/index.md."""
    about_path = docs_dir / "about" / "index.md"
    if not about_path.exists():
        return None

    content = about_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content, "index")

    md = create_markdown()
    content_html = md(body)
    content_html = resolve_relative_paths(content_html, about_path, docs_dir)

    return {
        "title": metadata.get("title", "关于"),
        "description": metadata.get("description", ""),
        "content_html": content_html,
    }


def _date_from_filename(filename: str) -> date:
    """Extract date from filename like '20250104'."""
    try:
        return datetime.strptime(filename, "%Y%m%d").date()
    except ValueError:
        return date.today()
