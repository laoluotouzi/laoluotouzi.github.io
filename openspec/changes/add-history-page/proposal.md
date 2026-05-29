## Why

目前博客中"老罗投资周记/实盘周记"系列的持仓截图只能通过 `history/` 目录下的独立生成器生成一个样式完全不同的独立页面查看。用户希望在博客站点内直接访问历史持仓快照页面，样式与现有博客保持一致，且能从主导航栏进入。

## What Changes

- 在博客静态站点生成器中新增"历史"页面类型，从周记文章中提取持仓图片，生成瀑布流展示页面
- 在 `base.html` 导航栏中，"归档"之后添加"历史"链接
- 新建 `history.html` 模板，继承 `base.html`，复用博客的 header、sidebar、footer 布局
- 在 `renderer.py` 中新增 `render_history()` 函数，按年月分页展示持仓快照
- 在 `generator.py` 构建流程中调用 `render_history()`
- 将 `history/generate.py` 中图片提取逻辑（关键字过滤、正则匹配持仓图片、路径转换）整合到博客生成器中

## Capabilities

### New Capabilities
- `history-page`: 博客内的历史持仓快照页面，从周记文章提取持仓图片，按年月分组展示，支持分页，样式与博客一致

### Modified Capabilities
（无现有 spec 需要修改）

## Impact

- **模板**: 新增 `blog/src/templates/history.html`；修改 `base.html` 添加导航链接
- **构建器**: 修改 `generator.py` 在构建流程中增加历史页面渲染步骤
- **渲染器**: 修改 `renderer.py` 新增 `render_history()` 函数
- **数据**: 复用 `parser.py` 已解析的文章数据，从中过滤周记并提取图片引用
- **无新依赖**: 图片提取使用已有的正则匹配逻辑，无需额外 Python 包
