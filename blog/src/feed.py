"""RSS 2.0 feed generator."""

import urllib.parse
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

from models import Post


def generate_rss(posts: list[Post], dist_dir: Path, site_url: str = "https://laoluotouzi.github.io", max_items: int = 20) -> None:
    """Generate RSS 2.0 feed XML from the latest posts."""
    rss = Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    channel = SubElement(rss, "channel")

    SubElement(channel, "title").text = "老罗投资"
    SubElement(channel, "link").text = site_url
    SubElement(channel, "description").text = "专注于股权投资、阅读、学习与个人成长"
    SubElement(channel, "language").text = "zh-CN"

    atom_link = SubElement(channel, "atom:link")
    atom_link.set("href", f"{site_url}/feed.xml")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    for post in posts[:max_items]:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = post.title
        SubElement(item, "link").text = f"{site_url}{post.url}"
        SubElement(item, "description").text = post.description
        SubElement(item, "pubDate").text = post.date.strftime("%a, %d %b %Y 00:00:00 +0800")
        SubElement(item, "guid").text = f"{site_url}{post.url}"

    indent(rss, space="  ")

    dist_dir.mkdir(parents=True, exist_ok=True)
    tree = ElementTree(rss)
    tree.write(dist_dir / "feed.xml", xml_declaration=True, encoding="utf-8")
