# 📝 将 Markdown 笔记导入 Gridea 博客

本指南将帮助您将现有的 Markdown 笔记添加到您的 Gridea 博客中。

## 🚀 快速开始

### 方法一：使用自动化脚本（推荐）

1. **准备您的 Markdown 文件**
   ```bash
   # 将您的 Markdown 文件放在一个目录中
   mkdir ~/my-notes
   # 复制您的 .md 文件到这个目录
   cp /path/to/your/notes/*.md ~/my-notes/
   ```

2. **运行批量导入脚本**
   ```bash
   cd /Users/obitoma/Documents/GitHub/obitoma.github.io
   python3 batch_import_markdown.py
   ```

3. **按提示操作**
   - 输入包含 Markdown 文件的目录路径
   - 脚本会自动处理所有 .md 文件

### 方法二：单个文件导入

1. **运行单个文件导入脚本**
   ```bash
   python3 create_article_template.py
   ```

2. **按提示输入信息**
   - Markdown 文件路径
   - 文章标题
   - 发布日期
   - 标签

## 📋 手动添加步骤

如果您想手动添加文章，请按以下步骤：

### 1. 创建文章目录
```bash
# 创建新的文章目录
mkdir -p post/your-article-name
```

### 2. 创建 index.html 文件
复制现有文章的结构，修改以下内容：
- 文章标题
- 发布日期
- 文章内容（将 Markdown 转换为 HTML）
- 标签

### 3. 更新相关页面
添加新文章后，需要更新：
- `index.html` - 首页文章列表
- `archives/index.html` - 归档页面
- `tags/index.html` - 标签页面
- `atom.xml` - RSS 订阅

## 🏷️ Markdown 文件格式建议

为了获得最佳效果，建议您的 Markdown 文件包含：

```markdown
# 文章标题

tags: 标签1, 标签2, 标签3

## 文章内容

这里是您的文章内容...

### 子标题

更多内容...
```

## 🔧 高级配置

### 配置文件格式
创建 `config.json` 文件来自定义导入行为：

```json
{
  "default_tags": ["笔记", "学习"],
  "date_format": "%Y-%m-%d",
  "output_directory": "post",
  "template_file": "article_template.html"
}
```

### 自定义模板
您可以修改 `create_article_template.py` 中的 `generate_article_html` 函数来自定义文章模板。

## 📁 文件结构

导入后的文件结构：
```
post/
├── your-article-1/
│   └── index.html
├── your-article-2/
│   └── index.html
└── ...
```

## 🚨 注意事项

1. **路径问题**：确保所有相对路径正确
2. **图片处理**：如果 Markdown 中有图片，需要手动复制到 `post-images/` 目录
3. **样式一致性**：确保生成的 HTML 与现有样式兼容
4. **SEO 优化**：添加适当的 meta 标签

## 🛠️ 故障排除

### 常见问题

1. **脚本无法运行**
   ```bash
   # 确保 Python 3 已安装
   python3 --version
   ```

2. **路径错误**
   - 检查 Markdown 文件路径是否正确
   - 确保在项目根目录运行脚本

3. **编码问题**
   - 确保 Markdown 文件使用 UTF-8 编码

### 获取帮助

如果遇到问题，请检查：
1. 文件路径是否正确
2. 文件编码是否为 UTF-8
3. 是否有足够的文件权限

## 📚 下一步

导入完成后，您需要：

1. **测试网站**：在本地测试所有页面
2. **更新导航**：确保所有链接正常工作
3. **优化 SEO**：添加适当的 meta 标签
4. **部署**：推送到 GitHub Pages

## 🎉 完成！

现在您的 Markdown 笔记已经成功导入到 Gridea 博客中了！

记住定期备份您的内容，并考虑使用版本控制来管理您的博客。
