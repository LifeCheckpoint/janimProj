from janim.imports import * # type: ignore
from typing import List, Dict, Tuple, Optional
from ..logic.turingcore import Transition
from .grid_cell import GridCell, local_font

class GridTable(Group):
    def __init__(
        self,
        states: List[str],
        symbols: List[str],
        transitions: Dict[Tuple[str, str], Transition],
        transpose: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        self.transpose = transpose
        self.cells: Dict[Tuple[str, str], GridCell] = {}

        self._build_table()

    def _build_table(self):
        cell_w = 1.1
        cell_h = 1.1
        buff = 0.1

        rows = self.symbols if self.transpose else self.states
        cols = self.states if self.transpose else self.symbols

        # Create Cells first to use them for header positioning
        for i, row_name in enumerate(rows):
            for j, col_name in enumerate(cols):
                state = col_name if self.transpose else row_name
                symbol = row_name if self.transpose else col_name

                trans = self.transitions.get((state, symbol))

                if trans:
                    d_map = {"R": "RIGHT", "L": "LEFT", "S": "STOP"}
                    move_dir = d_map.get(trans.direction, "STOP")
                    next_state = trans.next_state
                    write_val = trans.write_symbol
                else:
                    move_dir = "STOP"
                    next_state = "HALT"
                    write_val = symbol

                cell = GridCell(
                    state_name=next_state,
                    write_bit=write_val,
                    move_dir=move_dir,
                    is_active=False,
                    width=cell_w,
                    height=cell_h
                )

                x = j * (cell_w + buff)
                y = -i * (cell_h + buff)
                cell.points.move_to([x, y, 0])

                self.cells[(state, symbol)] = cell
                self.add(cell)

        # Create Column Headers
        for j, col_name in enumerate(cols):
            header = Text(col_name, font_size=24, font=local_font, color="#BBBBBB")
            # Get the first cell in this column
            # If transpose: state=cols[j], symbol=rows[0]
            # If not transpose: state=rows[0], symbol=cols[j]
            state = cols[j] if self.transpose else rows[0]
            symbol = rows[0] if self.transpose else cols[j]
            first_cell_in_col = self.cells[(state, symbol)]
            header.points.next_to(first_cell_in_col, UP, buff=0.15)
            self.add(header)

        # Create Row Headers
        for i, row_name in enumerate(rows):
            header = Text(row_name, font_size=24, font=local_font, color="#BBBBBB")
            # Get the first cell in this row
            # If transpose: state=cols[0], symbol=rows[i]
            # If not transpose: state=rows[i], symbol=cols[0]
            state = cols[0] if self.transpose else rows[i]
            symbol = rows[i] if self.transpose else cols[0]
            first_cell_in_row = self.cells[(state, symbol)]
            header.points.next_to(first_cell_in_row, LEFT, buff=0.15)
            self.add(header)

        self.points.move_to(ORIGIN)

    def get_cell(self, state: str, symbol: str) -> Optional[GridCell]:
        return self.cells.get((state, symbol))
        
    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], str):
            return self.cells[key]
        return super().__getitem__(key)
