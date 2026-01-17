from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

Direction = Literal["L", "R", "S"]
"""移动方向类型，L 表示左移，R 表示右移，S 表示不动"""

class Transition(BaseModel):
    """转移规则模型"""
    next_state: str
    """下一状态"""
    
    write_symbol: str
    """写入符号"""
    
    direction: Direction
    """下一步移动方向"""

class StepResult(BaseModel):
    """单步执行结果模型"""
    model_config = ConfigDict(from_attributes=True)
    
    step: int
    """当前步骤数"""
    
    state: str
    """当前状态"""
    
    head_index: int
    """磁带头位置"""
    
    current_symbol: str
    """当前读取的符号"""
    
    is_halted: bool
    """是否停机"""
    
    transition_applied: Optional[Transition] = None
    """这一步所执行的规则，如果没有匹配规则则为 None"""
