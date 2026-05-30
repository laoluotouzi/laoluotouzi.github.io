## Why

当前博客使用 MkDocs 构建，存在构建速度慢、依赖重、定制性差等问题。需要一个轻量的 Python3 静态博客生成器，直接读取 `docs/` 目录下的 markdown 文章和附件，生成纯静态 HTML 到 `blog/dist`，以获得更快的构建速度和更灵活的定制能力。

## What Changes

- 新增一个 Python3 静态博客生成服务，源代码放在 `blog/src/`
- 该服务读取 `docs/` 目录下的 markdown 文件（约 265 篇，按 `docs/blog/YYYY/MM/YYYYMMDD.md` 组织）及 `docs/attachments/` 下的附件
- 生成纯静态 HTML 文件到 `blog/dist/`
- 支持 markdown 解析、代码高亮、图片/附件引用、标签分类、按时间归档、RSS 订阅等博客核心功能

## Capabilities

### New Capabilities
- `markdown-parser`: 解析 markdown 文件，提取 frontmatter 元数据（标题、日期、标签等），将 markdown 转换为 HTML，支持代码高亮、图片链接重写、附件路径解析
- `site-generator`: 根据解析后的文章数据生成完整静态站点，包括文章详情页、首页列表、标签页、归档页、RSS feed，使用 Jinja2 模板引擎渲染 HTML
- `asset-pipeline`: 处理静态资源（CSS、JS、图片、附件），复制附件和图片到输出目录，保持正确的相对路径引用

### Modified Capabilities
（无现有能力被修改）

## Impact

- **代码**: 新增 `blog/src/` 目录下的 Python3 代码，包括生成器主程序、模板、静态资源
- **输出**: `blog/dist/` 目录将包含生成的静态 HTML 站点
- **依赖**: Python3，以及 markdown 解析库（如 markdown 或 mistune）、模板引擎（如 Jinja2）、代码高亮库（如 Pygments）等
- **数据源**: 读取现有的 `docs/` 目录内容，不修改原始文件
- **构建流程**: 可与现有 MkDocs 构建并存，不影响当前部署流程
