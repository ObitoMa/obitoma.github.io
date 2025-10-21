# 📝 博客自动更新指南

## 🤔 为什么需要手动更新？

您的博客是**静态博客**，不像动态博客那样可以自动更新。每次添加新文章后，需要手动更新以下页面：

- 📄 **首页** - 显示文章列表
- 📚 **归档页面** - 按时间排序
- 🏷️ **标签页面** - 按标签分类
- 📡 **RSS订阅** - 订阅源更新

## 🚀 自动化解决方案

我为您创建了 `update_blog.py` 脚本，可以自动完成所有更新工作！

### 📋 使用方法

#### 方法一：添加新文章后运行脚本

1. **添加新文章**：
   ```bash
   # 将新文章的文件夹放到 post/ 目录下
   cp -r /path/to/new-article post/
   ```

2. **运行更新脚本**：
   ```bash
   cd /Users/obitoma/Documents/GitHub/obitoma.github.io
   python3 update_blog.py
   ```

3. **提交更改**：
   ```bash
   git add .
   git commit -m "添加新文章：文章标题"
   git push origin main
   ```

#### 方法二：使用Markdown工具创建文章

1. **使用Markdown展示器**：
   - 访问 `https://obitoma.github.io/markdown-display.html`
   - 拖拽Markdown文件
   - 点击"创建博客文章"
   - 下载压缩包并解压到 `post/` 目录

2. **运行更新脚本**：
   ```bash
   python3 update_blog.py
   ```

### 🔧 脚本功能

`update_blog.py` 脚本会自动：

1. **扫描文章**：自动发现 `post/` 目录下的所有文章
2. **提取信息**：从HTML文件中提取标题、日期、摘要、标签
3. **更新首页**：按时间顺序显示最新文章
4. **更新归档**：按年份分组显示所有文章
5. **更新标签**：自动创建标签页面和标签详情页
6. **更新RSS**：生成完整的RSS订阅源

### 📁 脚本工作原理

```
post/
├── 文章1/
│   └── index.html
├── 文章2/
│   └── index.html
└── ...

↓ 扫描文章

↓ 提取信息
- 标题、日期、摘要、标签

↓ 更新页面
- index.html (首页)
- archives/index.html (归档)
- tags/index.html (标签列表)
- tag/标签名/index.html (标签详情)
- atom.xml (RSS)
```

### 🎯 推荐工作流程

#### 日常写作流程

1. **写文章**：
   - 使用您喜欢的Markdown编辑器
   - 或使用在线Markdown工具

2. **创建博客文章**：
   - 使用 `markdown-display.html` 工具
   - 下载压缩包并解压到 `post/` 目录

3. **更新博客**：
   ```bash
   python3 update_blog.py
   ```

4. **部署**：
   ```bash
   git add .
   git commit -m "添加新文章：文章标题"
   git push origin main
   ```

### 🛠️ 高级用法

#### 批量添加文章

```bash
# 1. 将多个文章文件夹复制到 post/ 目录
cp -r /path/to/articles/* post/

# 2. 运行更新脚本
python3 update_blog.py

# 3. 提交所有更改
git add .
git commit -m "批量添加文章"
git push origin main
```

#### 自定义脚本

您可以修改 `update_blog.py` 脚本来自定义：
- 首页显示的文章数量
- 文章排序方式
- RSS条目数量
- 标签处理方式

### 📝 注意事项

1. **文章结构**：确保每篇文章都在 `post/文章名/index.html` 格式
2. **HTML格式**：文章HTML需要包含正确的class名称
3. **标签格式**：标签需要在HTML中以 `<span class="tag">标签名</span>` 格式存在
4. **备份**：运行脚本前建议备份重要文件

### 🚨 故障排除

#### 常见问题

1. **脚本无法运行**：
   ```bash
   # 确保Python 3已安装
   python3 --version
   ```

2. **文章没有被识别**：
   - 检查文章HTML格式是否正确
   - 确保包含必要的class名称

3. **标签页面没有创建**：
   - 检查文章中的标签格式
   - 确保标签以正确的HTML格式存在

### 🎉 总结

使用 `update_blog.py` 脚本，您可以：

- ✅ **一键更新**：运行一个命令更新所有页面
- ✅ **自动发现**：自动扫描新文章
- ✅ **智能处理**：自动提取文章信息
- ✅ **完整更新**：更新首页、归档、标签、RSS

现在您只需要：
1. 添加新文章到 `post/` 目录
2. 运行 `python3 update_blog.py`
3. 提交并推送更改

就这么简单！🎉
