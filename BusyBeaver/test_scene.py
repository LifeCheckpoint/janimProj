from janim.imports import * # type: ignore
from turing_machine.components.tape_cell import TapeCell
from turing_machine.effects.alpha_vignette import AlphaVignetteEffect
from turing_machine.effects.lens import LensEffect
from turing_machine.effects.identity import IdentityEffect
from turing_machine.components.paper_tile import InfinityTapeItem
from turing_machine.logic.tapecore import InfiniteTape
from turing_machine.components.grid_cell import GridCell
from turing_machine.components.grid_table import GridTable
from turing_machine.logic.turingcore import Transition
from turing_machine.turing_machine import TuringMachine
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.components.turing_counter import TuringCounter
from turing_machine.components.turing_machine_transform import TuringMachineTransform

from dowhen import goto
from janim.render.renderer_vitem_plane import VItemPlaneRenderer
source_hash = "f746551d"
goto("if self.vbo_points.size != self.vbo_mapped_points.size:").when(
    VItemPlaneRenderer._update_points_normal,
    "if new_attrs.points is not self.attrs.points \\",
    source_hash=source_hash
)

class PaperTileTest(Timeline):
    """
    uv run janim run test_scene.py PaperTileTest -i
    """

class TapeCellTest(Timeline):
    """
    uv run janim run test_scene.py TapeCellTest -i
    """
    CONFIG = Config(
        pixel_height=2160,
        pixel_width=3840,
    )

    def construct(self):
        ch0 = R"#text(fill: white)[0]"
        cell = TapeCell(tile_data=ch0)
        self.forward()
        self.play(Create(cell))
        self.forward()
        cell.get_chromatic_effect().show()
        self.play(
            cell.create_chromatic_in_updater(duration=4.0, intensity=20)
        )
        self.play(
            cell.stop_chromatic_in_updater(intensity=20)
        )
        self.forward(1)

class RotatingTapeCellTest(Timeline):
    """
    uv run janim run test_scene.py RotatingTapeCellTest -i
    """
    def construct(self):
        tl1 = TapeCellTest().build().to_item().show()
        rotate = TransformableFrameClip(tl1, scale=(0.5, 0.5)).show()
        self.play(
            DataUpdater(
                rotate,
                lambda data, p: data.clip.set(rotate=PI * p.alpha)
            ),
            duration=tl1.duration,
            rate_func=smooth
        )

class TapeCellTest2(Timeline):
    """
    uv run janim run test_scene.py TapeCellTest2 -i
    """
    def construct(self):
        ch0 = R"#text(fill: white)[0]"
        ch1 = R"#text(fill: red)[1]"
        ch2 = R"#text(fill: blue)[2]"
        ch3 = R"#text(fill: green)[3]"
        cell = TapeCell(tile_data=ch0)
        self.forward()
        self.play(Create(cell))
        self.forward()
        cell.get_chromatic_effect().show()
        self.play(
            cell.create_chromatic_in_updater(duration=4.0, intensity=20)
        )
        self.play(
            cell.stop_chromatic_in_updater(intensity=20)
        )
        self.forward(1)
        self.play(
            cell.create_set_value_animation(ch1)
        )
        self.forward(1)
        self.play(
            cell.create_set_value_animation(ch2)
        )
        self.forward(1)
        self.play(
            cell.create_set_value_animation(ch3)
        )
        self.forward(1)
        self.play(
            cell.create_clear_value_animation()
        )
        self.forward(1)

class AlphaVignetteEffectTest(Timeline):
    """
    uv run janim run test_scene.py AlphaVignetteEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2).fill.set(color=BLUE, alpha=1).r
        vignette = AlphaVignetteEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        vignette.show()
        self.forward(2)
        self.play(
            DataUpdater(
                vignette,
                lambda item, p: item.apply_uniforms_set(
                    vignette_radius=0.8 - 0.5 * p.alpha,
                    vignette_softness=0.4,
                    vignette_intensity=1.0 + 2.0 * p.alpha,
                    aspect_ratio=1.77,
                ),
            ),
            duration=4.0,
            rate_func=smooth
        )

class LensEffectTest(Timeline):
    """
    uv run janim run test_scene.py LensEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2)
        lens = LensEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        lens.show()
        self.forward(2)
        self.play(
            DataUpdater(
                lens,
                lambda item, p: item.apply_uniforms_set(
                    lens_radius=0.5 + 0.3 * p.alpha,
                    lens_strength=0.5 + 1.5 * p.alpha,
                    aspect_ratio=1.77,
                ),
            ),
            duration=4.0,
            rate_func=smooth
        )

