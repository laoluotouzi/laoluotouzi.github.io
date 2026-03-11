## 1. 项目初始化

- [x] 1.1 创建 `history/` 目录结构
- [x] 1.2 创建 `history/requirements.txt`，添加 Jinja2 依赖
- [x] 1.3 创建 `history/generate.py` 主脚本文件（包含基本的 CLI 参数解析）
- [x] 1.4 创建 `history/template.html` Jinja2 模板文件框架

## 2. 核心功能实现

- [x] 2.1 实现目录扫描功能：递归扫描 `docs/attachments/` 目录
- [x] 2.2 实现图片提取功能：从每个目录中提取 `1.png` 文件
- [x] 2.3 实现日期解析功能：支持多种日期格式（ISO 8601、YYYY/MM/DD、YYYY.MM.DD）
- [x] 2.4 实现日期排序功能：按时间倒序排列图片
- [x] 2.5 实现错误处理：处理缺失目录和无效日期格式
- [x] 2.6 添加日志输出：显示处理进度和警告信息

## 3. HTML 模板和生成

- [x] 3.1 设计并实现瀑布流布局的 CSS（使用 CSS Multi-column）
- [x] 3.2 实现响应式设计：移动端 1 列、平板 2-3 列、桌面 3-4 列
- [x] 3.3 在模板中添加图片懒加载（`loading="lazy"` 属性）
- [x] 3.4 实现图片点击放大功能（使用简单的 lightbox 或 target="_blank"）
- [x] 3.5 在模板中嵌入所有必要的 CSS
- [x] 3.6 实现相对路径生成：`../docs/attachments/<year>/<date>/1.png`
- [x] 3.7 添加页面标题和元数据

## 4. 集成和测试

- [x] 4.1 本地测试：运行 `python history/generate.py` 生成页面
- [ ] 4.2 在浏览器中打开 `history/static/index.html` 验证显示效果
- [ ] 4.3 验证所有图片链接正确且可访问
- [ ] 4.4 测试日期解析：确认不同格式的目录名都能正确解析
- [ ] 4.5 测试时间排序：确认图片按时间倒序显示
- [ ] 4.6 测试响应式布局：在不同屏幕尺寸下验证布局

## 5. 文档和部署

- [x] 5.1 在 `history/` 目录下创建 `README.md`，说明使用方法
- [x] 5.2 将 `history/` 目录添加到 git 版本控制
