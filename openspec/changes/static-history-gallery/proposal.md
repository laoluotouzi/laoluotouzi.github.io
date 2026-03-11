## Why

当前 `docs/attachments` 目录下存储了按日期组织的交易截图（各日期目录下的 1.png），但缺少一个可视化的历史回顾页面来展示这些图片。需要一个自动化工具来生成静态的图片展示页面，以便在网站上以瀑布流形式展示交易历史记录。

## What Changes

- 新建 `history/` 目录用于存放图片展示页面生成程序
- 开发 Python 程序，功能包括：
  - 扫描 `docs/attachments/` 下所有日期目录
  - 提取每个目录中的 `1.png` 图片文件
  - 从目录名称解析日期信息
  - 按时间倒序排列图片
  - 生成瀑布流布局的静态 HTML 页面
  - 将生成的页面输出到指定位置（如 `history/static/index.html`）

## Capabilities

### New Capabilities
- `static-gallery-generator`: 基于 Python 的静态图片展示页面生成器，能够从目录结构中提取图片并生成瀑布流布局的 HTML 页面

### Modified Capabilities
- 无

## Impact

- **新增代码**: `history/` 目录及 Python 生成程序
- **新增依赖**: 可能需要 Python 模板引擎（如 Jinja2）用于 HTML 生成
- **构建流程**: 需要将生成程序集成到网站的构建或部署流程中
- **现有内容**: 不影响现有网站内容，纯增量添加
