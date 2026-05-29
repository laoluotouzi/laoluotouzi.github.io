# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"老罗投资" 静态博客站点，使用自定义 Python 静态站点生成器构建。部署在 GitHub Pages（主分支 `gh-pages`）和 Gitee Pages。

## Build Commands

```bash
# 构建（需要 Python 3.11）
python3.11 blog/src/generator.py build

# 清理输出
python3.11 blog/src/generator.py clean

# 构建并启动本地预览（端口 8080）
bash blog/preview.sh
```

依赖安装：`pip install -r blog/src/requirements.txt`（mistune, Jinja2, Pygments, PyYAML）

## Architecture

### Build Pipeline (`blog/src/generator.py`)

构建流程：Clean → Parse posts → Copy assets → Build sidebar → Render pages → RSS

1. **`parser.py`** — 扫描 `docs/blog/YYYY/MM/YYYYMMDD.md`，解析 YAML frontmatter（title/date/tags/banner），用 mistune 转 HTML，用 Pygments 做代码高亮，解析相对路径（attachments 引用）
2. **`renderer.py`** — Jinja2 模板渲染：首页（分页）、文章详情（上下篇）、标签页（分页）、归档页（按年/月分页）、关于页。侧边栏包含最近文章、热门标签、归档年份、社交媒体
3. **`asset_manager.py`** — 清理 dist 目录，复制 `docs/attachments/` 和 `blog/src/static/` 到 `blog/dist/`
4. **`feed.py`** — 生成 RSS 2.0 XML（最新 20 篇）
5. **`models.py`** — 数据类 `Post`、`Tag`、`Archive`，Post URL 自动生成为 `/blog/YYYY/MM/YYYYMMDD/`

### Content Structure

- **文章源文件**: `docs/blog/YYYY/MM/YYYYMMDD.md`（frontmatter 可缺省，会从文件名推断日期、从正文推断标题）
- **附件**: `docs/attachments/`（文章中的图片等）
- **模板**: `blog/src/templates/`（`base.html` 为基础模板，其他模板继承它）
- **静态资源**: `blog/src/static/`（CSS、JS、图片）
- **构建输出**: `blog/dist/`

### Key Conventions

- CSS/JS 通过 `?v={{ version }}` 做缓存 busting（version 为构建时间戳）
- 标签 slug 使用 `urllib.parse.quote` 处理中文
- 每页 10 篇文章，分页支持省略号
- 文章按日期降序排列，文章详情页有上下篇导航
