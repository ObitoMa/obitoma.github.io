#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客更新脚本
自动扫描新文章并更新首页、归档、标签、RSS等页面
"""

import os
import re
import json
import datetime
from pathlib import Path
from collections import defaultdict

def scan_articles():
    """扫描所有文章"""
    articles = []
    post_dir = Path("post")
    
    if not post_dir.exists():
        print("❌ post 目录不存在")
        return articles
    
    for article_dir in post_dir.iterdir():
        if article_dir.is_dir():
            index_file = article_dir / "index.html"
            if index_file.exists():
                article_info = extract_article_info(index_file, article_dir.name)
                if article_info:
                    articles.append(article_info)
    
    # 按日期排序（最新的在前）
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def extract_article_info(html_file, article_slug):
    """从HTML文件中提取文章信息"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'<h2 class="post-title">(.+?)</h2>', content)
        title = title_match.group(1) if title_match else article_slug
        
        # 提取日期
        date_match = re.search(r'<div class="post-date">(.+?)</div>', content)
        date = date_match.group(1) if date_match else datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 提取摘要
        abstract_match = re.search(r'<div class="post-abstract">.*?<p>(.+?)</p>', content, re.DOTALL)
        abstract = abstract_match.group(1).strip() if abstract_match else "暂无摘要"
        
        # 提取标签
        tags = []
        tag_matches = re.findall(r'<span class="tag">(.+?)</span>', content)
        tags = [tag.strip() for tag in tag_matches]
        
        return {
            'slug': article_slug,
            'title': title,
            'date': date,
            'abstract': abstract,
            'tags': tags,
            'path': f"./post/{article_slug}/"
        }
    except Exception as e:
        print(f"❌ 解析文章 {article_slug} 失败: {e}")
        return None

def update_homepage(articles):
    """更新首页"""
    print("📝 更新首页...")
    
    # 生成文章列表HTML
    articles_html = ""
    for article in articles[:5]:  # 只显示最新5篇
        articles_html += f"""
            <article class="post-item">
              <div class="left">
                <a href="{article['path']}">
                  <h2 class="post-title">{article['title']}</h2>
                </a>
                <div class="post-date">
                  {article['date']}
                </div>
                <div class="post-abstract">
                  <p>{article['abstract']}</p>
                </div>
              </div>
            </article>
        """
    
    # 读取并更新首页
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换文章列表部分
    pattern = r'<div class="content-container" data-aos="fade-up">(.*?)<div class="pagination-container">'
    replacement = f'<div class="content-container" data-aos="fade-up">{articles_html}<div class="pagination-container">'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 首页更新完成")

