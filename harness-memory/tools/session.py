# tools/session.py

"""
Harness 会话管理工具

核心原则：
- 捕获关键决策，丢弃闲聊
- 结构化输出，便于检索
- 自动关联历史记忆
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Decision:
    """关键决策记录"""
    question: str      # 决策问题
    choice: str        # 做出的选择
    reason: str        # 决策原因
    timestamp: str     # 时间戳


@dataclass
class TodoItem:
    """待办事项"""
    content: str       # 待办内容
    completed: bool    # 是否完成
    source: str        # 来源（如会话ID）


@dataclass
class SessionSummary:
    """会话摘要"""
    session_id: str
    start_time: str
    end_time: str
    decisions: List[Decision]
    todos: List[TodoItem]
    related_memories: List[Dict]  # 关联的历史记忆
    notes: str  # 额外备注


def session_capture(messages: List[Dict], capture_range: Optional[tuple] = None) -> Dict:
    """
    捕获会话关键信息
    
    Args:
        messages: 会话消息列表
        capture_range: 捕获范围 (start_idx, end_idx)
    
    Returns:
        结构化的会话数据
    """
    if capture_range:
        start, end = capture_range
        messages = messages[start:end]
    
    # 提取关键信息（简化版，实际可接入LLM分析）
    decisions = []
    todos = []
    
    for msg in messages:
        content = msg.get('content', '')
        
        # 简单启发式提取（实际应使用LLM）
        if '决定' in content or '选择' in content or '用' in content:
            decisions.append({
                'raw': content,
                'timestamp': msg.get('timestamp', datetime.now().isoformat())
            })
        
        if '待办' in content or 'TODO' in content or '记得' in content:
            todos.append({
                'raw': content,
                'completed': '[x]' in content or '完成' in content,
                'timestamp': msg.get('timestamp', datetime.now().isoformat())
            })
    
    return {
        'message_count': len(messages),
        'decisions_raw': decisions,
        'todos_raw': todos,
        'captured_at': datetime.now().isoformat()
    }


def session_summarize(session_data: Dict, format_type: str = "standard") -> str:
    """
    生成会话摘要
    
    Args:
        session_data: 会话数据（来自 session_capture）
        format_type: 输出格式 (standard/compact/full)
    
    Returns:
        格式化摘要文本
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    
    if format_type == "standard":
        lines = [
            f"## 会话摘要 [{timestamp}]",
            "",
            "### 关键决策",
            "| 决策点 | 选择 | 原因 |",
            "|--------|------|------|",
        ]
        
        for d in session_data.get('decisions_raw', []):
            lines.append(f"| {d['raw'][:30]}... | - | - |")
        
        if not session_data.get('decisions_raw'):
            lines.append("| （无明确决策） | - | - |")
        
        lines.extend([
            "",
            "### 待办状态",
        ])
        
        for t in session_data.get('todos_raw', []):
            status = "[x]" if t['completed'] else "[ ]"
            lines.append(f"- {status} {t['raw'][:50]}")
        
        if not session_data.get('todos_raw'):
            lines.append("- （无待办事项）")
        
        lines.extend([
            "",
            "### 关联记忆",
            "- （待检索关联）",
        ])
        
        return '\n'.join(lines)
    
    elif format_type == "compact":
        return f"[{timestamp}] 决策:{len(session_data.get('decisions_raw', []))} 待办:{len(session_data.get('todos_raw', []))}"
    
    else:  # full
        return json.dumps(session_data, ensure_ascii=False, indent=2)


def session_archive(summary: str, target_path: str) -> Dict:
    """
    归档会话摘要
    
    Args:
        summary: 会话摘要内容
        target_path: 目标文件路径
    
    Returns:
        操作结果
    """
    try:
        from tools.memory import memory_write
        result = memory_write(target_path, summary, mode="append")
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 便捷函数
def quick_summary(messages: List[Dict]) -> str:
    """快速生成会话摘要"""
    data = session_capture(messages)
    return session_summarize(data, format_type="standard")


if __name__ == "__main__":
    # 测试
    test_messages = [
        {'content': '我们决定用 React 而不是 Vue', 'timestamp': '2026-04-18T10:00:00'},
        {'content': '待办：下次确定组件库', 'timestamp': '2026-04-18T10:05:00'},
    ]
    print(quick_summary(test_messages))
