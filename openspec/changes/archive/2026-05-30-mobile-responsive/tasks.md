## 1. 导航栏响应式

- [x] 1.1 修改 `blog/src/static/style.css` 中 768px 媒体查询的 `.site-header .container` 样式，移除 `flex-direction: column` 和 `gap: 8px`，保持水平排列
- [x] 1.2 在 768px 媒体查询中为 `.site-nav` 添加横向滚动样式：`overflow-x: auto`、`white-space: nowrap`、隐藏滚动条（`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`）
- [x] 1.3 在 768px 媒体查询中为 `.site-nav a` 添加 `flex-shrink: 0`，防止导航链接被压缩

## 2. 768px 断点优化

- [x] 2.1 修改 `blog/src/static/style.css` 中 768px 媒体查询的 `.post-nav`，添加 `flex-direction: column`，设置 `.post-nav-item` 的 `max-width: 100%`
- [x] 2.2 在 768px 媒体查询中为 `.post-nav-next` 添加 `text-align: left` 和 `margin-left: 0`

## 3. 375px 极小屏断点

- [x] 3.1 在 `blog/src/static/style.css` 末尾新增 `@media (max-width: 375px)` 媒体查询块
- [x] 3.2 在 375px 断点中隐藏 `.post-card-thumb`（`display: none`）
- [x] 3.3 在 375px 断点中减小 `.post-card-title` 字号（`font-size: 1.05em`）
- [x] 3.4 在 375px 断点中减小分页按钮尺寸：`.pagination-page` 的 `min-width: 32px`、`height: 32px`、`font-size: 0.82em`
- [x] 3.5 在 375px 断点中减小 `.pagination-pages` 的 `gap: 2px`
- [x] 3.6 在 375px 断点中减小 `.post` 的 padding 为 `16px`
- [x] 3.7 在 375px 断点中减小 `.post-title` 字号为 `1.15em`
- [x] 3.8 在 375px 断点中减小 `.page-title` 字号为 `1.15em`

## 4. 表格横向滚动

- [x] 4.1 在 `blog/src/static/style.css` 中添加 `.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 1em; }` 样式
- [x] 4.2 在 `blog/src/static/main.js` 的 DOMContentLoaded 回调中添加逻辑：查找 `.post-content` 内的所有 `<table>` 元素，对每个未被 `.table-wrap` 包裹的 table 创建包裹 div

## 5. History 页面移动端适配

- [x] 5.1 在 `blog/src/templates/history.html` 的内联 `<style>` 末尾添加 `@media (max-width: 640px)` 媒体查询，为 `.history-year-tabs` 添加 `overflow-x: auto`、`white-space: nowrap`、隐藏滚动条
- [x] 5.2 在 `.history-year-tab a` 的 640px 断点中添加 `flex-shrink: 0` 防止标签被压缩
- [x] 5.3 在 history.html 内联样式中添加 `@media (max-width: 480px)` 媒体查询，减小 `.history-card-header` padding（`8px 12px`）和 `.history-card-image` padding（`8px`）
- [x] 5.4 在 480px 断点中减小 `.history-card-date` 字号为 `0.9rem`、`.history-card-link` 字号为 `0.8rem`
