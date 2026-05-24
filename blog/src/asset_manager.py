"""Asset pipeline for copying attachments and static resources."""

import shutil
import urllib.parse
from pathlib import Path


def clean_output(dist_dir: Path) -> None:
    """Remove the entire dist directory for a clean build."""
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)


def copy_attachments(docs_dir: Path, dist_dir: Path) -> None:
    """Copy docs/attachments/ to dist/attachments/, preserving directory structure."""
    src = docs_dir / "attachments"
    dst = dist_dir / "attachments"
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_static(src_dir: Path, dist_dir: Path) -> None:
    """Copy blog/src/static/ to dist/static/, preserving directory structure."""
    src = src_dir / "static"
    dst = dist_dir / "static"
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def url_encode_path(path: str) -> str:
    """Encode a URL path with percent-encoding for special/CJK characters.

    Preserves '/' separators. Only encodes individual path segments.
    """
    if not path.startswith("/"):
        path = "/" + path

    parts = path.split("/")
    encoded_parts = [urllib.parse.quote(part) for part in parts]
    return "/".join(encoded_parts)
