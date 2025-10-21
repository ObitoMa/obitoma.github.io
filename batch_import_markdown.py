#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入 Markdown 笔记到 Gridea 博客
"""

import os
import re
import json
import datetime
from pathlib import Path

def batch_import_markdown(notes_directory, config_file=None):
    """
    批量导入 Markdown 笔记
    
    Args:
        notes_directory: 包含 Markdown 文件的目录
        config_file: 配置文件路径（可选）
    """
    
    if not os.path.exists(notes_directory):
        print(f"错误：目录 {notes_directory} 不存在")
        return False
    
    # 加载配置
    config = load_config(config_file) if config_file else {}
    
    # 查找所有 Markdown 文件
    markdown_files = []
    for root, dirs, files in os.walk(notes_directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                markdown_files.append(os.path.join(root, file))
    
    print(f"找到 {len(markdown_files)} 个 Markdown 文件")
    
    # 处理每个文件
    success_count = 0
    for md_file in markdown_files:
        try:
            # 从文件名或内容中提取信息
            title = extract_title_from_file(md_file)
            date = extract_date_from_file(md_file)
            tags = extract_tags_from_file(md_file)
            
            # 创建文章
            if create_article_from_markdown(md_file, title, date, tags):
                success_count += 1
                print(f"✅ 成功处理: {title}")
            else:
                print(f"❌ 处理失败: {md_file}")
                
        except Exception as e:
            print(f"❌ 处理 {md_file} 时出错: {e}")
    
    print(f"\n🎉 批量导入完成！成功处理 {success_count}/{len(markdown_files)} 个文件")
    return success_count > 0

def load_config(config_file):
    """加载配置文件"""
    if not os.path.exists(config_file):
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_title_from_file(file_path):
    """从文件路径或内容中提取标题"""
    # 从文件名提取
    filename = os.path.basename(file_path)
    title = os.path.splitext(filename)[0]
    
    # 尝试从文件内容中提取标题
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找第一个 # 标题
            match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except:
        pass
    
    return title

def extract_date_from_file(file_path):
    """从文件内容中提取日期"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找日期格式 YYYY-MM-DD
            match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
            if match:
                return match.group(1)
    except:
        pass
    
    # 使用文件修改时间
    mtime = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def extract_tags_from_file(file_path):
    """从文件内容中提取标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找标签行
            match = re.search(r'^tags?:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
            if match:
                return [tag.strip() for tag in match.group(1).split(',')]
    except:
        pass
    
    return []

def create_article_from_markdown(markdown_file, title, date, tags):
    """创建文章（简化版）"""
    try:
        # 读取 Markdown 内容
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 创建文章目录
        article_slug = re.sub(r'[^\w\s-]', '', title.lower())
        article_slug = re.sub(r'[-\s]+', '-', article_slug)
        article_dir = f"post/{article_slug}"
        os.makedirs(article_dir, exist_ok=True)
        
        # 生成 HTML 内容（简化版）
        html_content = generate_simple_html(title, date, markdown_content, tags)
        
        # 写入文件
        html_file = os.path.join(article_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    except Exception as e:
        print(f"创建文章时出错: {e}")
        return False

def generate_simple_html(title, date, content, tags):
    """生成简化的 HTML"""
    # 简单的 Markdown 转换
    html_content = content.replace('\n', '<br>\n')
    
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{title} | Gridea</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <link rel="stylesheet" href="../../styles/main.css">
  </head>
  <body>
    <div class="main">
      <div class="sidebar">
        <div class="top-container">
          <div class="top-header-container">
            <a class="site-title-container" href="/">
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
          <div class="post-detail">
            <h2 class="post-title">{title}</h2>
            <div class="post-date">{date}</div>
            <div class="post-content">
              {html_content}
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>"""

def main():
    """主函数"""
    print("📝 批量导入 Markdown 笔记到 Gridea 博客")
    print("=" * 50)
    
    notes_dir = input("请输入包含 Markdown 文件的目录路径: ").strip()
    
    if batch_import_markdown(notes_dir):
        print("\n🎉 批量导入完成！")
        print("\n接下来您需要：")
        print("1. 检查生成的文章是否正确")
        print("2. 更新首页、归档页面、标签页面")
        print("3. 更新 RSS 文件")
    else:
        print("❌ 批量导入失败")

if __name__ == "__main__":
    main()
