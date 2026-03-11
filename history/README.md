# 交易历史图片展示页面生成器

这是一个 Python 工具，用于从 `docs/blog/` 目录的 Markdown 文件中提取交易截图引用，并生成瀑布流布局的静态 HTML 页面。

## 功能特性

- ✅ 自动扫描 `docs/blog/` 目录下的所有 Markdown 文件
- ✅ **智能过滤：仅处理包含"老罗投资周记"或"老罗实盘周记"关键字的文件**
- ✅ **仅显示周六的交易记录**
- ✅ 从 Markdown 文件中提取图片引用和元数据（标题、日期）
- ✅ 生成公网可访问的完整 URL（`https://invest.zdyi.com/attachments/YYYY/MM/YYYYMMDD/1.png`）
- ✅ 支持多种日期格式解析（YYYYMMDD、YYYY-MM-DD、YYYY/MM/DD 等）
- ✅ 按时间倒序展示交易记录
- ✅ **单列布局**（一行显示一个图片，所有设备统一体验）
- ✅ 图片懒加载，提升页面性能
- ✅ 点击图片可放大查看
- ✅ 纯静态 HTML，无需后端服务
- ✅ **零新增依赖**：使用正则表达式解析 Markdown，无需额外的 Markdown 解析库

## 目录结构

```
history/
├── generate.py          # 主生成脚本
├── generate.py.backup   # 旧版本备份（扫描附件目录的方式）
├── template.html        # HTML 模板文件
├── requirements.txt     # Python 依赖
├── README.md           # 说明文档（本文件）
└── static/
    └── index.html      # 生成的静态页面（git 可选）
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r history/requirements.txt
```

### 2. 准备博客文件

确保你的博客文章（位于 `docs/blog/` 目录）：

1. 包含"老罗投资周记"或"老罗实盘周记"关键字
2. 包含图片引用，格式如下：
   ```markdown
   ![目前持仓](../../../attachments/2026/03/20260307/1.png)
   ```
3. 可选：包含 frontmatter 元数据（标题、日期等）

**示例博客文件格式**：

```markdown
---
title: 老罗投资周记-20260307
date: 2026-03-07
tags:
    - 投资周记
---

老罗投资周记，每周六更新。

## 2. 目前持仓

![目前持仓](../../../attachments/2026/03/20260307/1.png)
```

### 3. 运行生成器

```bash
# 使用默认配置（扫描 docs/blog/ 目录）
python history/generate.py

# 自定义博客目录
python history/generate.py --blog-dir /path/to/blog

# 自定义输出路径
python history/generate.py --output /path/to/output.html

# 自定义模板文件
python history/generate.py --template /path/to/template.html
```

### 4. 查看结果

在浏览器中打开生成的 `history/static/index.html` 文件。

## 图片引用格式说明

生成器使用正则表达式匹配以下格式的图片引用：

```markdown
![目前持仓](../../../attachments/YYYY/MM/YYYYMMDD/1.png)
```

**要求**：
- alt 文本必须是"目前持仓"
- 路径必须是相对路径（以 `../` 或 `./` 开头）
- 路径必须指向 `attachments/` 目录下的图片文件
- 文件名通常是 `1.png`，但也可以是其他文件名

**支持的路径格式**：

```
../../../attachments/2026/03/20260307/1.png
../../attachments/2026/03/20260307/1.png
./attachments/2026/03/20260307/1.png
attachments/2026/03/20260307/1.png
```

所有这些路径都会被转换为：
```
https://invest.zdyi.com/attachments/2026/03/20260307/1.png
```

## 元数据提取

生成器会从 Markdown 文件中提取以下元数据：

### 标题提取（按优先级）

1. **Frontmatter 中的 `title` 字段**：
   ```yaml
   ---
   title: 老罗投资周记-20260307
   ---
   ```
2. **第一个一级标题（`# 标题`）**
3. **文件名**（如果以上都不存在）

### 日期提取（按优先级）