class ShaderTransformTest(Timeline):
    """
    uv run janim run test_scene.py ShaderTransformTest -i
    """
    def construct(self):
        rect1 = Rect(2, 3).stroke.set(color=RED).r
        rect2 = Rect(3, 2).stroke.set(color=BLUE).r
        LensEffect(rect1).show()
        LensEffect(rect2).show()
        self.play(Create(rect1))
        self.forward(1)
        self.play(Transform(rect1, rect2))
        self.forward(1)

class IdentityEffectTest(Timeline):
    """
    uv run janim run test_scene.py IdentityEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2)
        identity = IdentityEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        identity.show()
        self.forward(4)

class InfinityTapeItemTest(Timeline):
    """
    uv run janim run test_scene.py InfinityTapeItemTest -i
    """
    def construct(self):
        tape = InfiniteTape[str](empty_value="", initial_window_size=11)
        tape.write_batch_absolute(start_abs_index=-2, data=["A", "B", "C_0", "D_1", "E", "F", "G"])
        tape.move_pointer(1)
        tape_item = InfinityTapeItem(
            showcase_radius=5,
            tape_center_at=DOWN * 1,
            init_tape=tape,
            cell_setting=lambda index, value: TapeCell(
                square_size=0.8,
                tile_data=value,
                line_color=WHITE,
                text_scaling=1.0,
                index=index,
            ),
            # vignette_setting=lambda item: AlphaVignetteEffect(
            #     item,
            #     vignette_radius=0.6,
            #     vignette_softness=0.2,
            #     vignette_intensity=2.0,
            #     aspect_ratio=16 / 9,
            # ),
            # lens_setting=lambda item: LensEffect(
            #     item,
            #     lens_radius=1.2,
            #     lens_strength=0.5,
            #     aspect_ratio=16 / 9,
            # ),
        )
        self.play(Create(tape_item))
        self.forward(1)
        self.play(
            tape_item.set_value("D_2"),
        )
        self.play(
            tape_item.set_value("D_3"),
        )
        self.play(
            tape_item.set_value("D_4"),
        )

        for _ in range(5):
            self.forward(1)
            self.play(
                tape_item.tape_shift_right(duration=1.0),
            )
        
        for _ in range(5):
            self.forward(1)
            self.play(
                tape_item.tape_shift_left(duration=1.0),
            )

class GridCellTest(Timeline):
    """
    uv run janim run test_scene.py GridCellTest -i
    """
    def construct(self):
        cell1 = GridCell(state_name="<c BLUE>B</c>", write_bit=0, move_dir="RIGHT", is_active=True)
        cell2 = GridCell(state_name="<c YELLOW>C</c>", write_bit=1, move_dir="LEFT", is_active=False)
        cell3 = GridCell(state_name="<c RED>HALT</c>", write_bit=1, move_dir="STOP", is_active=False)
        
        group = Group(cell1, cell2, cell3)
        group.points.arrange(RIGHT, buff=0.5)
        
        self.play(Create(group))
        self.forward()
        
        self.play(
            cell1.animate_active(False),
            cell2.animate_active(True),
        )
        self.forward()

class GridTableTest(Timeline):
    """
    uv run janim run test_scene.py GridTableTest -i
    """
    def construct(self):
        states = ["A", "B", "HALT"]
        symbols = ["0", "1"]
        transitions = {
            ("A", "0"): Transition(next_state="B", write_symbol="1", direction="R"),
            ("A", "1"): Transition(next_state="A", write_symbol="1", direction="L"),
            ("B", "0"): Transition(next_state="A", write_symbol="1", direction="L"),
            ("B", "1"): Transition(next_state="HALT", write_symbol="1", direction="S"),
        }
        
        table = GridTable(states, symbols, transitions)
        self.play(Create(table))
        self.forward()
        
        # Highlight cell (A, 0)
        cell = table["A", "0"]
        self.play(cell.animate_active(True))
        self.forward()

class TuringCounterTest(Timeline):
    """
    uv run janim run test_scene.py TuringCounterTest -i
    """
    def construct(self):
        counter = TuringCounter(num_digits=4, max_value=10)
        self.play(Create(counter))
        self.forward()
        
        for i in range(1, 12):
            self.play(counter.anim_set_value(i, duration=0.5))
            self.forward(0.1)

class TuringMachineTest(Timeline):
    """
    uv run janim run test_scene.py TuringMachineTest -i
    """
    def construct(self):
        from typst_dfa.typst_dfa import load_dfa_typst
        
        core = TuringMachineCore(
            initial_tape="00000",
            start_state="A",
            blank_symbol="0",
            halt_states=["HALT"]
        )
        
        core.add_rule("A", "0", "B", "1", "R")
        core.add_rule("A", "1", "B", "1", "L")
        core.add_rule("B", "0", "A", "1", "L")
        core.add_rule("B", "1", "HALT", "1", "R")

        dfa_graph = load_dfa_typst("busy_2_1")
        for item in dfa_graph.dfa_main_item.walk_descendants(): # type: ignore
            item: VItem
            item.glow.set(color=WHITE)
        dfa_graph.dfa_main_item.points.move_to(RIGHT * 4 + DOWN * 1).scale(0.7)
        
        self.forward(1)
        
        tm = TuringMachine(
            core, 
            showcase_radius=12,
            table_scaling=0.9,
            tape_config={"center_scaling": 1.0},
            table_config={"transpose": True},
            counter_config={"max_value": 6},
        )
        
        self.play(FadeIn(tm.tape_item))
        self.play(tm.show_counter_anim(), tm.show_table_anim(), FadeIn(dfa_graph.dfa_main_item))
        self.forward()
        
        for _ in range(6):
            tm.step(duration=0.75).run_step_anim(self)
            self.forward(1)
            
        self.forward(1)
        self.play(tm.hide_counter_anim(), tm.hide_table_anim(), FadeOut(dfa_graph.dfa_main_item))
        self.forward(1)

class TuringMachineTransformTest(Timeline):
    """
    uv run janim run test_scene.py TuringMachineTransformTest -i
    """
    def construct(self):
        transform = TuringMachineTransform()
        self.play(FadeIn(transform))
        self.forward()
        
        self.play(
            transform.anim_update_info(
                state_from="A",
                state_to="B",
                read_symbol="0",
                write_symbol="1",
                direction="R"
            )
        )
        self.forward()
        
        self.play(
            transform.anim_update_info(
                state_from="B",
                state_to="HALT",
                read_symbol="1",
                write_symbol="0",
                direction="L"
            )
        )
        self.forward()


class TypDFATest(Timeline):
    """
    uv run janim run test_scene.py TypDFATest -i
    """
    def construct(self):
        from typst_dfa.typst_dfa import load_dfa_typst

        dfa = load_dfa_typst("test")
        self.play(Create(dfa.dfa_main_item))
        self.forward(1)

        self.play(*[
            DataUpdater(
                dfa.dfa_main_item[i],
                lambda item, p: item.glow.set(alpha=p.alpha)
            ) for i in dfa.circle_item["start"]
        ])
        self.forward(1)
        self.play(
            *[
                DataUpdater(
                    dfa.dfa_main_item[i],
                    lambda item, p: item.glow.set(alpha=p.alpha)
                ) for i in dfa.circle_item["stop"]
            ],
            *[
                DataUpdater(
                    dfa.dfa_main_item[i],
                    lambda item, p: item.glow.set(alpha=1 - p.alpha)
                ) for i in dfa.circle_item["start"]
            ],
        )
        self.forward(1)
        self.play(FadeOut(dfa.dfa_main_item))

        dfa2 = load_dfa_typst("busy_2_1")
        for item in dfa2.dfa_main_item.walk_descendants(None): # type: ignore
            item: VItem
            item.glow.set(color=WHITE)
        
        self.play(Create(dfa2.dfa_main_item))
        self.forward(1)
        self.play(*[
            DataUpdater(
                dfa2.dfa_main_item[i],
                lambda item, p: item.glow.set(alpha=p.alpha)
            ) for i in dfa2.circle_item["A"]
        ])
        self.forward(1)
        self.play(*[
            DataUpdater(
                dfa2.dfa_main_item[i],
                lambda item, p: item.glow.set(alpha=p.alpha)
            ) for i in dfa2.circle_item["B"]
        ])
        self.forward(1)
        self.play(*[
            DataUpdater(
                dfa2.dfa_main_item[i],
                lambda item, p: item.glow.set(alpha=p.alpha)
            ) for i in dfa2.circle_item["H"]
        ])
        self.forward(2)
        self.play(FadeOut(dfa2.dfa_main_item))

        self.forward(1)
        busy_6_1 = load_dfa_typst("busy_6_1")
        self.play(FadeIn(busy_6_1.dfa_main_item))
        self.forward(4)
        self.play(FadeOut(busy_6_1.dfa_main_item))

        self.forward(1)
        busy_6_2 = load_dfa_typst("busy_6_2")
        self.play(FadeIn(busy_6_2.dfa_main_item))
        self.forward(4)
        self.play(FadeOut(busy_6_2.dfa_main_item))


from history_grid.history_grid import HistoryGrid
class HistoryGridTest(Timeline):
    """
    uv run janim run test_scene.py HistoryGridTest -i
    """
    def construct(self):
        tape_range = range(-2, 3)
        
        # Create some dummy history
        history = []
        for t in range(4):
            tape = InfiniteTape[str](empty_value="0")
            if t == 0:
                pass # all 0
            elif t == 1:
                tape.write_absolute(1, "1")
                tape.write_absolute(2, "1")
            elif t == 2:
                tape.write_absolute(0, "1")
                tape.write_absolute(1, "1")
                tape.write_absolute(2, "1")
            elif t == 3:
                tape.write_absolute(1, "1")
                tape.write_absolute(2, "1")
            history.append(tape)
            
        grid = HistoryGrid(tape_range=tape_range)
        grid.points.to_center()
        grid.show()
        
        self.forward(1)
        
        for t, tape in enumerate(history):
            self.play(grid.get_add_column_anim(tape, t))
            self.forward(0.5)
            
        self.forward(2)

class ManyCellsTest(Timeline):
    """
    uv run janim run test_scene.py ManyCellsTest -i
    """
    def construct(self):
        def get_cell_4098(n: int = 4098):
            res = []
            for _ in range(n):
                cell = TapeCell(square_size=0.075, tile_data="")
                cell.frame.apply_style(stroke_radius=0.001)
                res.append(cell)
            return res
        
        group_cells_4098 = Group(*get_cell_4098())
        group_cells_4098.points.arrange_in_grid(n_rows=33, n_cols=128, buff=0)
        cell_1 = TapeCell(square_size=0.5, tile_data="1", text_scaling=0.75)
        cell_1.depth.set(-10)
        brace_group_cells = Brace(group_cells_4098, UP, buff=0.1).points.shift(DOWN * 0.5).r
        text_4098 = TypstMath("4098 times")
        cell_1.points.next_to(text_4098["times"], RIGHT, buff=0.25)
        group_text_4098 = Group(cell_1, text_4098).points.next_to(brace_group_cells, UP, buff=0.25).r
        
        self.play(
            *[
                Write(cell) for cell in group_cells_4098
            ],
            lag_ratio=0.0002,
        )
        self.play(
            group_cells_4098.anim.points.shift(DOWN * 0.5),
            Write(brace_group_cells),
            Write(group_text_4098),
            lag_ratio=0.2,
        )
        self.forward(2)
        self.play(
            FadeOut(group_cells_4098),
            FadeOut(brace_group_cells),
            FadeOut(group_text_4098),
            lag_ratio=0.2,
        )

from langton_ant.langton_ant_grid import LangtonAntGrid
class LangtonAntGridTest(Timeline):
    """
    uv run janim run test_scene.py LangtonAntGridTest -i
    """
    def construct(self):
        grid = LangtonAntGrid(cell_size=0.1)
        grid.show()
        self.forward(0.5)

        self.play(grid.get_step_anim())
        assert grid.core.get_steps() == 1
        self.forward(0.3)

        self.play(grid.get_multi_step_anim(5))
        assert grid.core.get_steps() == 6
        self.forward(0.3)

        grid2 = LangtonAntGrid(cell_size=0.1, pre_alloc=2)
        grid2.points.shift(RIGHT * 3)
        grid2.show()
        for _ in range(20):
            self.play(grid2.get_step_anim(duration=0.05))
        assert len(grid2.cells) > 4

        self.forward(1)