## Why

当前的 `history/generate.py` 脚本直接扫描 `docs/attachments/` 目录结构来提取图片，这种方式无法利用博客文章中的上下文信息（如标题、日期、标签等）。通过改为从 `docs/blog/` 目录的 Markdown 文件中提取图片引用，可以利用文章元数据来增强图库展示，并且更符合内容管理的逻辑——图片展示应该跟随内容而非独立存在。

## What Changes

- **BREAKING**: 修改图片扫描方式，从扫描 `docs/attachments/` 目录改为遍历 `docs/blog/` 目录下的 `.md` 文件
- 添加 Markdown 文件解析功能，检测"老罗投资周记"关键字
- 从 Markdown 文件中提取图片引用，格式如 `![目前持仓](../../../attachments/2026/03/20260307/1.png)`
- 将相对路径转换为公网可访问的 URL：`https://invest.zdyi.com/attachments/2026/03/20260307/1.png`
- 保留现有的日期解析、排序和 HTML 生成功能
- 改进元数据提取，利用博客文章的日期和标题信息

## Capabilities

### New Capabilities
（无新增能力）

### Modified Capabilities
- `static-gallery-generator`: 修改图片扫描和提取的需求，从直接扫描附件目录改为从博客 Markdown 文件中提取图片引用

## Impact

- **修改代码**: `history/generate.py` 需要重写核心扫描逻辑
- **新增依赖**: 可能需要 Markdown 解析库（如 `markdown` 或直接使用正则表达式）
- **输入数据源**: 从 `docs/attachments/` 目录结构变为 `docs/blog/*.md` 文件
- **输出格式**: 保持不变，仍生成 `history/static/index.html`
- **现有内容**: 不影响现有博客内容，纯实现方式改进
