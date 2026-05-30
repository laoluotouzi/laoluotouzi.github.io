## 1. 项目初始化与依赖配置

- [x] 1.1 创建 `blog/src/` 目录结构（generator.py、parser.py、renderer.py、models.py、asset_manager.py、feed.py、templates/、static/）
- [x] 1.2 创建 `blog/src/requirements.txt`，声明依赖：mistune>=3.0、Jinja2>=3.0、Pygments>=2.0、PyYAML>=6.0
- [x] 1.3 实现 `models.py` 数据模型：Post（title, date, tags, banner, description, content_html, source_path）、Tag（name, slug, posts）、Archive（year, month, posts）

## 2. Markdown 解析器（parser.py）

- [x] 2.1 实现 `scan_posts()` 函数，递归扫描 `docs/blog/YYYY/MM/` 目录，收集所有 `YYYYMMDD.md` 文件路径并按文件名排序
- [x] 2.2 实现 `parse_frontmatter()` 函数，提取 YAML frontmatter（title, description, banner, date, tags, comments），对缺失字段使用合理默认值，支持无 frontmatter 的文章
- [x] 2.3 实现 `parse_markdown()` 函数，使用 mistune v3 将 markdown 内容转换为 HTML，支持标准 markdown 语法（标题、段落、列表、链接、图片、粗体、斜体、引用、表格、水平线、行内 HTML）
- [x] 2.4 集成 Pygments 代码高亮，检测 fenced code block 的语言标识，生成带 CSS class 的语法高亮 HTML；无语言标识时输出纯 `<pre><code>` 块
- [x] 2.5 实现相对路径解析，根据源文件位置将图片和链接的相对路径规范化为基于 `docs/` 的路径（如 `../../../../attachments/...` → `attachments/...`）
- [x] 2.6 实现 `parse_post()` 顶层函数，组合以上功能：扫描 → 解析 frontmatter → 转换 markdown → 解析路径 → 返回 Post 对象列表

## 3. 资源管理（asset_manager.py）

- [x] 3.1 实现附件复制功能，将 `docs/attachments/` 整体复制到 `blog/dist/attachments/`，保持 `YYYY/MM/YYYYMMDD/` 目录结构，以二进制模式复制文件
- [x] 3.2 实现静态资源复制功能，将 `blog/src/static/`（CSS、JS）复制到 `blog/dist/static/`，保持目录结构
- [x] 3.3 实现 HTML 内容中的图片路径重写，将基于 `docs/` 的路径转换为输出页面可正确访问的 URL 路径
- [x] 3.4 实现 URL 编码处理，对包含中文或特殊字符的文件名进行 percent-encoding，磁盘文件保持原名
- [x] 3.5 实现 clean build 模式，构建前删除整个 `blog/dist/` 目录再重新创建

## 4. Jinja2 模板（templates/）

- [x] 4.1 创建 `base.html` 基础布局模板，包含 HTML head（meta、CSS 引用）、header（站点标题、导航）、footer、可覆盖的 content block
- [x] 4.2 创建 `post.html` 文章详情页模板，继承 base.html，展示标题、日期、标签、banner 图片、正文内容
- [x] 4.3 创建 `index.html` 首页模板，继承 base.html，展示文章列表（标题、日期、摘要、banner 缩略图）和分页导航
- [x] 4.4 创建 `tag.html` 标签页模板，展示标签下的文章列表
- [x] 4.5 创建 `archive.html` 归档页模板，按年/月展示文章列表
- [x] 4.6 创建 `feed.xml` RSS feed 模板，输出 RSS 2.0 格式 XML

## 5. 页面渲染（renderer.py）

- [x] 5.1 实现 Jinja2 Environment 初始化，配置模板加载路径为 `blog/src/templates/`，注册自定义过滤器（日期格式化、URL 编码等）
- [x] 5.2 实现文章详情页渲染，为每篇文章生成 `blog/dist/posts/YYYY/MM/YYYYMMDD/index.html`
- [x] 5.3 实现首页渲染与分页，每页 10 篇文章，生成 `blog/dist/index.html` 和 `blog/dist/page/N/index.html`
- [x] 5.4 实现标签索引页渲染，生成 `blog/dist/tags/index.html`（所有标签列表含文章数）和 `blog/dist/tags/<slug>/index.html`（每个标签的文章列表）
- [x] 5.5 实现归档页渲染，生成 `blog/dist/archive/YYYY/index.html` 和 `blog/dist/archive/YYYY/MM/index.html`

## 6. RSS Feed 生成（feed.py）

- [x] 6.1 实现 RSS 2.0 feed 生成，输出最近 20 篇文章的 title、绝对 URL、description、pubDate 到 `blog/dist/feed.xml`

## 7. CLI 入口与构建编排（generator.py）

- [x] 7.1 实现 CLI 参数解析，支持 `build` 和 `clean` 子命令，使用 argparse
- [x] 7.2 实现 `build` 命令的完整构建流程编排：扫描 → 解析 → 构建索引 → 复制附件 → 复制静态资源 → 渲染页面 → 生成 RSS
- [x] 7.3 实现 `clean` 命令，删除 `blog/dist/` 目录
- [x] 7.4 创建 `blog/src/static/style.css` 基础样式文件（排版、布局、代码高亮、响应式）
- [x] 7.5 创建 `blog/src/static/main.js` 基础脚本文件

## 8. 集成验证

- [x] 8.1 运行 `python3 blog/src/generator.py build` 对现有 `docs/` 数据执行完整构建，验证输出到 `blog/dist/`
- [x] 8.2 检查生成的文章详情页：确认所有约 265 篇文章正确生成，frontmatter 元数据完整，图片路径可访问
- [x] 8.3 检查首页分页、标签页、归档页导航链接正确性
- [x] 8.4 检查 RSS feed 格式有效性
- [x] 8.5 本地浏览器预览 `blog/dist/index.html`，确认页面显示正常
