#!/usr/bin/env python3
"""
交易历史图片展示页面生成器

扫描 docs/blog/ 目录下的 Markdown 文件，
从包含"老罗投资周记"或"老罗实盘周记"的文章中提取图片引用，
生成瀑布流布局的静态 HTML 页面。
"""

import os
import re
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from jinja2 import Template

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


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


def parse_date_from_path(file_path: Path) -> Optional[datetime]:
    """
    从文件路径中解析日期

    支持的路径格式：
    - docs/blog/YYYY/MM/YYYYMMDD.md
    - docs/blog/YYYY/MM-DD.md
    """
    # 尝试从文件名中提取日期
    filename = file_path.stem  # 去掉扩展名

    # 首先尝试直接解析文件名
    parsed_date = parse_date(filename)
    if parsed_date:
        return parsed_date

    # 尝试从路径结构中提取日期
    parts = file_path.parts
    if len(parts) >= 3:
        # 查找年份和月份目录
        for i, part in enumerate(parts):
            if part.isdigit() and len(part) == 4:
                year = part
                # 检查下一部分是否是月份
                if i + 1 < len(parts) and parts[i + 1].isdigit():
                    month = parts[i + 1].zfill(2)
                    # 尝试组合年月日
                    if len(filename) >= 8:
                        day = filename[-2:] if filename[-2:].isdigit() else "01"
                        date_str = f"{year}{month}{day}"
                        parsed_date = parse_date(date_str)
                        if parsed_date:
                            return parsed_date

    return None


def extract_image_reference(content: str) -> Optional[str]:
    """
    从 Markdown 内容中提取图片引用路径

    匹配格式：![目前持仓](../../../attachments/YYYY/MM/YYYYMMDD/1.png)
    """
    # 正则表达式匹配图片引用
    pattern = r'!\[目前持仓\]\(([^)]+)\)'
    match = re.search(pattern, content)

    if match:
        return match.group(1)

    return None


def convert_to_public_url(relative_path: str) -> str:
    """
    将相对路径转换为公网可访问的 URL

    输入：../../../attachments/2026/03/20260307/1.png
    输出：https://invest.zdyi.com/attachments/2026/03/20260307/1.png
    """
    # 去除 ../ 前缀
    clean_path = relative_path.replace('../', '')
    # 确保路径以 attachments/ 开头
    if not clean_path.startswith('attachments/'):
        clean_path = 'attachments/' + clean_path
    return f'https://invest.zdyi.com/{clean_path}'


def extract_metadata(content: str, file_path: Path) -> Dict[str, str]:
    """
    从 Markdown 文件中提取元数据

    返回字典，包含：
    - title: 文章标题
    - date: 日期字符串
    """
    metadata = {
        'title': '',
        'date': ''
    }

    # 提取标题
    # 优先级 1: frontmatter 中的 title
    title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    else:
        # 优先级 2: 第一个一级标题
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            metadata['title'] = h1_match.group(1).strip()
        else:
            # 优先级 3: 使用文件名
            metadata['title'] = file_path.stem

    # 提取日期
    # 优先级 1: frontmatter 中的 date
    date_match = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
    if date_match:
        metadata['date'] = date_match.group(1).strip()
    else:
        # 优先级 2: 从文件路径解析
        parsed_date = parse_date_from_path(file_path)
        if parsed_date:
            metadata['date'] = parsed_date.strftime('%Y-%m-%d')

    return metadata


