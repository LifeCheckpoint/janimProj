from __future__ import annotations

from janim.imports import * # type: ignore
from typing import List, Optional
from .history_cell import HistoryCell

if TYPE_CHECKING:
    from ..turing_machine.logic.tapecore import InfiniteTape

class HistoryGrid(Group):
    def __init__(
        self,
        tape_range: range,
        initial_history: Optional[List[InfiniteTape]] = None,
        cell_size: float = 0.6,
        buff: float = 0.05,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.tape_range = tape_range
        self.cell_size = cell_size
        self.buff = buff
        
        self.columns = Group()
        self.time_labels = Group()
        
        self.add(self.columns, self.time_labels)
        
        # "Time ->" 标签
        self.time_axis_label = Group(
            TypstText(R"#text(fill: orange)[Time]"),
            Arrow(LEFT, RIGHT, color=ORANGE).points.scale(0.4).r
        ).points.arrange(RIGHT, buff=0.2).r
        
        self.add(self.time_axis_label)
        
        if initial_history:
            for t, tape in enumerate(initial_history):
                self.add_column(tape, t)
        
        self._update_layout()

    def add_column(self, tape: InfiniteTape, time: int):
        column = Group()
        for i in self.tape_range:
            val = str(tape.read_absolute(i))
            cell = HistoryCell(val, square_size=self.cell_size)
            column.add(cell)
        
        column.points.arrange(DOWN, buff=self.buff)
        
        if len(self.columns) > 0:
            column.points.next_to(self.columns, RIGHT, buff=self.buff)
        
        self.columns.add(column)
        
        label = Text(str(time), font_size=24, color=GOLD)
        label.points.next_to(column, DOWN, buff=0.2)
        self.time_labels.add(label)
        
        self._update_layout()

    def _update_layout(self):
        if len(self.time_labels) > 0:
            self.time_axis_label.points.next_to(self.time_labels, DOWN, buff=0.2)
            self.time_axis_label.points.align_to(self.time_labels, LEFT)

    def get_add_column_anim(self, tape: InfiniteTape, time: int, duration: float = 1.0):
        """
        获取“显示新一列time时间点的图灵机纸带状态”的动画
        """
        new_column = Group()
        for i in self.tape_range:
            val = str(tape.read_absolute(i))
            cell = HistoryCell(val, square_size=self.cell_size)
            new_column.add(cell)
        
        new_column.points.arrange(DOWN, buff=self.buff)
        
        if len(self.columns) > 0:
            new_column.points.next_to(self.columns, RIGHT, buff=self.buff)
        
        new_label = Text(str(time), font_size=24, color=GOLD)
        new_label.points.next_to(new_column, DOWN, buff=0.2)
        
        def update_state():
            self.columns.add(new_column)
            self.time_labels.add(new_label)
            self._update_layout()

        return Succession(
            AnimGroup(
                FadeIn(new_column),
                FadeIn(new_label),
                duration=duration
            ),
            Do(update_state)
        )
