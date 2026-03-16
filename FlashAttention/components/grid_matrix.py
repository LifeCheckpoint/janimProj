from janim.imports import * # type: ignore
from typing import cast

def create_grid_matrix_cell(
    value: str,
    cell_length: float = 1.0,
    fill: str = "#19043A",
    stroke: str = "#eeeeee",
    text_color = "#eeeeee",
    text_scaling: float = 1.0,
) -> Group:
    """
    创建一个网格矩阵单元格，包含一个背景矩形和一个文本对象。
    """
    bg = Rect(cell_length, cell_length)
    bg.fill.set(color=fill, alpha=1.0)
    bg.stroke.set(color=stroke)
    text = TypstMath(value, color=text_color)
    text.points.scale(text_scaling)
    
    return Group(bg, text)


def create_grid_matrix(
    rows: int,
    cols: int,
    create_cell_fn_by_1d: Callable[[int], Group] | None = None,
    create_cell_fn_by_2d: Callable[[int, int], Group] | None = None,
    buff: float = 0.1,
) -> Group:
    """
    创建一个网格，可以通过提供一个函数来创建每个单元格。函数可以是基于一维索引的，也可以是基于二维索引的。
    """
    if not create_cell_fn_by_1d and not create_cell_fn_by_2d:
        raise ValueError("必须提供至少一个创建单元格的函数")
    if create_cell_fn_by_1d and create_cell_fn_by_2d:
        raise ValueError("只能提供一个创建单元格的函数")
    
    cells = None
    if create_cell_fn_by_1d:
        cells = Group.from_iterable(
            create_cell_fn_by_1d(i) for i in range(rows * cols)
        )
    if create_cell_fn_by_2d:
        cells = Group.from_iterable(
            create_cell_fn_by_2d(i, j) for i in range(rows) for j in range(cols)
        )
    
    cells = cast(Group, cells)
    cells.points.arrange_in_grid(n_rows=rows, n_cols=cols, buff=buff)
    return cells


def get_cell_at(grid_matrix: Group[Group], row: int, col: int, cols: int) -> Group:
    """
    获取网格矩阵中指定行列位置的单元格。假设单元格是按照行优先顺序排列的。
    """
    index = row * cols + col
    return grid_matrix[index]


def get_cells_at(grid_matrix: Group[Group], cols: int, row_range: tuple[int, int], col_range: tuple[int, int]) -> Group:
    """
    获取网格矩阵中指定行列范围内的单元格。假设单元格是按照行优先顺序排列的。

    range 为左闭右开区间，即 [start, end)
    """
    cells = Group()
    for row in range(row_range[0], row_range[1]):
        for col in range(col_range[0], col_range[1]):
            cell = get_cell_at(grid_matrix, row, col, cols)
            cells.add(cell)
    return cells


