"""Sitemap XML generator."""

from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

from models import Post


def generate_sitemap(
    posts: list[Post],
    dist_dir: Path,
    site_url: str = "https://invest.zdyi.com",
) -> None:
    """Generate sitemap.xml from all posts."""
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    # Homepage
    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = site_url + "/"
    SubElement(url, "changefreq").text = "daily"
    SubElement(url, "priority").text = "1.0"

    # Post pages
    for post in posts:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = site_url + post.url
        SubElement(url, "lastmod").text = post.date.isoformat()
        SubElement(url, "changefreq").text = "monthly"
        SubElement(url, "priority").text = "0.8"

    indent(urlset, space="  ")

    dist_dir.mkdir(parents=True, exist_ok=True)
    tree = ElementTree(urlset)
    tree.write(dist_dir / "sitemap.xml", xml_declaration=True, encoding="utf-8")
