"""CLI entry point for the static blog generator."""

import argparse
import sys
import time
from pathlib import Path

# Add the src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from asset_manager import clean_output, copy_attachments, copy_static
from feed import generate_rss
from parser import parse_all_posts
from renderer import build_sidebar_context, create_env, render_archives, render_index, render_posts, render_tags

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
    env = create_env(TEMPLATES_DIR)
    render_posts(env, posts, DIST_DIR, sidebar_ctx)
    print(f"  Rendered {len(posts)} post pages")

    render_index(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered index pages")

    render_tags(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered tag pages")

    render_archives(env, posts, DIST_DIR, sidebar_ctx)
    print("  Rendered archive pages")

    # Step 6: Generate RSS
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
