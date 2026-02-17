from janim.imports import * # type: ignore
from typing import cast
from tools import get_typ_doc, local_font, CYAN, parse_rule_to_core, get_perceptual_gradient_function
from turing_machine.components.tape_cell import TapeCell
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.turing_machine import TuringMachine
from typst_dfa.typst_dfa import load_dfa_typst
import random

class s3_1(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_1 -i
    """
    def construct(self) -> None:
        frame_width = cast(float, Config.get.frame_width)
        frame_height = cast(float, Config.get.frame_height)

        class TMLoop(Timeline):
            def construct(self) -> None:
                self.camera.points.scale(1.2)
                core_loop = TuringMachineCore(
                    initial_tape=["0"],
                    start_state="A",
                    halt_states=["HALT"]
                )
                core_loop.add_rule("A", "0", "B", "0", "R")
                core_loop.add_rule("A", "1", "HALT", "1", "S")
                core_loop.add_rule("B", "0", "C", "1", "L")
                core_loop.add_rule("B", "1", "A", "0", "L")
                core_loop.add_rule("C", "0", "D", "0", "R")
                core_loop.add_rule("C", "1", "HALT", "1", "S")
                core_loop.add_rule("D", "0", "HALT", "0", "S")
                core_loop.add_rule("D", "1", "E", "1", "L")
                core_loop.add_rule("E", "0", "B", "0", "R")
                core_loop.add_rule("E", "1", "HALT", "1", "S")
                tm_loop = TuringMachine(
                    turing_core=core_loop,
                    showcase_radius=9,
                    table_scaling=0.75,
                    tape_config={"center_scaling": 1},
                    table_config={"transpose": True},
                    counter_config={"max_value": 9999},
                )
                tm_loop.is_table_shown = True
                tm_loop.is_counter_shown = False
                tm_loop.points.shift(DOWN * 1.5)
                tm_loop.table.points.shift(RIGHT * 0.25)
                dfa_tm_loop = load_dfa_typst("loop_5_1").dfa_main_item
                dfa_tm_loop.points.scale(0.75).next_to(tm_loop.table, UP, buff=0.1)

                self.play(
                    Write(tm_loop.tape_item),
                    Write(tm_loop.table),
                    Write(tm_loop.framebox),
                )
                self.play(Write(dfa_tm_loop))
                self.forward(4)

                # text_trans_method = TypstDoc(Path("typ_docs/loop_5_1_trans.typ").read_text())
                # text_trans_method.points.scale(0.7).next_to(dfa_tm_loop, RIGHT, buff=1).shift(LEFT * 2.5)
                hl_rect_state = Rect(1, 1)
                hl_rect_state.color.set(color=YELLOW, alpha=0)

                self.prepare(
                    hl_rect_state.anim.stroke.set(alpha=1),
                    at=2
                )

                for i in range(500):
                    cur_tag = ["A", "B", "C", "D", "E", "B"][(i + 1) % 6]
                    if i >= 100 and (i + 1) % 6 == 0:
                        self.forward(0.5)
                    tm_loop.step(duration=0.01).run_step_anim(self, compress=True)
                    hl_rect_state.points.move_to(dfa_tm_loop.get_label(cur_tag).points.box.center)

        class TMBB5(Timeline):
            def construct(self) -> None:
                self.camera.points.scale(1.2)
                core_bb5 = TuringMachineCore(
                    initial_tape=["0"],
                    start_state="A",
                    halt_states=["HALT"]
                )
                core_bb5.add_rule("A", "0", "B", "1", "R")
                core_bb5.add_rule("A", "1", "C", "1", "L")
                core_bb5.add_rule("B", "0", "C", "1", "R")
                core_bb5.add_rule("B", "1", "B", "1", "R")
                core_bb5.add_rule("C", "0", "D", "1", "R")
                core_bb5.add_rule("C", "1", "E", "0", "L")
                core_bb5.add_rule("D", "0", "A", "1", "L")
                core_bb5.add_rule("D", "1", "D", "1", "L")
                core_bb5.add_rule("E", "0", "HALT", "1", "R")
                core_bb5.add_rule("E", "1", "A", "0", "L")
                tm_bb5 = TuringMachine(
                    turing_core=core_bb5,
                    showcase_radius=9,
                    table_scaling=0.75,
                    tape_config={"center_scaling": 1},
                    table_config={"transpose": True},
                    counter_config={"max_value": 9999},
                )
                tm_bb5.is_table_shown = True
                tm_bb5.is_counter_shown = False
                tm_bb5.points.shift(DOWN * 1.5)
                dfa_tm_bb5 = load_dfa_typst("busy_5_1").dfa_main_item
                dfa_tm_bb5.points.scale(0.75).next_to(tm_bb5.table, UP, buff=0.1)

                self.play(
                    Write(tm_bb5.tape_item),
                    Write(tm_bb5.table),
                    Write(tm_bb5.framebox),
                    Write(dfa_tm_bb5),
                )
                self.forward(15)

                text_busybeaver = Text("忙碌海狸机", font=local_font, depth=-10)
                text_busybeaver.color.set(color=LIGHT_PINK).r \
                               .points.scale(2).next_to(tm_bb5.table, RIGHT, buff=1).shift(UP * 1)
                text_busybeaver_en = Text("Busy Beaver", font=local_font, depth=-10)
                text_busybeaver_en.color.set(color=CYAN).r \
                                  .points.next_to(text_busybeaver, DOWN, buff=0.1, aligned_edge=LEFT)

                self.prepare(
                    Succession(
                        Write(text_busybeaver),
                        Write(text_busybeaver_en),
                    ),
                    at=15
                )

                for i in range(800):
                    tm_bb5.step(duration=0.01).run_step_anim(self, compress=True)
        
        subtimeline_loop = TMLoop().build().to_item().show()
        clip_loop = TransformableFrameClip(
            subtimeline_loop,
            clip=(0, 0, 0, 0),
            offset=(0, 0),
        )
        
        self.play(FadeIn(clip_loop))
        self.forward(3)

        subtimeline_bb5 = TMBB5().build().to_item().show()
        clip_bb5 = TransformableFrameClip(
            subtimeline_bb5,
            clip=(1 / 3, 0, 1 / 3, 0),
            offset=(1 / 3, 0),
        )
        line_seperator = DashedLine(
            frame_height / 2 * DOWN,
            frame_height / 2 * UP,
            color=WHITE,
        )
        line_seperator.points.shift(RIGHT * frame_width * 1 / 6)
        text_config = Text("配置 / 格局", font=local_font, depth=-10)
        text_config.color.set(color=GREEN_A)
        text_config_en = Text("Configuration", font=local_font, depth=-10)
        text_config_en.color.set(color=GREEN_C)
        text_config_en.points.scale(0.5).next_to(text_config, DOWN, aligned_edge=LEFT, buff=0.1)
        Group(text_config, text_config_en).points.scale(3)
        mask_rec = Rect(20, 20)
        mask_rec.color.set(color=BLACK, alpha=0.6)

        self.play(
            FadeIn(clip_bb5),
            Write(line_seperator),
            clip_loop.anim.clip.set(1 / 6, 0, 1 / 6, 0, x_offset=-1 / 6),
        )
        self.forward(10)
        self.pause_point()
        self.play(
            FadeIn(mask_rec),
            Write(text_config),
            Write(text_config_en),
            lag_ratio=0.2,
        )
        self.forward(1.5)
        self.play(
            FadeOut(mask_rec),
            FadeOut(text_config),
            FadeOut(text_config_en),
        )
        self.forward(2)
        self.play(
            clip_loop.anim.clip.set(1 / 3, 0, 1 / 3, 0, x_offset=-1 / 3),
            clip_bb5.anim.clip.set(1 / 6, 0, 1 / 6, 0, x_offset=1 / 6),
            line_seperator.anim.points.move_to(LEFT * frame_width * 1 / 6),
        )
        self.forward(3)

        dfa_bb5 = load_dfa_typst("busy_5_1").dfa_main_item
        dfa_bb5.depth.set(-10)
        dfa_bb5.points.scale(0.85).shift(UP * 1.5)
        mask_rec.color.set(alpha=0.8)
        text_step_counter = Text(
            f"<c BLUE_B><fs 2.5>0</fs></c>步",
            format="rich",
            font=local_font,
        ).points.next_to(dfa_bb5, DOWN, buff=0.5).r
        rect_hl_state = Rect(1, 1)

        def get_cell_4098(n: int = 4098):
            res = []
            for _ in range(n):
                cell = TapeCell(square_size=0.075, tile_data="")
                cell.frame.apply_style(stroke_radius=0.001)
                res.append(cell)
            return res
        
        group_cells_4098 = Group(*get_cell_4098())
        group_cells_4098.points.arrange_in_grid(n_rows=33, n_cols=128, buff=0) \
                               .next_to(text_step_counter, DOWN, buff=1)
        cell_1 = TapeCell(square_size=0.5, tile_data="1", text_scaling=0.75)
        cell_1.depth.set(-10)
        brace_group_cells = Brace(group_cells_4098, UP, buff=0.1).points.shift(DOWN * 0.5).r
        text_4098 = TypstMath("4098 times")
        cell_1.points.next_to(text_4098["times"], RIGHT, buff=0.25)
        group_text_4098 = Group(cell_1, text_4098).points.next_to(brace_group_cells, UP, buff=0.2).r

        self.play(
            FadeIn(mask_rec),
            FadeIn(dfa_bb5),
        )
        self.play(
            ItemUpdater(
                text_step_counter,
                lambda p: Text(
                    f"<c BLUE_B><fs 2.5>{int(p.alpha * 47176870)}</fs></c>步",
                    format="rich",
                    font=local_font,
                    depth=-10,
                ).points.next_to(dfa_bb5, DOWN, buff=0.5).r,
                rate_func=ease_inout_cubic,
            ),
            ItemUpdater(
                rect_hl_state,
                lambda p: Rect(1, 1) \
                    .color.set(color=YELLOW).r \
                    .points.move_to(
                        dfa_bb5.get_label(["A", "B", "C", "D", "E", "B"][random.randint(0, 5)]).points.box.center
                        if p.alpha < 0.99
                        else dfa_bb5.get_label("H").points.box.center
                    ).r,
                rate_func=smooth,
            ),
            duration=3,
        )
        self.forward(1.5)
        
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
            FadeOut(mask_rec),
            FadeOut(text_step_counter),
            FadeOut(rect_hl_state),
            FadeOut(dfa_bb5),
        )
        self.forward(1)
        self.play(
            clip_loop.anim.clip.set(1 / 2, 0, 1 / 2, 0, x_offset=-1 / 2),
            clip_bb5.anim.clip.set(0, 0, 0, 0, x_offset=0),
            line_seperator.anim.points.move_to(LEFT * frame_width * 1 / 2 + LEFT * 0.1),
        )
        clip_loop.hide()
        subtimeline_loop.hide()
        line_seperator.hide()
        self.forward(7)

        class TMDIY(Timeline):
            def __init__(
                self,
                core: TuringMachineCore,
                dfa_typst_path: str | None = None,
                steps: int = 300,
                step_count: int = 0,
                counting_color: str = "BLUE_B",
                counting_start_at: float = 1.5,
                counting_duration: float = 3,
            ):
                super().__init__()
                self.core = core
                self.dfa_typst_path = dfa_typst_path
                self.steps = steps
                self.step_count = step_count
                self.counting_color = counting_color
                self.counting_start_at = counting_start_at
                self.counting_duration = counting_duration
            
            def construct(self) -> None:
                tm_diy = TuringMachine(
                    turing_core=self.core,
                    showcase_radius=9,
                    table_scaling=0.75,
                    tape_config={"center_scaling": 1},
                    table_config={"transpose": True},
                    counter_config={"max_value": 9999},
                )
                tm_diy.is_table_shown = True
                tm_diy.is_counter_shown = False
                tm_diy.tape_item.show()
                tm_diy.table.show()
                tm_diy.framebox.show()
                
                if self.dfa_typst_path is not None:
                    dfa_tm_diy = load_dfa_typst(self.dfa_typst_path).dfa_main_item
                    dfa_tm_diy.points.scale(0.75).next_to(tm_diy.table, UP, buff=0.1)
                    dfa_tm_diy.show()

                frame_width = cast(float, Config.get.frame_width)
                frame_height = cast(float, Config.get.frame_height)
                mask_rect = Rect(
                    frame_width,
                    frame_height,
                    color=GREY_B,
                    depth=-10,
                )
                mask_rec.stroke.set(alpha=0.5)
                text_run_step_count = Text(
                    f"<c {self.counting_color}><fs 2.5>0</fs></c>步",
                    format="rich",
                    font=local_font,
                    depth=-20,
                ).points.move_to(mask_rect).r

                self.prepare(
                    Succession(
                        FadeIn(mask_rect),
                        ItemUpdater(
                            text_run_step_count,
                            lambda p: Text(
                                f"<c {self.counting_color}>"
                                f"<fs 2.5>{int(p.alpha * self.step_count)}</fs>"
                                f"</c>步",
                                format="rich",
                                font=local_font,
                                depth=-20,
                            ).points.move_to(mask_rect).scale(2.5).r,
                            rate_func=ease_inout_cubic,
                            duration=self.counting_duration,
                        ),
                    ),
                    at=self.counting_start_at,
                )

                for _ in range(self.steps):
                    tm_diy.step(duration=0.01).run_step_anim(self, compress=True)

        tm_diy_width = 3
        tm_diy_height = 3
        full_rules = Path("resources/turings_5.txt").read_text(encoding="utf-8").splitlines()
        choiced_rules = random.choices(full_rules, k=tm_diy_width * tm_diy_height)
        choiced_cores = [{
            "core": parse_rule_to_core(rule)[0],
            "step_count": parse_rule_to_core(rule)[1],
        } for rule in choiced_rules]
        DEBUG = True
        counting_color_gradient = get_perceptual_gradient_function([
            GREEN_B,
            YELLOW,
            RED_B,
        ])
        max_counting = max([core["step_count"] for core in choiced_cores])
        min_counting = min([core["step_count"] for core in choiced_cores])
        if DEBUG:
            print(f"max_counting: {max_counting}, min_counting: {min_counting}")
        if max_counting == min_counting:
            counting_gradient_func = lambda _count: "YELLOW"
        else:
            counting_gradient_func = lambda count: \
                counting_color_gradient(
                    (count - min_counting) / (max_counting - min_counting)
                )
        if DEBUG:
            [print(f"step for {i}: {info['step_count']}") for i, info in enumerate(choiced_cores)]
        tms_diy = [
            TMDIY(
                core=info["core"],
                step_count=info["step_count"],
                counting_color=str(counting_gradient_func(info["step_count"])),
                counting_start_at=random.uniform(1.5, 2.5),
                counting_duration=3,
            ).build().to_item()
            for info in choiced_cores
        ]
        def get_clip_xy(i: int):
            # 中间的移走，不阻挡原有的
            if i == tm_diy_width * tm_diy_height // 2:
                return (10, 10)

            mid_X = (tm_diy_width - 1) / 2
            mid_Y = (tm_diy_height - 1) / 2
            col = i % tm_diy_width
            row = i // tm_diy_width
            if DEBUG:
                print(f"计算坐标 ({col - mid_X}, {mid_Y - row})")
            return (col - mid_X, mid_Y - row)
        clips_diy = [
            TransformableFrameClip(
                tm_diy.show(),
                clip=(0, 0, 0, 0),
            ).clip.set(
                x_offset=get_clip_xy(i)[0],
                y_offset=get_clip_xy(i)[1],
            ).r.show()
            for i, tm_diy in enumerate(tms_diy)
        ]
        
        # 这个 frame 需要检查情况
        if DEBUG:
            for i, c in enumerate(clips_diy):
                print(f"---- clip {i} 信息:")
                for i in range(9):
                    name = (
                        "left", "top", "right",
                        "bottom", "x_offset", "y_offset",
                        "x_scale", "y_scale", "rotate"
                    )[i]
                    print(f"  {name}: {c.clip._attrs[i]}")
                print("---")

        self.play(
            clip_bb5.anim.clip.set(
                x_scale=1 / tm_diy_width,
                y_scale=1 / tm_diy_height,
                x_offset=0,
                y_offset=0,
            ),
            *[
                diyclip.anim.clip.set(
                    x_offset=1 / tm_diy_width * get_clip_xy(i)[0],
                    y_offset=1 / tm_diy_height * get_clip_xy(i)[1],
                    x_scale=1 / tm_diy_width,
                    y_scale=1 / tm_diy_height,
                )
                for i, diyclip in enumerate(clips_diy)
            ],
            rate_func=ease_inout_cubic,
        )
        self.forward(6)
        for clip in clips_diy:
            clip.hide()
        for tm in tms_diy:
            tm.hide()
        self.play(
            clip_bb5.anim.clip.set(
                x_scale=1,
                y_scale=1,
                x_offset=0,
                y_offset=0,
            ),
        )
        self.forward(10)
