# tools/memory.py

"""
Harness 记忆读写工具

核心原则：
- 熵减优先：优先更新，不新建
- 精准操作：使用行号定位，不全文覆盖
- 链接友好：返回路径+行号，便于引用
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# 配置
MEMORY_DIR = "C:\\Users\\User\\project\\memory"
HARNESS_DIR = "C:\\Users\\User\\project\\harness-memory"


@dataclass
class MemorySnippet:
    """记忆片段"""
    path: str
    line_start: int
    line_end: int
    content: str
    score: float  # 相关度分数


def memory_search(query: str, max_results: int = 5, min_score: float = 0.3) -> List[MemorySnippet]:
    """
    语义检索记忆文件
    
    Args:
        query: 检索关键词
        max_results: 最大返回结果数
        min_score: 最低相关度阈值
    
    Returns:
        匹配的记忆片段列表
    """
    results = []
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    
    # 遍历记忆目录
    for root, dirs, files in os.walk(MEMORY_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    content = ''.join(lines)
            except Exception as e:
                continue
            
            # 简单相关度计算（基于关键词匹配）
            content_lower = content.lower()
            matches = sum(1 for term in query_terms if term in content_lower)
            score = matches / len(query_terms) if query_terms else 0
            
            if score < min_score:
                continue
            
            # 找到匹配内容所在的行范围
            match_lines = []
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if any(term in line_lower for term in query_terms):
                    match_lines.append(i)
            
            if match_lines:
                # 取第一个匹配点，前后各扩展3行
                start = max(0, match_lines[0] - 3)
                end = min(len(lines), match_lines[0] + 4)
                snippet_content = ''.join(lines[start:end])
                
                results.append(MemorySnippet(
                    path=filepath,
                    line_start=start + 1,  # 1-based
                    line_end=end,
                    content=snippet_content.strip(),
                    score=score
                ))
    
    # 按相关度排序，取前N个
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:max_results]


def memory_get(path: str, from_line: int = 1, lines: int = 50) -> str:
    """
    精准读取记忆片段
    
    Args:
        path: 文件绝对路径
        from_line: 起始行号（1-based）
        lines: 读取行数
    
    Returns:
        指定范围的文件内容
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            start = from_line - 1  # 0-based
            end = start + lines
            return ''.join(all_lines[start:end])
    except Exception as e:
        return f"Error reading file: {e}"


def memory_write(path: str, content: str, mode: str = "append") -> Dict:
    """
    写入记忆
    
    Args:
        path: 目标文件路径
        content: 要写入的内容
        mode: "append" 追加, "overwrite" 覆盖
    
    Returns:
        操作结果信息
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if mode == "append" and os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as f:
                f.write('\n\n' + content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            "success": True,
            "path": path,
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def memory_update(path: str, old_text: str, new_text: str) -> Dict:
    """
    精准更新记忆片段
    
    Args:
        path: 目标文件路径
        old_text: 要替换的文本（必须精确匹配）
        new_text: 新文本
    
    Returns:
        操作结果信息
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text not in content:
            return {
                "success": False,
                "error": "old_text not found in file"
            }
        
        new_content = content.replace(old_text, new_text, 1)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            "success": True,
            "path": path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_file_link(path: str, line_start: int = 1, line_end: Optional[int] = None) -> str:
    """
    格式化文件链接（file:// 协议）
    
    Args:
        path: 文件绝对路径
        line_start: 起始行号
        line_end: 结束行号
    
    Returns:
        Markdown 格式的文件链接
    """
    filename = os.path.basename(path)
    if line_end and line_end != line_start:
        anchor = f"#L{line_start}-L{line_end}"
    else:
        anchor = f"#L{line_start}"
    
    return f"[{filename}](file:///{path}{anchor})"


# 便捷函数
def quick_search(query: str) -> str:
    """快速检索，返回格式化结果"""
    results = memory_search(query)
    if not results:
        return "未找到相关记忆。"
    
    output = [f"## 检索结果: '{query}'\n"]
    for i, snippet in enumerate(results, 1):
        link = format_file_link(snippet.path, snippet.line_start, snippet.line_end)
        output.append(f"{i}. {link}")
        output.append(f"   相关度: {snippet.score:.2f}")
        output.append(f"   预览: {snippet.content[:100]}...\n")
    
    return '\n'.join(output)


if __name__ == "__main__":
    # 测试
    print(quick_search("Harness"))
