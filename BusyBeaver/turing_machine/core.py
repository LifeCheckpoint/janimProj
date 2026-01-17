from __future__ import annotations
from collections import defaultdict
from typing import Dict, Tuple, List, Optional
from .models import Direction, Transition, StepResult

class TuringMachineCore:
    def __init__(
        self, 
        initial_tape: str | List[str] = "", 
        start_state: str = "Q0", 
        blank_symbol: str = "0", 
        halt_states: Optional[List[str]] = None
    ) -> None:
        # 内部状态
        self._tape: Dict[int, str] = defaultdict(lambda: blank_symbol)
        content = list(initial_tape)
        for i, char in enumerate(content):
            self._tape[i] = char
            
        self._head: int = 0
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
        """添加规则，内部自动构建 Transition 模型"""
        rule = Transition(
            next_state=next_state, 
            write_symbol=write_symbol, 
            direction=direction
        )
        self._transitions[(state, read_symbol)] = rule

    @property
    def current_info(self) -> StepResult:
        """获取当前状态"""
        curr_symbol = self._tape[self._head]
        applied = self._transitions.get((self._state, curr_symbol))
        
        return StepResult(
            step=self._step_count,
            state=self._state,
            head_index=self._head,
            current_symbol=curr_symbol,
            is_halted=self._is_halted,
            transition_applied=applied
        )

    def step(self) -> StepResult:
        """执行一步并返回结果"""
        if self._is_halted:
            return self.current_info

        curr_symbol = self._tape[self._head]
        rule = self._transitions.get((self._state, curr_symbol))

        if not rule:
            self._is_halted = True
            return self.current_info

        # 写入并更新状态
        self._tape[self._head] = rule.write_symbol
        self._state = rule.next_state
        
        # 移动读写头
        if rule.direction == "L":
            self._head -= 1
        elif rule.direction == "R":
            self._head += 1
            
        self._step_count += 1
        
        # 停机判定
        if self._state in self._halt_states:
            self._is_halted = True

        return self.current_info

    def get_tape_snapshot(self, left: int, right: int) -> List[str]:
        """获取范围内的纸带快照"""
        return [self._tape[i] for i in range(left, right + 1)]
