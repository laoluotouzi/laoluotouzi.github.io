## Why

博客站点已有基础的移动端适配（viewport meta 标签、768px/480px 两个媒体查询断点），但覆盖面不够全面，部分页面和组件在主流移动端分辨率（320px-428px）下体验不佳。需要系统性完善所有页面的移动端响应式样式。

## What Changes

- 补充更多断点覆盖：在现有 768px 和 480px 之间增加 640px 断点，并细化 480px 以下（特别是 320px-375px 小屏手机）的样式
- 改进导航栏：小屏幕下顶部导航链接可能溢出或换行，需要添加汉堡菜单或横向滚动
- 优化文章卡片列表：480px 以下缩略图布局调整，卡片间距和字号适配
- 优化文章详情页：正文表格在移动端需支持横向滚动，代码块已有 overflow-x 但需确认小屏表现，文章内图片间距优化
- 优化历史持仓页：年份标签栏（tabs）在移动端需要横向可滚动，卡片头部和图片在小屏下的间距
- 优化侧边栏：移动端侧边栏移到下方后，widget 之间的间距和内边距需要更紧凑
- 优化分页组件：小屏下分页按钮尺寸和间距适配
- 优化 post-nav（上下篇导航）：小屏下改为垂直堆叠布局
- 统一 history.html 中内联样式的移动端适配（该页面使用内联 CSS，未走全局 style.css）

## Capabilities

### New Capabilities
- `responsive-layout`: 移动端响应式布局能力，涵盖断点策略、导航栏移动端适配、各组件小屏适配、横向溢出处理等

### Modified Capabilities

## Impact

- `blog/src/static/style.css` — 主要修改文件，补充和完善媒体查询规则
- `blog/src/templates/history.html` — 内联样式部分的移动端适配
- `blog/src/templates/base.html` — 可能需要添加汉堡菜单 HTML 结构
- `blog/src/static/main.js` — 可能需要添加汉堡菜单的展开/收起 JS 逻辑