def scan_blog_directory(blog_dir: Path) -> List[Tuple[datetime, str, str, Dict[str, str]]]:
    """
    扫描博客目录，从 Markdown 文件中提取图片信息

    返回: [(date, date_label, image_url, metadata), ...]
    """
    images = []
    stats = {
        'total': 0,
        'keyword_match': 0,
        'has_image': 0,
        'success': 0,
        'skipped': 0,
        'errors': 0
    }

    if not blog_dir.exists():
        logger.error(f"错误: 博客目录不存在: {blog_dir}")
        return images

    # 递归扫描所有 Markdown 文件
    logger.info(f"扫描目录: {blog_dir}")
    for md_file in blog_dir.rglob("*.md"):
        stats['total'] += 1

        try:
            # 读取文件内容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否包含关键字（支持"老罗投资周记"和"老罗实盘周记"）
            if "老罗投资周记" not in content and "老罗实盘周记" not in content:
                stats['skipped'] += 1
                continue

            stats['keyword_match'] += 1

            # 提取图片引用
            image_path = extract_image_reference(content)
            if not image_path:
                logger.warning(f"警告: 未找到图片引用: {md_file}")
                stats['skipped'] += 1
                continue

            stats['has_image'] += 1

            # 转换为公网 URL
            image_url = convert_to_public_url(image_path)

            # 提取元数据
            metadata = extract_metadata(content, md_file)

            # 解析日期
            parsed_date = parse_date(metadata['date']) if metadata['date'] else parse_date_from_path(md_file)

            if parsed_date is None:
                logger.warning(f"警告: 无法解析日期: {md_file}，使用文件名作为标签")
                parsed_date = datetime.min
                date_label = md_file.stem
            else:
                # 只显示周六的图片（周一=0, 周六=5, 周日=6）
                if parsed_date != datetime.min and parsed_date.weekday() != 5:
                    stats['skipped'] += 1
                    continue
                date_label = parsed_date.strftime('%Y%m%d')

            images.append((parsed_date, date_label, image_url, metadata))
            stats['success'] += 1

        except FileNotFoundError:
            logger.error(f"错误: 文件不存在: {md_file}")
            stats['errors'] += 1
        except PermissionError:
            logger.error(f"错误: 无权限读取文件: {md_file}")
            stats['errors'] += 1
        except UnicodeDecodeError:
            logger.error(f"错误: 文件编码问题: {md_file}")
            stats['errors'] += 1
        except Exception as e:
            logger.error(f"错误: 处理文件时发生异常: {md_file} - {e}")
            stats['errors'] += 1

    # 输出统计信息
    logger.info("=" * 50)
    logger.info("扫描统计:")
    logger.info(f"  总文件数: {stats['total']}")
    logger.info(f"  包含关键字: {stats['keyword_match']}")
    logger.info(f"  包含图片引用: {stats['has_image']}")
    logger.info(f"  成功处理: {stats['success']}")
    logger.info(f"  跳过: {stats['skipped']}")
    logger.info(f"  错误: {stats['errors']}")
    logger.info("=" * 50)

    return images


def sort_images_by_date(images: List[Tuple[datetime, str, str, Dict[str, str]]]) -> List[Tuple[datetime, str, str, Dict[str, str]]]:
    """
    按日期倒序排列图片
    """
    return sorted(images, key=lambda x: x[0], reverse=True)


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


def render_html(images: List[Tuple[datetime, str, str, Dict[str, str]]], template_path: Path, output_path: Path):
    """
    使用 Jinja2 模板生成 HTML
    """
    # 准备模板数据
    gallery_items = []
    years_set = set()
    years_seen = set()  # 跟踪已经出现过的年份
    year_months_seen = {}  # 跟踪每年已经出现的月份 {year: set()}

    for date, date_label, image_url, metadata in images:
        blog_url = generate_blog_url(image_url)

        # 提取年份和月份信息
        year = date.strftime('%Y') if date != datetime.min else date_label[:4]
        month = date.strftime('%m') if date != datetime.min else date_label[4:6]

        # 使用 metadata 中的标题，如果没有则使用日期标签
        title = metadata.get('title', date_label)

        # 标记是否是该年份的第一个项目
        is_first_in_year = year not in years_seen
        if is_first_in_year:
            years_seen.add(year)

        # 标记是否是该年该月的第一个项目
        if year not in year_months_seen:
            year_months_seen[year] = set()
        is_first_in_month = month not in year_months_seen[year]
        if is_first_in_month:
            year_months_seen[year].add(month)

        gallery_items.append({
            'date': date_label,
            'image_url': image_url,
            'full_image_url': image_url,
            'blog_url': blog_url,
            'year': year,
            'month': month,
            'title': title,
            'is_first_in_year': is_first_in_year,
            'is_first_in_month': is_first_in_month
        })

        years_set.add(year)

    # 按年份排序（倒序）
    years = sorted(years_set, reverse=True)

    # 创建按年月分组的导航数据
    year_months = {}
    for item in gallery_items:
        year = item['year']
        month = item['month']
        if year not in year_months:
            year_months[year] = []
        if month not in year_months[year]:
            year_months[year].append(month)
    # 对每年的月份进行排序（倒序）
    for year in year_months:
        year_months[year].sort(reverse=True)

    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)
    html_content = template.render(items=gallery_items, years=years, year_months=year_months)

    # 写入输出文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    parser = argparse.ArgumentParser(
        description='生成交易历史图片展示页面（从博客 Markdown 文件中提取图片）'
    )
    parser.add_argument(
        '--blog-dir',
        type=Path,
        default=Path('docs/blog'),
        help='博客目录路径 (默认: docs/blog)'
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

    # 扫描博客目录
    images = scan_blog_directory(args.blog_dir)

    if not images:
        print("❌ 没有找到任何图片，退出")
        return

    print(f"✅ 找到 {len(images)} 张图片")

    # 排序
    print("📅 按日期排序...")
    sorted_images = sort_images_by_date(images)

    # 生成 HTML
    print(f"📝 生成 HTML 页面: {args.output}")
    try:
        render_html(sorted_images, args.template, args.output)
        print("✅ 页面生成成功！")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        raise

    print("=" * 50)
    print(f"🎉 完成！打开 {args.output} 查看结果")


if __name__ == '__main__':
    main()
