## Context

当前博客站点使用纯 CSS（无预处理器）+ Flexbox 布局，已有基础的移动端适配：viewport meta 标签、768px 和 480px 两个媒体查询断点。导航栏有 6 个链接（首页、历史、标签、归档、关于、RSS），当前在 768px 以下会换行显示。history 页面使用内联 `<style>` 而非全局 CSS。项目无前端框架，JS 极简（仅外链新窗口打开）。

目标移动端分辨率覆盖：iPhone SE (320px)、iPhone 6/7/8 (375px)、iPhone X/11/12 (390px)、iPhone 14/15 Pro Max (430px)、常见安卓设备 (360px-412px)。

## Goals / Non-Goals

**Goals:**
- 所有页面在 320px-430px 宽度下布局合理、内容可读、交互可用
- 导航栏在小屏幕下不换行、不溢出
- 文章内容（表格、代码块、图片）在小屏下不破坏布局
- history 页面的年份标签栏在小屏下可操作
- 最小化改动，不引入新的 JS 依赖或 CSS 框架

**Non-Goals:**
- 不做深色模式
- 不做 PWA 或离线支持
- 不改变桌面端现有样式
- 不引入 CSS 预处理器（Sass/Less）或构建工具
- 不重新设计页面布局结构

## Decisions

### 1. 导航栏：汉堡菜单 vs 横向滚动

**选择：横向滚动**

汉堡菜单需要修改 HTML 模板（添加 toggle 按钮）和 JS（添加展开/收起逻辑），增加了复杂度。当前只有 6 个导航项，总宽度约 300px，在大多数移动设备上刚好放得下或略溢出。

实现方式：给 `.site-nav` 添加 `overflow-x: auto`、`white-space: nowrap`、隐藏滚动条（`-webkit-overflow-scrolling: touch` + scrollbar 隐藏），768px 以下生效。导航链接不换行，超宽时用户可横向滑动。这比汉堡菜单改动更小，且 6 个链接完全可滑动浏览。

**替代方案：** 汉堡菜单（更规整但改动大，且 6 个链接不需要折叠）。

### 2. 断点策略：保留现有断点 + 细化小屏

**选择：保留 768px/480px，在 480px 以下新增 375px 断点**

现有 768px 断点处理平板到大屏手机的过渡（sidebar 堆叠），480px 处理小屏手机。新增 375px 断点处理 iPhone SE 等极小屏幕的字号和间距调整。

不使用 640px 断点，因为 640px-768px 区间已有 768px 断点覆盖，且该区间主要是大屏手机横屏或小平板，现有 flex-direction: column 布局已足够。

**替代方案：** 添加 640px 断点（不必要，增加维护成本）。

### 3. 表格溢出处理

**选择：`.post-content table` 外层包裹可滚动容器**

使用 CSS `overflow-x: auto` 包裹表格。具体做法：不修改模板 HTML，而是给 `.post-content` 设置 `overflow-x: hidden`，然后给 `.post-content table` 的父级元素（或直接对 table 使用 `display: block; overflow-x: auto`）。

实际上最简单的做法是在 CSS 中为 `.post-content` 内的 table 添加一个包裹样式。但纯 CSS 无法自动添加包裹元素。因此采用另一种方式：直接给 `.post-content` 设置 `overflow-x: auto`，让内容可横向滚动。但这会影响所有内容。

**最终方案：** 通过 JS 在构建时或页面加载时，找到 `.post-content` 内的所有 `<table>`，将其包裹在 `<div class="table-wrap">` 中，然后 CSS 给 `.table-wrap` 设置 `overflow-x: auto`。在 `main.js` 中添加这段逻辑。

**替代方案：** 纯 CSS 方案（给 `.post-content` 整体加 overflow-x，但会影响段落文本换行行为）。

### 4. history 页面内联样式处理

**选择：保留内联样式，在内联 `<style>` 块中添加媒体查询**

history.html 有约 140 行内联 CSS。将这些样式迁移到 style.css 虽然更整洁，但改动范围大且不必要。直接在内联 `<style>` 块末尾添加 `@media` 规则即可。

**替代方案：** 迁移到 style.css（改动大，收益不明显）。

### 5. Post-nav 小屏适配

**选择：768px 以下改为垂直堆叠**

当前 post-nav 是 `display: flex; justify-content: space-between` 水平排列。768px 以下改为 `flex-direction: column`，两个导航项上下堆叠，各占 100% 宽度。

### 6. 分页组件小屏适配

**选择：缩小按钮尺寸，隐藏省略号间距**

480px 以下将分页按钮的 min-width 从 36px 减至 32px，高度从 36px 减至 32px，字体缩小。

## Risks / Trade-offs

- **横向滚动导航可能不被用户发现** → 通过 CSS 隐藏滚动条但保留滚动功能，导航项足够短不会明显溢出；如后续导航项增加可再升级为汉堡菜单
- **JS 包裹 table 可能影响已有页面结构** → 只针对 `.post-content > table` 操作，不影响其他区域的表格；包裹前检查是否已被包裹
- **history 内联样式的媒体查询可能与全局样式冲突** → history 页面的 CSS 类名都是 `.history-*` 前缀，与全局样式隔离良好，冲突风险低
- **不引入 CSS 变量** → 当前样式维护成本可接受，后续如果主题化需求增加可再引入
