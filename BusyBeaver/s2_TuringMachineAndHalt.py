from janim.imports import * # type: ignore
from tools import get_typ_doc, local_font
from turing_machine.components.grid_cell import GridCell
from turing_machine.components.grid_table import GridTable
from turing_machine.components.paper_tile import InfinityTapeItem
from turing_machine.components.tape_cell import TapeCell
from turing_machine.components.turing_counter import TuringCounter
from turing_machine.components.turing_machine_transform import TuringMachineTransform
from turing_machine.effects.alpha_vignette import AlphaVignetteEffect
from turing_machine.effects.identity import IdentityEffect
from turing_machine.effects.lens import LensEffect
from turing_machine.logic.tapecore import InfiniteTape
from turing_machine.logic.turingcore import Transition
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.turing_machine import TuringMachine
from typst_dfa.typst_dfa import load_dfa_typst

class s2_1(Timeline):
    """
    uv run janim run s2_TuringMachineAndHalt.py s2_1 -i
    """
    def construct(self) -> None:
        text_turing_machine = Text("图灵机", font=local_font).points.scale(1.5).r
        text_turing_machine_en = Text("Turing Machine", font=local_font).points.scale(0.75).r
        text_turing_machine.points.to_border(UP).shift(UP * 0.05)
        text_turing_machine_en.points.next_to(text_turing_machine, DOWN, buff=0.1)
        text_turing_machine.astype(VItem).fill.set(color=RED_C)
        text_turing_machine_en.astype(VItem).fill.set(color=RED_A)
       
        core = TuringMachineCore(
            initial_tape="00000",
            start_state="A",
            blank_symbol="0",
            halt_states=["H"]
        )
        core.add_rule("A", "0", "B", "1", "R")
        core.add_rule("A", "1", "A", "1", "R")
        core.add_rule("B", "0", "C", "1", "R")
        core.add_rule("B", "1", "H", "1", "R")
        core.add_rule("C", "0", "A", "1", "L")
        core.add_rule("C", "1", "B", "0", "L")
        tm = TuringMachine(
            core, 
            showcase_radius=50,
            table_scaling=0.9,
            tape_config={"center_scaling": 1.0},
            table_config={"transpose": True},
            counter_config={"max_value": 15},
        )
        image_turing = ImageItem("resources/turing.jpg").points.shift(RIGHT * 4.5 + UP * 1).scale(0.75).r
        surrounding_rect_tape = SurroundingRect(tm.tape_item.cells_group, buff=0.2, depth=-20).points.shift(DOWN * 0.2).r
        surrounding_rect_tape.color.set(color=GREEN_A)
        surrounding_rect_tape.glow.set(color=GREEN_A, alpha=0.5)
        surrounding_group_tape = Group(
            surrounding_rect_tape,
            Rect(10, 10, depth=-10).points.next_to(surrounding_rect_tape, UP, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Rect(10, 10, depth=-10).points.next_to(surrounding_rect_tape, DOWN, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Text("纸带", font=local_font, depth=-20).points.scale(1.75) \
                                                .next_to(surrounding_rect_tape, UP, buff=0.2) \
                                                .shift(LEFT * 4).r \
                                                .fill.set(color=GREEN_A).r
        )
        surrounding_group_tape_cpy = surrounding_group_tape.copy()
        surround_rect_heading = SurroundingRect(tm.tape_item.pointer, buff=0.4, depth=-20).points.shift(DOWN * 0.1).r
        surround_rect_heading.color.set(color="#FFDDCF")
        surround_rect_heading.glow.set(color="#FFDDCF", alpha=0.5)
        surrounding_group_heading = Group(
            surround_rect_heading,
            Rect(20, 20, depth=-10).points.next_to(surround_rect_heading, UP, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, 20, depth=-10).points.next_to(surround_rect_heading, DOWN, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, surround_rect_heading.points.box.height, depth=-10) \
                        .points.next_to(surround_rect_heading, LEFT, buff=0).r \
                        .stroke.set(alpha=0).r \
                        .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, surround_rect_heading.points.box.height, depth=-10) \
                        .points.next_to(surround_rect_heading, RIGHT, buff=0).r \
                        .stroke.set(alpha=0).r \
                        .fill.set(color=BLACK, alpha=0.6).r,
            Text("读写头", font=local_font, depth=-20).points.scale(1.75) \
                                                .next_to(surround_rect_heading, UP, buff=0.2) \
                                                .shift(LEFT * 2.5).r \
                                                .fill.set(color="#FFDDCF").r
        )
        surrounding_group_heading_cpy = surrounding_group_heading.copy()
        surrounding_rect_table = SurroundingRect(tm.table, buff=0.2, depth=-20)
        surrounding_rect_table.color.set(color=BLUE_A)
        surrounding_rect_table.glow.set(color=BLUE_A, alpha=0.5)
        surrounding_group_table = Group(
            surrounding_rect_table,
            Rect(20, 20, depth=-10).points.next_to(surrounding_rect_table, UP, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, 20, depth=-10).points.next_to(surrounding_rect_table, DOWN, buff=0).r \
                                   .stroke.set(alpha=0).r \
                                   .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, surrounding_rect_table.points.box.height, depth=-10) \
                        .points.next_to(surrounding_rect_table, LEFT, buff=0).r \
                        .stroke.set(alpha=0).r \
                        .fill.set(color=BLACK, alpha=0.6).r,
            Rect(20, surrounding_rect_table.points.box.height, depth=-10) \
                        .points.next_to(surrounding_rect_table, RIGHT, buff=0).r \
                        .stroke.set(alpha=0).r \
                        .fill.set(color=BLACK, alpha=0.6).r,
            Text("操作规则", font=local_font, depth=-20).points.scale(1.75) \
                                                .next_to(surrounding_rect_table, UP, buff=0.2) \
                                                .shift(LEFT * 2.5).r \
                                                .fill.set(color=BLUE_A).r
        )
        cell_0 = TapeCell(tile_data="0").points.scale(0.5).r
        cell_0_word = cell_0.word.copy()
        cell_1 = TapeCell(tile_data="1").points.scale(0.5).r
        cell_1_word = cell_1.word.copy()
        text_mark_instruction = TypstDoc(
            get_typ_doc("tape_cell_instruction"),
            vars={
                "cell0": Group(cell_0_word, cell_0),
                "cell1": Group(cell_1_word, cell_1)
            },
            depth=-30
        ).points.scale(1.75).r
        text_mark_instruction.points.move_to(RIGHT * 4.5 + DOWN * 0.5)
        text_infinity = TypstMath("oo", depth=-40).points.scale(1.5).to_border(DOWN).shift(DOWN * 0.2).r

        text_heading_instruction = TypstDoc(get_typ_doc("heading_instruction"), depth=-30).points.scale(0.5).r
        text_heading_instruction.points.move_to(RIGHT * 4.2 + DOWN * 0.5)
        text_heading_instruction.points.scale(1.5)
        group_reading_example = Group(
            TapeCell(tile_data="1", square_size=0.6, text_scaling=0.6) \
                .points.move_to(ORIGIN).r \
                .depth.set(-40).r,
            SVGItem(str(Path(__file__).parent / "turing_machine" / "svgs" / "choice_frame.svg")) \
                .points.move_to(ORIGIN).scale(0.2).r \
                .depth.set(-45).r,
        )
        group_reading_example.points.next_to(text_heading_instruction.get_label("reading"), LEFT, buff=0.65)
        temp_writing_tape_cell = TapeCell(tile_data="1", square_size=0.6, text_scaling=0.6) \
                .points.move_to(ORIGIN).r \
                .depth.set(-40).r
        group_writing_example = Group(
            temp_writing_tape_cell,
            TypstMath("0", depth=-50).points.scale(0.6).move_to(temp_writing_tape_cell.word).r,
            SVGItem(str(Path(__file__).parent / "turing_machine" / "svgs" / "choice_frame.svg")) \
                .points.move_to(ORIGIN).scale(0.2).r \
                .depth.set(-45).r,
        )
        group_writing_example.points.next_to(text_heading_instruction.get_label("writing"), LEFT, buff=0.65)
        group_changing_state_example = Group(
            SVGItem(
                file_path=str(Path(__file__).parent / "turing_machine" / "svgs" / "pointer.svg"),
                scale=0.25,
                depth=-40,
            ),
            TypstText(
                RF"#text(size: 0.8em, fill: yellow)[A]",
                depth=-45,
            ),
            TypstText(
                RF"#text(size: 0.8em, fill: yellow)[B]",
                depth=-45,
            ),
        )
        group_changing_state_example.points.next_to(text_heading_instruction.get_label("state_changing"), RIGHT, buff=0.45)
        group_changing_state_example[0].points.shift(DOWN * 0.08)
        group_moving_example = Group(
            SVGItem(
                file_path=str(Path(__file__).parent / "turing_machine" / "svgs" / "pointer.svg"),
                scale=0.2,
                depth=-40,
            ),
            TapeCell(square_size=0.3).depth.set(-40).r,
            TapeCell(square_size=0.3).depth.set(-40).r,
        )
        group_moving_example[2].points.next_to(group_moving_example[1], RIGHT, buff=0)
        group_moving_example[0].points.next_to(group_moving_example[0], UP, buff=0.05)
        group_moving_example.points.next_to(text_heading_instruction.get_label("moving"), RIGHT, buff=0.35)

        self.play(FadeIn(tm.tape_item))
        self.play(tm.show_counter_anim(), tm.show_table_anim())
        self.forward()
        self.play(Write(text_turing_machine), Write(text_turing_machine_en))
        
        example_recurrence_times = 6
        example_reading_anim = Succession(
            FadeIn(group_reading_example),
            *[
                Succession(
                    FadeOut(group_reading_example[1], duration=0.5),
                    Wait(0.5),
                    FadeIn(group_reading_example[1], duration=0.5),
                    Wait(0.5)
                ) for _ in range(example_recurrence_times)
            ],
            FadeOut(group_reading_example),
        )
        example_writing_anim = Succession(
            AnimGroup(
                FadeIn(group_writing_example[0]),
                FadeIn(group_writing_example[2]),
            ),
            *[
                Succession(
                    AnimGroup(
                        FadeOut(group_writing_example[0].word, duration=0.5),
                        FadeIn(group_writing_example[1], duration=0.5),
                    ),
                    Wait(0.5),
                    AnimGroup(
                        FadeOut(group_writing_example[1], duration=0.5),
                        FadeIn(group_writing_example[0].word, duration=0.5),
                    ),
                    Wait(0.5)
                ) for _ in range(example_recurrence_times)
            ],
            FadeOut(group_writing_example),
        )
        example_changing_state_anim = Succession(
            AnimGroup(
                FadeIn(group_changing_state_example[0]),
                FadeIn(group_changing_state_example[1]),
            ),
            *[
                Succession(
                    AnimGroup(
                        FadeOut(group_changing_state_example[1], duration=0.5),
                        FadeIn(group_changing_state_example[2], duration=0.5),
                    ),
                    Wait(0.5),
                    AnimGroup(
                        FadeOut(group_changing_state_example[2], duration=0.5),
                        FadeIn(group_changing_state_example[1], duration=0.5),
                    ),
                    Wait(0.5)
                ) for _ in range(example_recurrence_times)
            ],
            FadeOut(group_changing_state_example),
        )
        distance_of_2_little_cell = group_moving_example[2].points.box.get_x() - group_moving_example[1].points.box.get_x()
        example_moving_anim = Succession(
            FadeIn(group_moving_example),
            *[
                Succession(
                    AnimGroup(group_moving_example[0].anim.points.shift(RIGHT * distance_of_2_little_cell), duration=0.5),
                    Wait(0.5),
                    AnimGroup(group_moving_example[0].anim.points.shift(LEFT * distance_of_2_little_cell), duration=0.5),
                    Wait(0.5),
                ) for _ in range(example_recurrence_times)
            ],
            FadeOut(group_moving_example),
        )
        
        grid_new = tm.table.copy()
        grid_new.points.shift(UP * 1)
        grid_new.depth.set(-50)
        rec_grid_row1 = SurroundingRect(
            Group(
                grid_new[("A", "0")],
                grid_new[("H", "0")],
            ),
            depth=-60,
        ).points.shift(UP * 1).r
        rec_grid_row2 = SurroundingRect(
            Group(
                grid_new[("A", "1")],
                grid_new[("H", "1")],
            ),
            depth=-60,
        ).points.shift(UP * 1).r

        for i in range(15):
            match i:
                case 1:
                    tm.step(duration=0.75).run_step_anim(self)
                    self.play(FadeIn(image_turing))
                case 2:
                    def case2ops(idx):
                        if idx == 2: self.prepare(FadeOut(image_turing))
                        if idx == 4: self.prepare(FadeIn(surrounding_group_tape))
                    tm.step(duration=0.75).run_step_anim(self, case2ops)
                case 3:
                    def case3ops(idx):
                        if idx == 2: self.prepare(
                            FadeOut(Group(*surrounding_group_tape[1:-2])),
                            TransformMatchingDiff(surrounding_group_tape[-1], surrounding_group_heading[-1]),
                            Transform(surrounding_group_tape[0], surrounding_group_heading[0]),
                            FadeIn(Group(*surrounding_group_heading[1:-2])),
                            lag_ratio=0.2,
                        )
                    tm.step(duration=0.75).run_step_anim(self, case3ops)
                case 4:
                    self.prepare(
                        FadeOut(Group(*surrounding_group_heading[1:-2])),
                        TransformMatchingDiff(surrounding_group_heading[-1], surrounding_group_table[-1]),
                        Transform(surrounding_group_heading[0], surrounding_group_table[0]),
                        FadeIn(Group(*surrounding_group_table[1:-2])),
                        lag_ratio=0.2,
                    )
                    def case4ops(idx):
                        if idx == 4: self.prepare(
                            FadeOut(Group(*surrounding_group_table[1:-2])),
                            TransformMatchingDiff(surrounding_group_table[-1], surrounding_group_tape_cpy[-1]),
                            Transform(surrounding_group_table[0], surrounding_group_tape_cpy[0]),
                            FadeIn(Group(*surrounding_group_tape_cpy[1:-2])),
                            lag_ratio=0.2,
                        )
                    tm.step(duration=0.75).run_step_anim(self, case4ops)
                case 5:
                    def case5ops(idx):
                        if idx == 1: self.prepare(
                            Write(text_mark_instruction),
                        )
                    tm.step(duration=0.75).run_step_anim(self, case5ops)
                    self.play(
                        Succession(
                            FadeIn(text_infinity),
                            AnimGroup(
                                tm.tape_item.cells_group.anim.points.shift(LEFT * 20),
                                tm.framebox.anim.points.shift(LEFT * 20),
                                rate_func=ease_inout_cubic,
                                duration=4.0,
                            ),
                            AnimGroup(
                                tm.tape_item.cells_group.anim.points.shift(RIGHT * 20),
                                tm.framebox.anim.points.shift(RIGHT * 20),
                                rate_func=ease_inout_cubic,
                                duration=4.0,
                            ),
                            FadeOut(text_infinity),
                        )
                    )
                case 6:
                    def case6ops(idx):
                        if idx == 1: self.prepare(
                            FadeOut(text_mark_instruction),
                        )
                        if idx == 2: self.prepare(
                            FadeOut(Group(*surrounding_group_tape_cpy[1:-2])),
                            TransformMatchingDiff(surrounding_group_tape_cpy[-1], surrounding_group_heading_cpy[-1]),
                            Transform(surrounding_group_tape_cpy[0], surrounding_group_heading_cpy[0]),
                            FadeIn(Group(*surrounding_group_heading_cpy[1:-2])),
                            lag_ratio=0.2,
                        )
                        if idx == 3: self.prepare(
                            Write(text_heading_instruction),
                        )
                        if idx == 4: self.prepare(
                            AnimGroup(example_reading_anim, at=1.0),
                            AnimGroup(example_writing_anim, at=2.5),
                            AnimGroup(example_changing_state_anim, at=4.0),
                            AnimGroup(example_moving_anim, at=5.5)
                        )
                    tm.step(duration=0.75).run_step_anim(self, case6ops)
                case 11:
                    self.prepare(
                        FadeOut(surrounding_group_heading_cpy[-1]),
                        text_heading_instruction.anim.points.shift(DOWN * 0.5),
                        *[
                            rect.anim.fill.set(alpha=1.0)
                            for rect in surrounding_group_heading_cpy[1:-2]
                        ],
                        surrounding_group_heading_cpy[1].anim.points.shift(DOWN * 0.2),
                        FadeIn(grid_new),
                        self.camera.anim.points.shift(UP * 1).scale(0.9),
                    )
                    def case11ops(idx):
                        if idx == 1: self.prepare(
                            Write(rec_grid_row1),
                        )
                        if idx == 3: self.prepare(
                            Transform(rec_grid_row1, rec_grid_row2),
                        )
                    tm.step(duration=0.5).run_step_anim(self, case11ops)
                    self.prepare(
                        Succession(
                            Wait(1.5),
                            AnimGroup(
                                FadeOut(grid_new),
                                FadeOut(rec_grid_row2),
                                FadeOut(surrounding_group_heading_cpy[0:-2]),
                                FadeOut(text_heading_instruction),
                                self.camera.anim.points.shift(DOWN * 1).scale(10 / 9),
                            )
                        )
                    )
                case _:
                    tm.step(duration=0.5).run_step_anim(self)
            
            self.forward(1)

        text_halt = TypstText("HALT").points.scale(1).move_to(tm.tape_item.pointer_text).r
        text_halt.astype(VItem).fill.set(color=RED_B)
        self.play(
            tm.table[("A", "1")].animate_active(False),
            tm.table[("H", "0")].animate_active(True),
            tm.table[("H", "1")].animate_active(True),
            TransformMatchingDiff(tm.tape_item.pointer_text, text_halt)
        )
        self.forward(1.5)
        self.play(
            FadeOut(tm.table),
            FadeOut(tm.counter),
            FadeOut(tm.tape_item.cells_group),
            FadeOut(tm.tape_item.pointer),
            FadeOut(tm.framebox),
            FadeOut(text_halt),
            FadeOut(text_turing_machine),
            FadeOut(text_turing_machine_en),
        )
        self.forward(1)

class s2_2(Timeline):
    """
    uv run janim run s2_TuringMachineAndHalt.py s2_2 -i
    """
    def construct(self) -> None:
        pass
    