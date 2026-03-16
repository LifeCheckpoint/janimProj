from janim.imports import * # type: ignore

with reloads():
    from components.colors import FAColor
    from components.utils import get_typ_doc
    from components.grid_matrix import create_grid_matrix_cell
    from components.memory_bar import MemoryBar

class TestGridMatrixCell(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background)
    )
    def construct(self) -> None:
        cells = Group.from_iterable(
            create_grid_matrix_cell(str(i), cell_length=0.5, text_scaling=0.8)
            for i in range(10)
        )
        cells.points.arrange_in_grid(n_rows=2, n_cols=5, buff=0.1)

        self.play(Write(cells))
        self.forward(2)

class TestMemoryBar(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background),
        typst_shared_preamble=get_typ_doc("preamble"),
    )
    def construct(self) -> None:
        memory_bar = MemoryBar(timeline=self)
        memory_bar.item.hide()
        
        self.forward(1)
        self.play(Write(memory_bar.item))
        self.forward(1)
        self.play(
            memory_bar.progress.anim.set_value(0.5),
            duration=2,
        )
        self.forward(1)
        self.play(
            memory_bar.progress.anim.set_value(1.5),
            duration=2,
        )
        self.forward(1)
        self.play(
            memory_bar.progress.anim.set_value(0.8),
            duration=2,
        )
        self.forward(1)
        self.play(FadeOut(memory_bar.item))
        self.forward(1)