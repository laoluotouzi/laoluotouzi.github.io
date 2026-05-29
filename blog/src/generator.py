"""CLI entry point for the static blog generator."""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

# Add the src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from asset_manager import clean_output, copy_attachments, copy_static
from feed import generate_rss
from parser import parse_all_posts, parse_about_page
from renderer import build_sidebar_context, create_env, render_about, render_archives, render_history, render_index, render_posts, render_tags
from renderer import _extract_history_items

PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SRC_DIR = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "blog" / "dist"
TEMPLATES_DIR = SRC_DIR / "templates"


def build():
    """Execute a full site build."""
    start_time = time.time()
    print(f"Source: {DOCS_DIR}")
    print(f"Output: {DIST_DIR}")
    print()

    # Step 1: Clean output
    print("Cleaning output directory...")
    clean_output(DIST_DIR)

    # Step 2: Parse all posts
    print("Parsing posts...")
    posts = parse_all_posts(DOCS_DIR)
    print(f"  Found {len(posts)} posts")

    # Step 3: Copy assets
    print("Copying attachments...")
    copy_attachments(DOCS_DIR, DIST_DIR)
    print("Copying static resources...")
    copy_static(SRC_DIR, DIST_DIR)

    # Step 4: Build sidebar context
    print("Building sidebar context...")
    sidebar_ctx = build_sidebar_context(posts)

    # Step 5: Render pages
    print("Rendering pages...")
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    env = create_env(TEMPLATES_DIR, version)
    render_posts(env, posts, DIST_DIR, sidebar_ctx)
    print(f"  Rendered {len(posts)} post pages")

    render_index(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered index pages")

    render_tags(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered tag pages")

    render_archives(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered archive pages")

    history_items = _extract_history_items(posts, DOCS_DIR)
    render_history(env, history_items, DIST_DIR, sidebar_ctx)
    print(f"  Rendered history pages ({len(history_items)} items)")

    # Step 6: Render about page
    about_page = parse_about_page(DOCS_DIR)
    if about_page:
        render_about(env, about_page, DIST_DIR, sidebar_ctx)
        print("  Rendered about page")

    # Step 7: Generate RSS
    print("Generating RSS feed...")
    generate_rss(posts, DIST_DIR)

    elapsed = time.time() - start_time
    print()
    print(f"Build complete in {elapsed:.2f}s")
    print(f"Output: {DIST_DIR}")


def clean():
    """Remove the dist directory."""
    if DIST_DIR.exists():
        import shutil
        shutil.rmtree(DIST_DIR)
        print(f"Removed {DIST_DIR}")
    else:
        print(f"Directory {DIST_DIR} does not exist")


def main():
    parser = argparse.ArgumentParser(description="Static blog generator")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build the static site")
    subparsers.add_parser("clean", help="Remove the output directory")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "clean":
        clean()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
