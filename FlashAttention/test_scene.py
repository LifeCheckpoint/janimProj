from janim.imports import * # type: ignore

with reloads():
    from components.colors import FAColor
    from components.utils import get_typ_doc
    from components.grid_matrix import create_grid_matrix_cell
    from components.grid_matrix import *
    from components.memory_bar import MemoryBar
    from components.stride_background import create_stride_background
if TYPE_CHECKING:
    from components.colors import FAColor
    from components.utils import get_typ_doc
    from components.grid_matrix import create_grid_matrix_cell
    from components.grid_matrix import *
    from components.memory_bar import MemoryBar
    from components.stride_background import create_stride_background

class TestGridMatrixCell(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background_dark)
    )
    def construct(self) -> None:
        cells = Group.from_iterable(
            create_grid_matrix_cell(str(i), cell_length=0.5, text_scaling=0.8)
            for i in range(10)
        )
        cells.points.arrange_in_grid(n_rows=2, n_cols=5, buff=0.1)

        self.play(Write(cells))
        self.forward(2)

class TestGridMatrix(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background_light),
        typst_shared_preamble=get_typ_doc("preamble"),
    )
    def construct(self) -> None:
        m1 = create_grid_query(rows=5, cols=2)
        m2 = create_grid_key(rows=5, cols=2)
        m3 = create_grid_value(rows=5, cols=2)
        m4 = create_grid_mask(rows=5, cols=2)
        g = Group(m1, m2, m3, m4)
        g.points.arrange_in_grid(n_rows=1, n_cols=4, buff=0.5)
        self.play(Write(g))
        self.forward(2)

class TestMemoryBar(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background_light),
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

class TestStrideBackground(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background_dark)
    )
    def construct(self) -> None:
        stripes, mask = create_stride_background(
            width=6.0,
            height=3.0,
            gap=0.3,
        )
        text = TypstText("显存")
        text.points.scale(1.5).next_to(mask, DOWN, buff=0.5)

        self.play(Write(stripes), Write(text))
        self.forward(2)
        self.play(FadeOut(stripes), FadeOut(text))
        self.forward(1)

class TestMask(Timeline):
    def construct(self) -> None:
        xxx = Circle(color=YELLOW).points.move_to(ORIGIN).r
        yyy = Circle(color=RED).points.move_to(LEFT).r
        zzz = Circle(color=GREEN).points.move_to(RIGHT).r
        m1 = Rect(5, 1.5).points.move_to(UP * 0.5).r
        m2 = Rect(5, 1.5).points.move_to(DOWN * 0.5).r
        mask1 = ShapeMask(shape=m1, affected=[xxx, zzz])
        mask2 = ShapeMask(shape=m2, affected=[xxx, yyy])

        self.play(FadeIn(Group(xxx, yyy, zzz)))
        self.forward(1)
        self.play(FadeIn(mask1))
        self.play(FadeIn(mask2))
        self.forward(1)