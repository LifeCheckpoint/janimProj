from janim.imports import * # type: ignore
from typing import List, Optional, Tuple, Set, Any
from .components.paper_tile import InfinityTapeItem
from .components.grid_table import GridTable
from .components.tape_cell import TapeCell
from .components.turing_counter import TuringCounter
from .logic.turingcore import TuringMachineCore, StepResult

class TuringMachine(Group):
    """
    图灵机动画物体
    组装了纸带 (InfinityTapeItem) 和状态转移表 (GridTable)
    """
    def __init__(
        self,
        turing_core: TuringMachineCore,
        showcase_radius: int = 5,
        table_scaling: float = 0.8,
        counter_scaling: float = 0.6,
        table_config: Optional[dict[str, Any]] = None,
        tape_config: Optional[dict[str, Any]] = None,
        counter_config: Optional[dict[str, Any]] = None,
        **kwargs
    ):
        self.core = turing_core
        self.showcase_radius = showcase_radius
        self.table_config = table_config or {}
        self.tape_config = tape_config or {}
        self.counter_config = counter_config or {}
        
        self.is_table_shown = False
        self.is_counter_shown = False
        self.last_active_cell = None

        super().__init__(**kwargs)
        
        self._setup_machine()
        self._init_layout(table_scaling, counter_scaling)
        
        self.table.hide()
        
    def _setup_machine(self):
        # 初始化纸带
        tape_copy = self.core._tape.model_copy(deep=True)
        
        self.tape_item = InfinityTapeItem(
            showcase_radius=self.showcase_radius,
            init_tape=tape_copy,
            cell_setting=lambda index, value: TapeCell(
                tile_data=value,
                index=index,
            ),
            **self.tape_config
        )
        
        # 初始化状态转移表
        states: Set[str] = set()
        symbols: Set[str] = set()
        
        states.add(self.core._state)
        symbols.add(self.core._blank_symbol)
        
        for (state, symbol), trans in self.core._transitions.items():
            states.add(state)
            symbols.add(symbol)
            states.add(trans.next_state)
            symbols.add(trans.write_symbol)
            
        states.update(self.core._halt_states)
            
        sorted_states = sorted(list(states))
        sorted_symbols = sorted(list(symbols))
        
        self.table = GridTable(
            states=sorted_states,
            symbols=sorted_symbols,
            transitions=self.core._transitions,
            **self.table_config
        )

        # 初始化计数器
        self.counter = TuringCounter(**self.counter_config)
        self.counter.hide()
        
        # 将子组件添加到 Group 中
        self.add(self.tape_item, self.table, self.counter)
        
    def _init_layout(self, table_scaling: float, counter_scaling: float):
        self.tape_item.points.scale(0.7)
        self.tape_item.points.move_to(DOWN * 1.5)
        
        self.counter.points.scale(counter_scaling)
        self.counter.points.next_to(self.tape_item.pointer, LEFT, buff=0.75)

        self.table.points.scale(table_scaling)
        self.table.points.next_to(self.tape_item, UP, buff=0.25).shift(LEFT * 0.25)
        
    def show_table_anim(self, duration: float = 1.0) -> AnimGroup:
        """
        显示表格动画
        """
        if self.is_table_shown:
            return AnimGroup()
            
        self.is_table_shown = True
        return AnimGroup(
            FadeIn(self.table, duration=duration),
            self.tape_item.anim(duration=duration).points.shift(DOWN * 0.25), # type: ignore
        )
        
    def hide_table_anim(self, duration: float = 1.0) -> AnimGroup:
        """
        隐藏表格动画
        """
        if not self.is_table_shown:
            return AnimGroup()
            
        self.is_table_shown = False
        return AnimGroup(
            FadeOut(self.table, duration=duration),
            self.tape_item.anim(duration=duration).points.shift(UP * 0.25), # type: ignore
        )

    def show_counter_anim(self, duration: float = 1.0) -> AnimGroup:
        """
        显示计数器动画
        """
        if self.is_counter_shown:
            return AnimGroup()
            
        self.is_counter_shown = True
        return AnimGroup(
            FadeIn(self.counter, duration=duration)
        )

    def hide_counter_anim(self, duration: float = 1.0) -> AnimGroup:
        """
        隐藏计数器动画
        """
        if not self.is_counter_shown:
            return AnimGroup()
            
        self.is_counter_shown = False
        return AnimGroup(
            FadeOut(self.counter, duration=duration)
        )
        
    def step(self, duration: float = 1.0) -> list[Animation]:
        """
        执行一步图灵机操作并返回动画序列

        :return: 动画序列，由于使用 Succession 在当前版本会有状态更新 Bug，返回 list 以供外部 play 使用
        :rtype: list[Animation]
        """
        pre_info = self.core.current_info
        self.core.step()
        
        # 构建动画序列
        anims = []
        
        # 表格高亮动画
        if self.is_table_shown:
            # 获取对应单元格
            cell = self.table.get_cell(pre_info.state, pre_info.current_symbol)
            
            if cell:
                # 如果有上一个高亮且不是当前这个，先取消高亮
                if self.last_active_cell and self.last_active_cell != cell:
                    anims.append(self.last_active_cell.animate_active(False, duration=duration/4))
                
                # 高亮当前规则
                anims.append(cell.animate_active(True, duration=duration/4))
                self.last_active_cell = cell
            elif self.last_active_cell:
                # 如果没有匹配规则，取消之前的规则高亮
                anims.append(self.last_active_cell.animate_active(False, duration=duration/4))
                self.last_active_cell = None
        
        # 如果已经停机，且没有规则应用，只返回高亮清除动画
        if pre_info.is_halted and not pre_info.transition_applied:
             return anims

        # 纸带写入动画
        if pre_info.transition_applied:
            write_val = pre_info.transition_applied.write_symbol
            # tape_item.set_value 会更新 tape_item 内部的 tape 副本
            anims.append(self.tape_item.set_value(write_val, transform_time=duration / 2))
            
            # 纸带移动动画
            direction = pre_info.transition_applied.direction
            if direction == "R":
                anims.append(self.tape_item.tape_shift_left(duration=duration / 2))
            elif direction == "L":
                anims.append(self.tape_item.tape_shift_right(duration=duration / 2))

        # 更新计数器
        anims.append(self.counter.anim_set_value(self.core._step_count, duration=duration))
            
        return anims
