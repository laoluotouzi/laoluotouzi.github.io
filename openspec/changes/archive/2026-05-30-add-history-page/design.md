## Context

博客使用 Python 静态站点生成器，构建流程为 `generator.py` → `parser.py` → `renderer.py` → 输出到 `blog/dist/`。现有页面类型包括首页（分页）、文章详情、标签页、归档页和关于页。

`history/` 目录下有一个独立的生成器 `generate.py`，通过正则匹配 `![目前持仓|持仓股票明细](...)` 从周记文章中提取持仓图片，生成一个完全独立样式的静态 HTML 页面。目标是将此功能整合到博客构建系统中，使用统一的模板和样式。

关键约束：
- Post 模型中 `content_html` 已经过 mistune 渲染，图片路径已被 `resolve_relative_paths` 转换为站点绝对路径（如 `/attachments/2026/03/20260307/1.png`）
- 博客模板继承 `base.html`，使用 Jinja2，通过 `?v={{ version }}` 做缓存 busting
- 现有分页机制使用 `_build_page_range()` 工具函数，每页 10 篇

## Goals / Non-Goals

**Goals:**
- 在博客站点内新增 `/history/` 页面，展示所有周记的持仓快照
- 页面样式与博客完全一致（继承 `base.html`，包含 sidebar）
- 按年月分组展示，支持分页
- 图片支持点击放大查看（lightbox）
- 从已解析的 Post 数据中提取图片信息，复用现有构建管线

**Non-Goals:**
- 不改变 `history/` 目录下的独立生成器（保持向后兼容）
- 不修改 Post 数据模型或 parser 的核心逻辑
- 不引入新的 Python 依赖

## Decisions

### 1. 图片提取方式：从 `content_html` 中正则匹配

**选择**: 在 `renderer.py` 的 `render_history()` 中，从已渲染的 `post.content_html` 用正则提取持仓图片 URL。

**替代方案**:
- 在 `parser.py` 阶段提取并存储到 Post 模型 → 需要修改 parser 和模型，增加耦合
- 重新读取原始 Markdown 文件 → 需要额外的文件 I/O，且路径需要重新解析

**理由**: Post 的 `content_html` 中图片路径已经被 `resolve_relative_paths` 转换为站点绝对路径（`/attachments/...`），直接匹配 `<img>` 标签的 alt 属性即可，无需额外路径处理。这是最小侵入的方式。

匹配规则：在 `content_html` 中搜索 `<img` 标签，alt 属性包含"目前持仓"或"持仓股票明细"的图片。

### 2. 数据模型：新增 `HistoryItem` 数据类

**选择**: 在 `models.py` 中新增 `HistoryItem` 数据类，包含 `post`（关联 Post）、`image_url`（持仓图片路径）、`date`、`title`。

**理由**: 解耦渲染逻辑和数据提取，便于模板使用。每个 HistoryItem 对应一篇周记中的一张持仓图。

### 3. 页面结构：按年分组的单层分页

**选择**: `/history/` 为总览页（所有快照按时间倒序，分页），每个分页页面 `/history/page/2/` 等。

**替代方案**:
- 按年/月二级导航（类似 archive 页面的 `/history/2026/`）→ 快照数量通常不多，二级导航过于复杂
- 单页无分页全部展示 → 快照图片较多时加载慢

**理由**: 参考原 `history/generate.py` 的设计，图片以时间倒序单列展示，加上分页控制加载量。保留年月分组标记用于视觉分隔（如"2026年3月"分组标题），不做独立的年月页面。

### 4. 模板设计：新建 `history.html` 继承 `base.html`

**选择**: 创建 `history.html` 模板，继承 `base.html`，包含 sidebar。页面主体展示持仓快照卡片列表（日期标题 + 图片 + 查看原文链接），支持 lightbox 放大。

**理由**: 与其他页面保持一致的布局结构。sidebar 中的"归档"widget 可用于快速跳转到对应年份的文章。

### 5. Lightbox 实现：复用现有静态资源模式

**选择**: 在 `history.html` 模板中内嵌 lightbox 的 CSS 和 JS（类似原 `history/template.html` 的实现方式），或放入 `main.js` 中统一管理。

**理由**: lightbox 功能仅历史页面使用，内嵌到模板中避免影响其他页面的 JS 体积。也可以添加到 `main.js` 中，通过 CSS class 控制只在 history 页面激活。优先选择添加到模板内嵌 script 中，保持独立性。

## Risks / Trade-offs

- **图片提取依赖正则匹配 HTML** → 如果 mistune 版本升级改变了 `<img>` 标签的输出格式，正则需要更新。缓解：使用较宽松的匹配模式。
- **Post 列表中非周记文章也会被遍历** → 通过关键字过滤（`content_html` 中包含"老罗投资周记"或"老罗实盘周记"）来跳过非周记文章，与原 `generate.py` 逻辑一致。
- **历史页面图片加载可能较慢** → 使用 `loading="lazy"` 属性和分页来控制。缓解：每页展示 10 条快照。
