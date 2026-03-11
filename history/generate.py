#!/usr/bin/env python3
"""
交易历史图片展示页面生成器

扫描 docs/attachments/ 目录下的所有日期目录中的 1.png 文件，
生成瀑布流布局的静态 HTML 页面。
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
from jinja2 import Template


def parse_date(date_str: str) -> Optional[datetime]:
    """
    解析多种日期格式

    支持的格式：
    - ISO 8601: YYYY-MM-DD
    - YYYY/MM/DD
    - YYYY.MM.DD
    - YYYYMMDD (紧凑格式)
    """
    date_formats = [
        "%Y%m%d",        # YYYYMMDD (紧凑格式，如 20221127)
        "%Y-%m-%d",      # ISO 8601
        "%Y/%m/%d",      # YYYY/MM/DD
        "%Y.%m.%d",      # YYYY.MM.DD
        "%Y-%m-%d %H:%M:%S",  # ISO 8601 with time
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def scan_attachments_directory(attachments_dir: Path) -> List[Tuple[datetime, str, Path]]:
    """
    扫描 attachments 目录，提取所有图片

    支持两种目录结构：
    - docs/attachments/YYYY/MM/YYYYMMDD/1.png (年/月/日期/文件)
    - docs/attachments/YYYY/YYYY-MM-DD/1.png (年/日期/文件)

    返回: [(date, date_label, image_path), ...]
    """
    images = []

    if not attachments_dir.exists():
        print(f"警告: 附件目录不存在: {attachments_dir}")
        return images

    # 递归扫描所有子目录
    for year_dir in attachments_dir.iterdir():
        if not year_dir.is_dir():
            continue

        # 第一层：年目录下的内容可能是月目录或日期目录
        for item in year_dir.iterdir():
            if not item.is_dir():
                continue

            # 检查是否是月目录（01-12）
            if item.name.isdigit() and 1 <= int(item.name) <= 12:
                # 这是月目录，继续扫描下一层（日期目录）
                for date_dir in item.iterdir():
                    if not date_dir.is_dir():
                        continue

                    image_path = date_dir / "1.png"
                    if not image_path.exists():
                        continue

                    date_label = date_dir.name
                    parsed_date = parse_date(date_label)

                    if parsed_date is None:
                        print(f"警告: 无法解析日期格式: {date_dir.name}，使用目录名作为标签")
                        parsed_date = datetime.min

                    # 只显示周六的图片（周一=0, 周六=5, 周日=6）
                    if parsed_date != datetime.min and parsed_date.weekday() != 5:
                        continue

                    images.append((parsed_date, date_label, image_path))
            else:
                # 这可能是直接在年目录下的日期目录
                date_dir = item
                image_path = date_dir / "1.png"
                if not image_path.exists():
                    continue

                date_label = date_dir.name
                parsed_date = parse_date(date_label)

                if parsed_date is None:
                    print(f"警告: 无法解析日期格式: {date_dir.name}，使用目录名作为标签")
                    parsed_date = datetime.min

                # 只显示周六的图片（周一=0, 周六=5, 周日=6）
                if parsed_date != datetime.min and parsed_date.weekday() != 5:
                    continue

                images.append((parsed_date, date_label, image_path))

    return images


def sort_images_by_date(images: List[Tuple[datetime, str, Path]]) -> List[Tuple[datetime, str, Path]]:
    """
    按日期倒序排列图片
    """
    return sorted(images, key=lambda x: x[0], reverse=True)


def generate_relative_path(image_path: Path, attachments_dir: Path) -> str:
    """
    生成图片的完整 URL 路径

    生成公网可访问的完整 URL，格式：https://invest.zdyi.com/attachments/YYYY/MM/YYYYMMDD/1.png
    """
    # 从完整路径中去掉 'docs/' 前缀，得到 attachments/... 格式
    # 例如：docs/attachments/2022/11/20221127/1.png -> attachments/2022/11/20221127/1.png
    path_str = str(image_path)
    if path_str.startswith('docs/'):
        path_str = path_str[5:]  # 去掉 'docs/' 前缀
    return f"https://invest.zdyi.com/{path_str}"


def generate_blog_url(image_url: str) -> str:
    """
    生成对应的博客页面 URL

    从图片 URL 生成博客页面 URL：
    https://invest.zdyi.com/attachments/YYYY/MM/YYYYMMDD/1.png
    -> https://invest.zdyi.com/blog/YYYY/MM/YYYYMMDD/
    """
    # 将 attachments 替换为 blog，并去掉文件名
    blog_url = image_url.replace('attachments/', 'blog/')
    blog_url = blog_url.rsplit('/', 1)[0]  # 去掉最后的 /1.png
    return blog_url + '/'  # 确保以 / 结尾


def render_html(images: List[Tuple[datetime, str, Path]], template_path: Path, output_path: Path, attachments_dir: Path):
    """
    使用 Jinja2 模板生成 HTML
    """
    # 准备模板数据
    gallery_items = []
    for date, date_label, image_path in images:
        image_url = generate_relative_path(image_path, attachments_dir)
        blog_url = generate_blog_url(image_url)
        gallery_items.append({
            'date': date_label,
            'image_url': image_url,
            'full_image_url': image_url,
            'blog_url': blog_url
        })

    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)
    html_content = template.render(items=gallery_items)

    # 写入输出文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    parser = argparse.ArgumentParser(
        description='生成交易历史图片展示页面'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('docs/attachments'),
        help='附件目录路径 (默认: docs/attachments)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('history/static/index.html'),
        help='输出 HTML 文件路径 (默认: history/static/index.html)'
    )
    parser.add_argument(
        '--template',
        type=Path,
        default=Path(__file__).parent / 'template.html',
        help='HTML 模板文件路径 (默认: history/template.html)'
    )

    args = parser.parse_args()

    print("📸 交易历史图片展示页面生成器")
    print("=" * 50)

    # 扫描目录
    print(f"🔍 扫描目录: {args.input}")
    images = scan_attachments_directory(args.input)
    print(f"✅ 找到 {len(images)} 张图片")

    if not images:
        print("❌ 没有找到任何图片，退出")
        return

    # 排序
    print("📅 按日期排序...")
    sorted_images = sort_images_by_date(images)

    # 生成 HTML
    print(f"📝 生成 HTML 页面: {args.output}")
    try:
        render_html(sorted_images, args.template, args.output, args.input)
        print("✅ 页面生成成功！")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        raise

    print("=" * 50)
    print(f"🎉 完成！打开 {args.output} 查看结果")


if __name__ == '__main__':
    main()
