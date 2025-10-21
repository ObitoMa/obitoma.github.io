# Markdown 测试文章

这是一篇用于测试 Markdown 渲染效果的示例文章。

## 代码块测试

### JavaScript 代码
```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
    return `Welcome to our blog, ${name}!`;
}

// 调用函数
const message = greet("读者");
console.log(message);
```

### Python 代码
```python
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试函数
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### CSS 代码
```css
.markdown-content {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: #333;
}

.code-block {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    padding: 1rem;
}
```

## 文本格式测试

- **粗体文本**
- *斜体文本*
- ~~删除线文本~~
- `行内代码`
- [链接示例](https://github.com)

## 列表测试

### 无序列表
- 第一项
- 第二项
  - 子项目 2.1
  - 子项目 2.2
- 第三项

### 有序列表
1. 第一步：准备环境
2. 第二步：安装依赖
3. 第三步：运行项目

### 任务列表
- [x] 完成 Markdown 渲染
- [x] 添加代码高亮
- [ ] 优化移动端显示
- [ ] 添加更多主题

## 表格测试

| 功能 | 状态 | 优先级 |
|------|------|--------|
| 代码高亮 | ✅ 完成 | 高 |
| 表格渲染 | ✅ 完成 | 中 |
| 图片支持 | 🔄 进行中 | 中 |
| 数学公式 | ❌ 未开始 | 低 |

## 引用块测试

> 这是一个引用块示例
> 
> 可以包含多行内容，用于突出显示重要信息。
> 
> — 作者

## 分割线测试

上面的内容已经展示完毕，下面是分割线。

---

## 图片测试

![示例图片](https://via.placeholder.com/400x200?text=示例图片)

## 复杂代码示例

```javascript
// React 组件示例
import React, { useState, useEffect } from 'react';

const BlogPost = ({ title, content, author }) => {
    const [isLiked, setIsLiked] = useState(false);
    const [likeCount, setLikeCount] = useState(0);

    useEffect(() => {
        // 从 API 获取点赞数
        fetch(`/api/posts/${title}/likes`)
            .then(response => response.json())
            .then(data => setLikeCount(data.count));
    }, [title]);

    const handleLike = () => {
        setIsLiked(!isLiked);
        setLikeCount(prev => isLiked ? prev - 1 : prev + 1);
    };

    return (
        <article className="blog-post">
            <h1>{title}</h1>
            <div className="content" dangerouslySetInnerHTML={{ __html: content }} />
            <div className="meta">
                <span>作者: {author}</span>
                <button 
                    onClick={handleLike}
                    className={isLiked ? 'liked' : ''}
                >
                    ❤️ {likeCount}
                </button>
            </div>
        </article>
    );
};

export default BlogPost;
```

## 总结

这篇测试文章展示了 Markdown 的各种功能：

1. **标题层级** - 从 H1 到 H6
2. **代码高亮** - 支持多种编程语言
3. **文本格式** - 粗体、斜体、删除线等
4. **列表** - 有序、无序、任务列表
5. **表格** - 完整的数据展示
6. **引用** - 突出重要信息
7. **链接和图片** - 外部资源引用

现在代码块应该显示得非常美观了！🎉
