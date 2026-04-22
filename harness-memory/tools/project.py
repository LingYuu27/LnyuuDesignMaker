# tools/project.py

"""
Harness 项目索引工具

核心原则：
- 项目隔离，不混杂
- 自动索引，减少手工
- 关联可追溯
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Optional, Set
from dataclasses import dataclass

# 配置
PROJECT_ROOT = "C:\\Users\\User\\project"
INDEX_FILE = os.path.join(PROJECT_ROOT, "harness-memory", "INDEX.md")


@dataclass
class ProjectFile:
    """项目文件记录"""
    path: str
    project: str
    file_type: str  # doc, code, config, etc.
    last_modified: str
    key_content: str  # 一句话摘要


def project_index(project_name: str, file_patterns: List[str] = None) -> Dict:
    """
    建立项目索引
    
    Args:
        project_name: 项目名称
        file_patterns: 文件匹配模式（如 ['*.md', '*.py']）
    
    Returns:
        索引结果
    """
    if file_patterns is None:
        file_patterns = ['*.md']
    
    project_files = []
    project_dirs = [
        os.path.join(PROJECT_ROOT, project_name),
        os.path.join(PROJECT_ROOT, "memory"),
    ]
    
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            continue
        
        for root, dirs, files in os.walk(project_dir):
            # 跳过隐藏目录和特定目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for filename in files:
                # 检查是否匹配模式
                matched = any(re.match(p.replace('*', '.*'), filename) for p in file_patterns)
                if not matched:
                    continue
                
                filepath = os.path.join(root, filename)
                try:
                    stat = os.stat(filepath)
                    modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # 提取关键内容（前200字符）
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read(200)
                            # 提取第一行非空行作为摘要
                            lines = [l.strip() for l in content.split('\n') if l.strip()]
                            key_content = lines[0] if lines else "(无内容)"
                    except:
                        key_content = "(无法读取)"
                    
                    project_files.append({
                        'path': filepath,
                        'filename': filename,
                        'project': project_name,
                        'last_modified': modified,
                        'key_content': key_content[:50]
                    })
                except Exception as e:
                    continue
    
    return {
        'project': project_name,
        'file_count': len(project_files),
        'files': project_files,
        'indexed_at': datetime.now().isoformat()
    }


def project_link(source_path: str, target_path: str, relation_type: str = "related") -> Dict:
    """
    建立文件关联
    
    Args:
        source_path: 源文件路径
        target_path: 目标文件路径
        relation_type: 关联类型 (related/derived/supersedes)
    
    Returns:
        操作结果
    """
    # 关联记录存储在 harness-memory/links.json
    links_file = os.path.join(PROJECT_ROOT, "harness-memory", "links.json")
    
    try:
        if os.path.exists(links_file):
            with open(links_file, 'r', encoding='utf-8') as f:
                links = json.load(f)
        else:
            links = {}
        
        source_key = source_path.replace(PROJECT_ROOT, "")
        if source_key not in links:
            links[source_key] = []
        
        links[source_key].append({
            'target': target_path.replace(PROJECT_ROOT, ""),
            'type': relation_type,
            'created_at': datetime.now().isoformat()
        })
        
        with open(links_file, 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "source": source_path,
            "target": target_path,
            "relation": relation_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def topic_cluster(files: List[str], cluster_method: str = "project") -> Dict:
    """
    主题聚类
    
    Args:
        files: 文件路径列表
        cluster_method: 聚类方法 (project/filename/keyword)
    
    Returns:
        聚类结果
    """
    clusters = {}
    
    for filepath in files:
        if cluster_method == "project":
            # 按目录/项目聚类
            parts = filepath.replace(PROJECT_ROOT, "").strip('\\/').split('\\')
            key = parts[0] if parts else "其他"
        
        elif cluster_method == "filename":
            # 按文件名关键词聚类
            filename = os.path.basename(filepath)
            # 提取日期前缀或关键词
            match = re.match(r'(\d{4}-\d{2})', filename)
            key = match.group(1) if match else "其他"
        
        else:
            key = "默认"
        
        if key not in clusters:
            clusters[key] = []
        clusters[key].append(filepath)
    
    return {
        'method': cluster_method,
        'cluster_count': len(clusters),
        'clusters': clusters
    }


def update_index_md(project_name: str, files_info: List[Dict]) -> Dict:
    """
    更新 INDEX.md
    
    Args:
        project_name: 项目名称
        files_info: 文件信息列表
    
    Returns:
        操作结果
    """
    try:
        from tools.memory import memory_get, memory_update
        
        # 读取现有 INDEX.md
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# INDEX.md - 记忆索引\n\n"
        
        # 生成新的项目索引表格
        new_section = f"\n## {project_name}\n\n"
        new_section += "| 文件 | 关键内容 | 最后更新 |\n"
        new_section += "|------|----------|----------|\n"
        
        for f in files_info:
            filename = os.path.basename(f['path'])
            link = f"[{filename}](file:///{f['path']})"
            new_section += f"| {link} | {f['key_content']} | {f['last_modified'][:10]} |\n"
        
        # 检查是否已有该项目section
        pattern = f"## {re.escape(project_name)}\\n\\n"
        if re.search(pattern, content):
            # 更新现有section
            old_section_match = re.search(f"## {re.escape(project_name)}.*?\\n(?=## |$)", content, re.DOTALL)
            if old_section_match:
                old_section = old_section_match.group(0)
                content = content.replace(old_section, new_section)
        else:
            # 添加新section
            content += new_section
        
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "index_file": INDEX_FILE,
            "project": project_name,
            "file_count": len(files_info)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 便捷函数
def quick_index(project_name: str) -> str:
    """快速建立项目索引"""
    result = project_index(project_name)
    if result['file_count'] > 0:
        update_result = update_index_md(project_name, result['files'])
        if update_result['success']:
            return f"✅ 索引完成: {project_name} ({result['file_count']} 个文件)"
    return f"⚠️ 索引失败或无可索引文件"


if __name__ == "__main__":
    # 测试
    print(quick_index("harness-memory"))
