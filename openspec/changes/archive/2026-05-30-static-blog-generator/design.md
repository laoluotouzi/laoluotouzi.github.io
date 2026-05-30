## Context

当前项目是一个基于 MkDocs + Material 主题的个人投资博客（GitHub Pages），`docs/` 目录包含约 265 篇 markdown 文章，按 `docs/blog/YYYY/MM/YYYYMMDD.md` 结构组织，附件存放在 `docs/attachments/YYYY/MM/YYYYMMDD/` 下。文章使用 YAML frontmatter 记录元数据（title、description、banner、date、tags），图片引用使用相对路径（如 `../../../../attachments/2025/01/20250104/banner.jpeg`）。

需要新建一个独立的 Python3 静态博客生成器，源代码放在 `blog/src/`，生成 HTML 到 `blog/dist/`，与现有 MkDocs 构建并存、互不影响。

## Goals / Non-Goals

**Goals:**
- 用纯 Python3 实现一个轻量的静态博客生成器，零外部构建工具依赖
- 正确解析现有 `docs/` 下的所有 markdown 文章和 frontmatter 元数据
- 生成完整的静态博客站点：文章详情页、首页列表（分页）、标签页、年月归档页、RSS feed
- 正确处理图片和附件的路径映射，从 `docs/` 的相对路径转换为 `blog/dist/` 下的正确路径
- 支持代码高亮
- 保持与现有 MkDocs 站点独立，不修改原始 `docs/` 文件

**Non-Goals:**
- 不替换现有 MkDocs 构建流程
- 不支持评论系统（保持 Disqus 在原站点）
- 不支持加密内容
- 不做服务端渲染或动态功能
- 不支持自定义主题系统（仅内置一套简洁主题）

## Decisions

### 1. Markdown 解析库选择：mistune

**选择**: mistune v3
**备选**: python-markdown、markdown-it-py
**理由**: mistune 速度快、API 简洁、原生支持插件扩展（目录、任务列表、数学公式等），且纯 Python 实现无需编译。相比 python-markdown 更轻量，相比 markdown-it-py 更容易定制渲染器。

### 2. 模板引擎：Jinja2

**选择**: Jinja2
**备选**: 手写字符串拼接、string.Template
**理由**: Jinja2 是 Python 生态最成熟的模板引擎，支持模板继承、宏、过滤器，方便构建博客的页面布局体系（base → page/list/detail）。

### 3. 代码高亮：Pygments

**选择**: Pygments
**备选**: highlight.js（前端 JS 方案）、Prism.js
**理由**: 构建时生成高亮 HTML，无需客户端 JS 依赖，减少页面加载负担。Pygments 与 mistune 可直接集成。后续如需前端高亮也可切换，但构建时高亮更适合静态站点的性能目标。

### 4. 项目结构

```
blog/src/
├── generator.py          # CLI 入口，解析参数，调度构建流程
├── parser.py             # Markdown 解析与 frontmatter 提取
├── renderer.py           # 页面渲染逻辑，调用 Jinja2 模板
├── models.py             # 数据模型：Post, Tag, Archive 等
├── asset_manager.py      # 静态资源与附件处理
├── feed.py               # RSS feed 生成
├── templates/            # Jinja2 模板目录
│   ├── base.html         # 基础布局
│   ├── index.html        # 首页（文章列表）
│   ├── post.html         # 文章详情页
│   ├── tag.html          # 标签页
│   ├── archive.html      # 归档页
│   └── feed.xml          # RSS feed 模板
└── static/               # 静态资源（CSS、JS）
    ├── style.css
    └── main.js
```

**理由**: 模块化清晰，每个文件职责单一，便于独立测试和维护。模板和静态资源内置在 `blog/src/` 下，生成时复制到 `blog/dist/`。

### 5. 路径映射策略

文章中的附件引用路径（如 `../../../../attachments/2025/01/20250104/banner.jpeg`）需要映射到输出目录。

**方案**: 解析阶段将所有相对路径规范化为基于 `docs/` 的绝对路径，渲染阶段将这些路径重写为 `/attachments/YYYY/MM/YYYYMMDD/filename` 的 URL 路径。附件文件直接从 `docs/attachments/` 复制到 `blog/dist/attachments/`，保持目录结构一致。

### 6. 构建流程

```
1. 扫描 docs/blog/YYYY/MM/*.md → 收集所有文章路径
2. 解析每篇文章 → 提取 frontmatter + 转换 markdown 为 HTML
3. 构建索引 → 按日期排序、标签分组、年月归档
4. 复制附件 → docs/attachments/ → blog/dist/attachments/
5. 渲染页面 → Jinja2 模板 + 文章数据 → 生成 HTML
6. 复制静态资源 → blog/src/static/ → blog/dist/static/
7. 生成 RSS feed → blog/dist/feed.xml
```

### 7. CLI 接口

```bash
python3 blog/src/generator.py build              # 完整构建
python3 blog/src/generator.py build --watch       # 监听文件变化自动重建
python3 blog/src/generator.py clean               # 清理 blog/dist/
```

## Risks / Trade-offs

- **[相对路径解析复杂]** → 解析 markdown 中的链接和图片引用时，需要正确处理不同层级文章的相对路径。通过在解析阶段统一规范化为基于 `docs/` 的路径来缓解。
- **[frontmatter 格式不一致]** → 部分早期文章的 frontmatter 可能缺少某些字段或格式不同。解析器需要容错处理，对缺失字段使用合理默认值。
- **[附件路径中包含中文或特殊字符]** → URL 编码处理，确保生成的路径在浏览器中可正常访问。
- **[构建速度]** → 约 265 篇文章的解析和渲染应在秒级完成。如有性能问题，后续可引入增量构建（仅重建变化的文章）。
- **[与 MkDocs 共存]** → `blog/dist/` 作为独立输出目录，不与 `site/`（MkDocs 输出）冲突，两者完全独立。
