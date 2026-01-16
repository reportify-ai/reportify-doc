#!/usr/bin/env python3
import os
import re

def add_mode_to_openapi_file(file_path):
    """如果文件有 openapi 字段但没有 mode 字段，则添加 mode: 'show'"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有 openapi 字段
    if not re.search(r'^openapi:\s*[\'"]?(GET|POST|PUT|DELETE|PATCH)', content, re.MULTILINE):
        return False
    
    # 检查是否已经有 mode 字段
    if re.search(r'^mode:\s*', content, re.MULTILINE):
        print(f"  跳过 {file_path} (已有 mode)")
        return False
    
    # 匹配 frontmatter 并添加 mode
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        print(f"⚠️  无法找到 frontmatter: {file_path}")
        return False
    
    frontmatter = match.group(1)
    
    # 在 frontmatter 最后添加 mode: 'show'
    new_frontmatter = frontmatter.rstrip() + "\nmode: 'show'"
    new_content = content.replace(f"---\n{frontmatter}\n---", f"---\n{new_frontmatter}\n---", 1)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {file_path}")
    return True

# 扫描所有 .mdx 文件
def scan_directory(directory):
    added_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mdx'):
                file_path = os.path.join(root, file)
                if add_mode_to_openapi_file(file_path):
                    added_count += 1
    return added_count

# 扫描 apis 目录
print("正在扫描 apis/ 目录...")
count = scan_directory('apis')

print(f"\n🎉 完成！为 {count} 个 OpenAPI 页面添加了 mode: 'show'")
