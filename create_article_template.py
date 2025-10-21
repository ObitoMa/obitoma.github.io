#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gridea 文章创建工具
用于将 Markdown 笔记转换为 Gridea 博客文章
"""

import os
import re
import datetime
from pathlib import Path

def create_article_from_markdown(markdown_file, title, date=None, tags=None, description=None):
    """
    从 Markdown 文件创建 Gridea 文章
    
    Args:
        markdown_file: Markdown 文件路径
        title: 文章标题
        date: 发布日期 (格式: YYYY-MM-DD)
        tags: 标签列表
        description: 文章描述
    """
    
    if not os.path.exists(markdown_file):
        print(f"错误：Markdown 文件 {markdown_file} 不存在")
        return False
    
    # 读取 Markdown 内容
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 设置默认值
    if date is None:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    if tags is None:
        tags = []
    if description is None:
        # 从 Markdown 内容中提取前100个字符作为描述
        description = markdown_content[:100].replace('\n', ' ').strip()
    
    # 创建文章目录名（基于标题）
    article_slug = re.sub(r'[^\w\s-]', '', title.lower())
    article_slug = re.sub(r'[-\s]+', '-', article_slug)
    article_dir = f"post/{article_slug}"
    
    # 创建目录
    os.makedirs(article_dir, exist_ok=True)
    
    # 生成文章 HTML
    html_content = generate_article_html(title, date, markdown_content, tags, description, article_slug)
    
    # 写入 HTML 文件
    html_file = os.path.join(article_dir, 'index.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 文章创建成功：{html_file}")
    return True

def generate_article_html(title, date, content, tags, description, article_slug):
    """生成文章 HTML 内容"""
    
    # 将 Markdown 转换为 HTML（简单转换）
    html_content = markdown_to_html(content)
    
    # 生成标签 HTML
    tags_html = ""
    if tags:
        tags_html = f"""
              <div class="tag-container">
                {''.join([f'<a href="../../tag/{tag}/" class="tag">{tag}</a>' for tag in tags])}
              </div>"""
    
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" >

<title>{title} | Gridea</title>

<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
<link rel="shortcut icon" href="../../favicon.ico?v=1659011765580">
<link rel="stylesheet" href="../../styles/main.css">



<link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>



    <meta name="description" content="{description}" />
    <meta name="keywords" content="{', '.join(tags)}" />
  </head>
  <body>
    <div id="app" class="main">

      <div class="sidebar" :class="{{ 'full-height': menuVisible }}">
  <div class="top-container" data-aos="fade-right">
    <div class="top-header-container">
      <a class="site-title-container" href="/">
        <img src="../../images/avatar.png?v=1659011765580" class="site-logo">
        <h1 class="site-title">Gridea</h1>
      </a>
      <div class="menu-btn" @click="menuVisible = !menuVisible">
        <div class="line"></div>
      </div>
    </div>
    <div>
      
        
          <a href="/" class="site-nav">
            首页
          </a>
        
      
        
          <a href="/archives" class="site-nav">
            归档
          </a>
        
      
        
          <a href="/tags" class="site-nav">
            标签
          </a>
        
      
        
          <a href="/post/about" class="site-nav">
            关于
          </a>
        
      
    </div>
  </div>
  <div class="bottom-container" data-aos="flip-up" data-aos-offset="0">
    <div class="social-container">
      
        
      
        
      
        
      
        
      
        
      
    </div>
    <div class="site-description">
      温故而知新
    </div>
    <div class="site-footer">
      Powered by <a href="https://github.com/getgridea/gridea" target="_blank">Gridea</a> | <a class="rss" href="../../atom.xml" target="_blank">RSS</a>
    </div>
  </div>
</div>


      <div class="main-container">
        <div class="content-container" data-aos="fade-up">
          <div class="post-detail">
            <h2 class="post-title">{title}</h2>
            <div class="post-date">{date}</div>
            
            <div class="post-content" v-pre>
              {html_content}
            </div>
            
            {tags_html}
            

            

          </div>

        </div>
      </div>
    </div>

    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
<script type="application/javascript">

AOS.init();

var app = new Vue({{
  el: '#app',
  data: {{
    menuVisible: false,
  }},
}})

</script>




  </body>
</html>"""

def markdown_to_html(markdown_content):
    """简单的 Markdown 到 HTML 转换"""
    # 这里可以集成更强大的 Markdown 解析器，如 markdown 库
    # 现在使用简单的正则表达式转换
    
    # 转换标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown_content, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 转换粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 转换链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 转换代码块
    html = re.sub(r'```([^`]+)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 转换段落
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            p = f'<p>{p}</p>'
        html_paragraphs.append(p)
    
    return '\n\n'.join(html_paragraphs)

def main():
    """主函数 - 示例用法"""
    print("📝 Gridea 文章创建工具")
    print("=" * 50)
    
    # 示例：创建一篇文章
    markdown_file = input("请输入 Markdown 文件路径: ").strip()
    title = input("请输入文章标题: ").strip()
    date = input("请输入发布日期 (YYYY-MM-DD，留空使用今天): ").strip() or None
    tags_input = input("请输入标签 (用逗号分隔): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    if create_article_from_markdown(markdown_file, title, date, tags):
        print(f"\n🎉 文章 '{title}' 创建成功！")
        print("现在您需要：")
        print("1. 更新首页 (index.html) 添加新文章链接")
        print("2. 更新归档页面 (archives/index.html)")
        print("3. 更新标签页面 (tags/index.html)")
        print("4. 更新 atom.xml RSS 文件")
    else:
        print("❌ 文章创建失败")

if __name__ == "__main__":
    main()
