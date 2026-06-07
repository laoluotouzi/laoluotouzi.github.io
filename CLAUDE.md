# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供项目指导。

## 项目概览

"老罗投资" 静态博客站点，使用自定义 Python 静态站点生成器构建。部署在 GitHub Pages（分支 `gh-pages`）和 Gitee Pages。

站点地址：`https://invest.zdyi.com`

## 构建命令

```bash
# 构建（需要 Python 3.11）
python3.11 blog/src/generator.py build

# 清理输出
python3.11 blog/src/generator.py clean

# 构建并启动本地预览（端口 8080）
bash blog/preview.sh
```

依赖安装：`pip install -r blog/src/requirements.txt`（mistune>=3.0, Jinja2>=3.0, Pygments>=2.0, PyYAML>=6.0）

## 项目结构

```
├── blog/
│   ├── src/                        # 构建源码（共约 1018 行 Python）
│   │   ├── generator.py            # CLI 入口，编排完整构建流程（122 行）
│   │   ├── renderer.py             # Jinja2 模板渲染（所有页面类型，467 行）
│   │   ├── parser.py               # Markdown 解析 + frontmatter 提取（225 行）
│   │   ├── models.py               # 数据模型（Post, Tag, Archive, HistoryItem，75 行）
│   │   ├── asset_manager.py        # 静态资源复制与目录管理（54 行）
│   │   ├── feed.py                 # RSS 2.0 生成器（39 行）
│   │   ├── sitemap.py              # sitemap.xml 生成器（36 行）
│   │   ├── requirements.txt        # Python 依赖
│   │   ├── templates/              # Jinja2 模板（9 个）
│   │   │   ├── base.html           # 基础模板（头部导航、侧边栏、底部）
│   │   │   ├── history.html        # 持仓历史图库页（含 lightbox，最大模板）
│   │   │   ├── index.html          # 首页（文章列表 + 分页）
│   │   │   ├── tag.html            # 单个标签页
│   │   │   ├── archive.html        # 年/月归档页
│   │   │   ├── post.html           # 文章详情页
│   │   │   ├── archive_index.html  # 归档索引页
│   │   │   ├── tags_index.html     # 标签索引页
│   │   │   └── about.html          # 关于页
│   │   └── static/
│   │       ├── style.css           # 主样式表（1083 行）
│   │       ├── main.js             # JS 工具（外链新窗口、表格滚动，28 行）
│   │       └── assets/images/      # 静态图片（10 个文件：logo、favicon、社交图标、about.gif、smile_curve.jpeg）
│   ├── preview.sh                  # 本地预览脚本
│   └── dist/                       # 构建输出（被 git 跟踪，.gitignore 中用 `!blog/dist` 排除忽略）
├── docs/
│   ├── blog/YYYY/MM/YYYYMMDD.md   # 文章源文件（2022-2026）
│   ├── attachments/YYYY/MM/       # 文章附件（图片等）
│   ├── about/index.md             # 关于页源文件
│   ├── index.md                   # 首页源文件（MkDocs 遗留，当前生成器未使用）
│   ├── favicon.ico                # 站点图标
│   ├── robots.txt                 # 爬虫规则
│   ├── tags/                      # 标签页源文件（MkDocs 遗留，含 index.md、cloud.md）
│   └── assets/                    # 其他静态资源（MkDocs 遗留，含 extra.css/js、view-bigimg 插件、mathjax.js、website-statistics.js）
└── .gitignore
```

## 构建流程

`generator.py build` 执行以下步骤：

1. **Clean** — 删除并重建 `blog/dist/`
2. **Parse** — 扫描 `docs/blog/YYYY/MM/YYYYMMDD.md`，解析所有文章
3. **Copy Assets** — 复制 attachments、static、robots.txt 到 dist
4. **Build Sidebar** — 构建侧边栏数据（最近 5 篇、热门标签 Top 20、归档年份）
5. **Render** — 渲染所有 HTML 页面（文章详情、首页、标签、归档、持仓历史、关于）
6. **RSS** — 生成 `feed.xml`（最新 20 篇）
7. **Sitemap** — 生成 `sitemap.xml`

## 核心模块说明

### `models.py` — 数据模型

- **`Post`**：文章（title, date, slug, tags, banner, content_html, url 等）
  - `slug` 默认从日期生成（`YYYYMMDD`）
  - `url` 自动生成为 `/blog/YYYY/MM/YYYYMMDD/`（支持同日多篇如 `YYYYMMDD_1`）
- **`Tag`**：标签（name, slug, posts 列表）
- **`Archive`**：归档（year, month, posts 列表），自动生成 url 和 title
- **`HistoryItem`**：持仓快照（关联 Post + 图片 URL），从周记中提取

