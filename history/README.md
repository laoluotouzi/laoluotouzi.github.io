# 交易历史图片展示页面生成器

这是一个 Python 工具，用于从 `docs/attachments/` 目录扫描交易截图，并生成瀑布流布局的静态 HTML 页面。

## 功能特性

- ✅ 自动扫描 `docs/attachments/` 目录下的所有图片
- ✅ **智能过滤：仅显示周六的交易记录**
- ✅ 生成公网可访问的完整 URL（`https://invest.zdyi.com/attachments/YYYY/MM/YYYYMMDD/1.png`）
- ✅ 支持多种日期格式解析（YYYYMMDD、YYYY-MM-DD、YYYY/MM/DD 等）
- ✅ 按时间倒序展示交易记录
- ✅ **单列布局**（一行显示一个图片，所有设备统一体验）
- ✅ 图片懒加载，提升页面性能
- ✅ 点击图片可放大查看
- ✅ 纯静态 HTML，无需后端服务

## 目录结构

```
history/
├── generate.py          # 主生成脚本
├── template.html        # HTML 模板文件
├── requirements.txt     # Python 依赖
├── README.md           # 说明文档
└── static/
    └── index.html      # 生成的静态页面（git 可选）
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r history/requirements.txt
```

### 2. 运行生成器

```bash
# 使用默认配置
python history/generate.py

# 自定义输入/输出路径
python history/generate.py --input /path/to/attachments --output /path/to/output.html
```

### 3. 查看结果

在浏览器中打开生成的 `history/static/index.html` 文件。

## 支持的目录结构

生成器支持以下两种目录结构：

```
# 格式 1：年/月/日期/文件
docs/attachments/2022/11/20221127/1.png

# 格式 2：年/日期/文件
docs/attachments/2022/2022-11-27/1.png
```

## 支持的日期格式

- `YYYYMMDD` - 紧凑格式（如 20221127）
- `YYYY-MM-DD` - ISO 8601 格式
- `YYYY/MM/DD` - 斜杠分隔
- `YYYY.MM.DD` - 点号分隔

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
  - `date` - 日期标签
  - `image_url` - 图片 URL
  - `full_image_url` - 大图 URL

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
- **纯 CSS** - 瀑布流布局（无 JavaScript 依赖）

## 故障排查

### 找不到图片

- 确保 `docs/attachments/` 目录存在
- 确保每个日期目录下有 `1.png` 文件
- 检查目录名是否匹配支持的日期格式

### 图片无法显示

- 检查生成的 HTML 中的图片路径是否正确
- 确保图片文件存在于 `docs/attachments/` 目录下
- 验证相对路径在部署环境中有效

## License

MIT