1. **Frontmatter 中的 `date` 字段**：
   ```yaml
   ---
   date: 2026-03-07
   ---
   ```
2. **从文件路径解析**（如 `docs/blog/2026/03/20260307.md` → `20260307`）

## 支持的日期格式

- `YYYYMMDD` - 紧凑格式（如 20260307）
- `YYYY-MM-DD` - ISO 8601 格式
- `YYYY/MM/DD` - 斜杠分隔
- `YYYY.MM.DD` - 点号分隔

## 错误处理

生成器具有强大的容错能力：

- ✅ **文件读取错误**：跳过无法读取的文件，记录警告
- ✅ **图片引用缺失**：跳过没有图片引用的文件，记录警告
- ✅ **日期解析失败**：使用文件名作为标签，继续处理
- ✅ **编码问题**：自动跳过编码错误的文件

**统计信息输出**：

```
扫描统计:
  总文件数: 250
  包含关键字: 70
  包含图片引用: 70
  成功处理: 68
  跳过: 182
  错误: 0
```

## 定制化

### 修改样式

编辑 `history/template.html` 文件中的 CSS 部分，可以自定义：

- 颜色主题
- 布局列数
- 图片间距
- 字体样式

### 修改模板

`template.html` 使用 Jinja2 模板语法，可用变量：

- `items` - 图片列表，每个元素包含：
  - `date` - 日期标签（YYYYMMDD 格式）
  - `image_url` - 图片 URL
  - `full_image_url` - 大图 URL（与 image_url 相同）
  - `blog_url` - 对应的博客文章 URL
  - `year` - 年份
  - `title` - 文章标题（从 Markdown frontmatter 或标题中提取）

## 集成到 CI/CD

在部署脚本中添加生成器调用：

```bash
#!/bin/bash
# 生成历史页面
python history/generate.py

# 继续部署...
```

## 技术栈

- **Python 3.8+** - 核心逻辑
- **Jinja2** - HTML 模板引擎
- **正则表达式** - Markdown 解析（零额外依赖）
- **纯 CSS** - 瀑布流布局（无 JavaScript 依赖）

## 工作原理

1. **扫描博客目录**：递归扫描 `docs/blog/` 目录，查找所有 `.md` 文件
2. **关键字过滤**：检查文件内容是否包含"老罗投资周记"或"老罗实盘周记"
3. **提取图片引用**：使用正则表达式匹配 `![目前持仓](...)` 格式
4. **路径转换**：将相对路径转换为公网可访问的 URL
5. **元数据提取**：从 frontmatter 或文件路径中提取标题和日期
6. **日期过滤**：仅保留周六的记录
7. **排序和生成**：按日期倒序排列，使用 Jinja2 模板生成 HTML

## 故障排查

### 没有找到任何图片

- 确保 `docs/blog/` 目录存在
- 确保博客文章包含"老罗投资周记"或"老罗实盘周记"关键字
- 检查图片引用格式是否正确：`![目前持仓](../../../attachments/...)`
- 查看统计信息，了解有多少文件被跳过

### 图片无法显示

- 检查生成的 HTML 中的图片 URL 是否正确
- 确保图片文件存在于 `docs/attachments/` 目录下
- 验证公网 URL 是否可访问

### 某些文件被跳过

- 检查文件是否包含"老罗投资周记"或"老罗实盘周记"关键字
- 检查图片引用格式是否正确
- 查看日志输出，了解跳过原因

## 版本历史

### v2.0.0（当前版本）

- **BREAKING**: 从扫描附件目录改为解析博客 Markdown 文件
- 添加 Markdown 文件解析功能（使用正则表达式）
- 添加元数据提取（标题、日期）
- 添加关键字过滤（"老罗投资周记"或"老罗实盘周记"）
- 改进错误处理和统计信息输出
- 添加 `--blog-dir` 命令行参数

### v1.0.0

- 初始版本，直接扫描 `docs/attachments/` 目录
- 备份文件：`generate.py.backup`

## License

MIT