### `parser.py` — Markdown 解析

- `scan_posts()`：递归扫描 `docs/blog/YYYY/MM/` 下的 `.md` 文件
- `parse_frontmatter()`：提取 YAML frontmatter（`---` 分隔）
- `parse_post()`：将 Markdown 文件转为 Post 对象
  - 用 mistune 渲染 Markdown（启用 table、mark 插件）
  - 用 Pygments 做代码语法高亮
  - `resolve_relative_paths()`：将相对路径（如 `../../../attachments/`）转为站点绝对路径（`/attachments/`）
  - frontmatter 可缺省：日期从文件名推断，标题从正文第一个 `#` 标题推断
  - 支持 banner 图片路径解析
- `parse_about_page()`：解析关于页

### `renderer.py` — 页面渲染

- `create_env()`：创建 Jinja2 环境，注册自定义过滤器（`tag_slug`、`truncate`）
- `_build_page_range()`：智能分页算法，显示最多 5 个页码 + 省略号
- `render_posts()`：渲染文章详情页，带上下篇导航
- `render_index()`：渲染首页（分页）
- `render_tags()`：渲染标签索引页 + 各标签详情页（分页）
- `render_archives()`：渲染归档索引 + 年归档 + 月归档（全部支持分页）
- `_extract_history_items()`：从 Markdown 源文件中提取包含"目前持仓"或"持仓股票明细"alt 的图片
- `render_history()`：按年份渲染持仓历史图库页，默认显示当年
- `render_about()`：渲染关于页

### `asset_manager.py` — 资源管理

- `clean_output()`：删除并重建 dist 目录
- `copy_attachments()`：复制 `docs/attachments/` → `dist/attachments/`
- `copy_static()`：复制 `blog/src/static/` → `dist/static/`
- `copy_robots_txt()`：复制 robots.txt
- `url_encode_path()`：CJK 字符的 URL 编码

### `feed.py` — RSS 生成

生成 RSS 2.0 XML，包含 atom:self 链接，最新 20 篇文章。

### `sitemap.py` — Sitemap 生成

生成标准 sitemap.xml，首页 priority 1.0，文章页 priority 0.8。

## URL 结构

| 页面类型 | URL 模式 | 示例 |
|---------|---------|------|
| 首页 | `/` 或 `/page/N/` | `/page/2/` |
| 文章详情 | `/blog/YYYY/MM/YYYYMMDD/` | `/blog/2026/06/20260606/` |
| 标签索引 | `/tags/` | — |
| 标签详情 | `/tags/标签名/` 或 `/tags/标签名/page/N/` | `/tags/实盘周记/` |
| 归档索引 | `/archive/` | — |
| 年归档 | `/archive/YYYY/` | `/archive/2026/` |
| 月归档 | `/archive/YYYY/MM/` | `/archive/2026/06/` |
| 持仓历史 | `/history/` 或 `/history/YYYY/` | `/history/2026/` |
| 关于 | `/about/` | — |
| RSS | `/feed.xml` | — |
| Sitemap | `/sitemap.xml` | — |

## 文章 Frontmatter 格式

```yaml
---
title: 文章标题
date: 2026-06-06
tags:
  - 标签1
  - 标签2
banner: ../attachments/2026/06/20260606/banner.jpg
description: 文章描述
comments: true
---

正文内容...
```

frontmatter 可全部缺省：日期从文件名推断，标题从正文第一个 `#` 标题推断，tags 默认为空。

## 关键约定

- **缓存 busting**：CSS/JS 通过 `?v={{ version }}` 做缓存控制（version 为构建时间戳 `%Y%m%d%H%M%S`）
- **中文标签**：标签 slug 使用 `urllib.parse.quote` 处理中文（如 `实盘周记` → `%E5%AE%9E%E7%9B%98%E5%91%A8%E8%AE%B0`）
- **分页**：每页 10 篇文章，智能分页显示最多 5 个页码 + 省略号
- **文章排序**：按日期降序，文章详情页有上下篇导航
- **同日多篇**：文件名支持 `YYYYMMDD_1`、`YYYYMMDD_2` 后缀
- **路径解析**：Markdown 中的相对附件路径自动转换为站点绝对路径
- **dist 被跟踪**：`blog/dist/` 目录被 git 跟踪，构建产物直接提交

## Git 分支策略

- **`main`**：开发分支（当前工作分支）
- **`gh-pages`**：GitHub Pages 部署分支（远程默认分支）

## 前端技术

- 纯原生 CSS + JS，无框架依赖
- 响应式设计（移动端适配）
- 主色调：红色 `#c0392b`
- 自定义 Pygments 代码高亮主题
- 社交媒体链接：微信公众号、B站、小红书、抖音、快手、雪球
- 评论系统：cwd-widget
