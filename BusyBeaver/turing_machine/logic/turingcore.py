from __future__ import annotations
from typing import Dict, Tuple, List, Optional, Literal, cast
from .tapecore import InfiniteTape

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


class TuringMachineCore:
    """
    图灵机核心逻辑类。
    
    使用 InfiniteTape 管理纸带数据，支持规则添加、单步执行及状态查询。
    """

    def __init__(
        self, 
        initial_tape: str | List[str] = "", 
        start_state: str = "Q0", 
        blank_symbol: str = "0", 
        halt_states: Optional[List[str]] = None
    ) -> None:
        """
        初始化图灵机。

        :param initial_tape: 初始纸带内容，可以是字符串或字符列表。
        :type initial_tape: str | List[str]
        :param start_state: 初始状态名称，默认为 "Q0"。
        :type start_state: str
        :param blank_symbol: 空白符号，默认为 "0"。
        :type blank_symbol: str
        :param halt_states: 停机状态列表。如果为 None，则默认为 {"HALT", "ACCEPT", "REJECT"}。
        :type halt_states: Optional[List[str]]
        """
        # 使用 InfiniteTape 管理纸带
        self._tape: InfiniteTape[str] = InfiniteTape[str](empty_value=blank_symbol)
        
        # 写入初始数据
        content = list(initial_tape)
        self._tape.write_batch_absolute(content, 0)
            
        self._state: str = start_state
        self._blank_symbol: str = blank_symbol
        self._halt_states: set[str] = set(halt_states) if halt_states else {"HALT", "ACCEPT", "REJECT"}
        
        # 转移表：{(当前状态, 读取符号): Transition模型}
        self._transitions: Dict[Tuple[str, str], Transition] = {}
        
        self._step_count: int = 0
        self._is_halted: bool = False

    def add_rule(
        self, 
        state: str, 
        read_symbol: str, 
        next_state: str, 
        write_symbol: str, 
        direction: Direction
    ) -> None:
        """
        添加转移规则。

        :param state: 当前状态。
        :type state: str
        :param read_symbol: 读取的符号。
        :type read_symbol: str
        :param next_state: 下一个状态。
        :type next_state: str
        :param write_symbol: 写入的符号。
        :type write_symbol: str
        :param direction: 移动方向 ("L", "R" 或 "S")。
        :type direction: Direction
        :return: None
        """
        rule = Transition(
            next_state=next_state, 
            write_symbol=write_symbol, 
            direction=direction
        )
        self._transitions[(state, read_symbol)] = rule

    @property
    def current_info(self) -> StepResult:
        """
        获取当前图灵机的运行状态信息。

        :return: 包含步骤、状态、读写头位置、当前符号等信息的 StepResult 对象。
        :rtype: StepResult
        """
        # 获取当前读写头位置的符号
        curr_symbol = cast(str, self._tape.read_absolute(self._tape._pointer))
        applied = self._transitions.get((self._state, curr_symbol))
        
        return StepResult(
            step=self._step_count,
            state=self._state,
            head_index=self._tape._pointer,
            current_symbol=curr_symbol,
            is_halted=self._is_halted,
            transition_applied=applied
        )

    def step(self) -> StepResult:
        """
        执行一步图灵机操作。
        
        根据当前状态和读写头下的符号，查找并执行对应的转移规则。
        如果没有匹配的规则，图灵机将停机。

        :return: 执行后的状态信息。
        :rtype: StepResult
        """
        if self._is_halted:
            return self.current_info

        # 读取当前符号
        curr_symbol = cast(str, self._tape.read_absolute(self._tape._pointer))
        rule = self._transitions.get((self._state, curr_symbol))

        if not rule:
            self._is_halted = True
            return self.current_info

        # 写入新符号
        self._tape.write_absolute(self._tape._pointer, rule.write_symbol)
        # 更新状态
        self._state = rule.next_state
        
        # 移动读写头
        if rule.direction == "L":
            self._tape._pointer -= 1
        elif rule.direction == "R":
            self._tape._pointer += 1
        elif rule.direction == "S":
            pass # 不移动
            
        self._step_count += 1
        
        # 停机判定
        if self._state in self._halt_states:
            self._is_halted = True

        return self.current_info

    def get_tape_snapshot(self, left: int, right: int) -> List[str]:
        """
        获取指定范围内的纸带快照。

        :param left: 起始绝对索引。
        :type left: int
        :param right: 结束绝对索引。
        :type right: int
        :return: 包含指定范围内符号的列表。
        :rtype: List[str]
        """
        return [cast(str, self._tape.read_absolute(i)) for i in range(left, right + 1)]