def update_archives(articles):
    """更新归档页面"""
    print("📚 更新归档页面...")
    
    # 按年份分组
    articles_by_year = defaultdict(list)
    for article in articles:
        year = article['date'][:4]
        articles_by_year[year].append(article)
    
    # 生成归档HTML
    archives_html = ""
    for year in sorted(articles_by_year.keys(), reverse=True):
        archives_html += f'<h2 class="year" data-aos="fade-in" data-aos-delay="500">{year}</h2>\n'
        for article in articles_by_year[year]:
            archives_html += f"""
                <article class="post">
                  <a href="../{article['path']}">
                    <h2 class="post-title">{article['title']}</h2>
                  </a>
                </article>
            """
    
    # 读取并更新归档页面
    with open('archives/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换归档内容
    pattern = r'<div class="archives-container">(.*?)</div>'
    replacement = f'<div class="archives-container">{archives_html}</div>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('archives/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 归档页面更新完成")

def update_tags(articles):
    """更新标签页面"""
    print("🏷️ 更新标签页面...")
    
    # 收集所有标签
    all_tags = set()
    for article in articles:
        all_tags.update(article['tags'])
    
    # 生成标签列表HTML
    tags_html = ""
    for tag in sorted(all_tags):
        tag_slug = re.sub(r'[^\w\s-]', '', tag).replace(' ', '-')
        tags_html += f'<a class="tag" href="../tag/{tag_slug}/">{tag}</a>\n'
    
    # 更新标签列表页面
    with open('tags/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<div class="tags-container">(.*?)</div>'
    replacement = f'<div class="tags-container">{tags_html}</div>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('tags/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 为每个标签创建详情页面
    for tag in all_tags:
        create_tag_page(tag, articles)
    
    print("✅ 标签页面更新完成")

def create_tag_page(tag, articles):
    """创建标签详情页面"""
    tag_slug = re.sub(r'[^\w\s-]', '', tag).replace(' ', '-')
    tag_dir = Path(f"tag/{tag_slug}")
    tag_dir.mkdir(parents=True, exist_ok=True)
    
    # 找到该标签下的文章
    tag_articles = [a for a in articles if tag in a['tags']]
    
    # 生成标签页面HTML
    articles_html = ""
    for article in tag_articles:
        articles_html += f"""
            <article class="post-item">
              <div class="left">
                <a href="../../{article['path']}">
                  <h2 class="post-title">{article['title']}</h2>
                </a>
                <div class="post-date">
                  {article['date']}
                </div>
                <div class="post-abstract">
                  <p>{article['abstract']}</p>
                </div>
              </div>
            </article>
        """
    
    tag_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{tag} | Gridea</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <link rel="stylesheet" href="../../styles/main.css">
  </head>
  <body>
    <div class="main">
      <div class="sidebar">
        <div class="top-container">
          <div class="top-header-container">
            <a class="site-title-container" href="/">
              <img src="../../images/avatar.png?v=1659011765580" class="site-logo">
              <h1 class="site-title">Gridea</h1>
            </a>
          </div>
          <div>
            <a href="/" class="site-nav">首页</a>
            <a href="/archives" class="site-nav">归档</a>
            <a href="/tags" class="site-nav">标签</a>
            <a href="/post/about" class="site-nav">关于</a>
          </div>
        </div>
      </div>
      
      <div class="main-container">
        <div class="content-container">
          <h2 class="current-tag">标签: {tag}</h2>
          {articles_html}
        </div>
      </div>
    </div>
  </body>
</html>"""
    
    with open(tag_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(tag_html)

def update_rss(articles):
    """更新RSS文件"""
    print("📡 更新RSS文件...")
    
    # 生成RSS条目
    entries = ""
    for article in articles[:10]:  # 只包含最新10篇
        entries += f"""
    <entry>
        <title type="html"><![CDATA[{article['title']}]]></title>
        <id>./{article['path']}</id>
        <link href="./{article['path']}">
        </link>
        <updated>{article['date']}T12:00:00.000Z</updated>
        <summary type="html"><![CDATA[<p>{article['abstract']}</p>]]></summary>
    </entry>"""
    
    # 生成完整RSS内容
    rss_content = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>.</id>
    <title>Gridea</title>
    <updated>{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')}</updated>
    <generator>https://github.com/jpmonette/feed</generator>
    <link rel="alternate" href="."/>
    <link rel="self" href="./atom.xml"/>
    <subtitle>温故而知新</subtitle>
    <logo>./images/avatar.png</logo>
    <icon>./favicon.ico</icon>
    <rights>All rights reserved {datetime.datetime.now().year}, Gridea</rights>{entries}
</feed>"""
    
    with open('atom.xml', 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print("✅ RSS文件更新完成")

def main():
    """主函数"""
    print("🚀 开始更新博客...")
    print("=" * 50)
    
    # 扫描文章
    articles = scan_articles()
    if not articles:
        print("❌ 没有找到任何文章")
        return
    
    print(f"📖 找到 {len(articles)} 篇文章")
    
    # 更新各个页面
    update_homepage(articles)
    update_archives(articles)
    update_tags(articles)
    update_rss(articles)
    
    print("=" * 50)
    print("🎉 博客更新完成！")
    print("\n📋 更新内容：")
    print("- ✅ 首页文章列表")
    print("- ✅ 归档页面")
    print("- ✅ 标签页面")
    print("- ✅ RSS订阅源")
    print("\n💡 使用提示：")
    print("1. 添加新文章后运行此脚本")
    print("2. 脚本会自动更新所有相关页面")
    print("3. 提交更改并推送到GitHub即可")

if __name__ == "__main__":
    main()
