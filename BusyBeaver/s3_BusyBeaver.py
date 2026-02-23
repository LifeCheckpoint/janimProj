from janim.imports import * # type: ignore
from typing import cast
from tools import (
    get_typ_doc,
    local_font,
    CYAN,
    parse_rule_to_core,
    get_perceptual_gradient_function,
    rejection_sample,
)
from turing_machine.components.tape_cell import TapeCell
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.turing_machine import TuringMachine
from turing_machine.components.grid_cell import GridCell
from langton_ant.langton_ant_grid import LangtonAntGrid
from typst_dfa.typst_dfa import load_dfa_typst
from dirty_patch import install_dirty_patch
import random

class s3_1(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_1 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        frame_width = cast(float, Config.get.frame_width)
        frame_height = cast(float, Config.get.frame_height)

        class TMLoop(Timeline):
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
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
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
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
        self.forward(3)

        class TMDIY(Timeline):
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
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
                self.camera.points.scale(0.9)
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
                    color=BLACK,
                    depth=-10,
                )
                mask_rect.stroke.set(alpha=0.5)
                mask_rect.fill.set(alpha=0.9)
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
                        Wait(1.5),
                        AnimGroup(
                            FadeOut(text_run_step_count),
                            mask_rect.anim.color.set(alpha=1),
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
        DEBUG = False
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
        self.forward(8)
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
        self.forward(1)

        svg_branch = SVGItem("resources/branch.svg").points.shift(DOWN * 6).r
        svg_beaver_dam = SVGItem("resources/beaver_dam.svg").points.shift(DOWN * 6).r
        
        self.play(
            self.camera.anim.points.shift(DOWN * 6),
            clip_bb5.anim.clip.set(y_offset=1),
            Write(svg_branch),
        )
        self.forward(0.5)
        self.play(
            FadeOut(svg_branch),
            Write(svg_beaver_dam),
        )
        self.forward(2)
        self.play(
            FadeOut(svg_beaver_dam),
            clip_bb5.anim.clip.set(y_offset=0),
            self.camera.anim.points.shift(UP * 6),
        )
        self.forward(2)

class s3_2(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_2 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        text_state_5_steps = TypstText(
            "$overbrace(A quad B quad C quad D quad E, \"5 状态\") quad arrow.r quad$ #text(fill: aqua)[47176870] 步",
        ).points.scale(1.7).move_to(UP * 1.5).r
        text_max_step = TypstDoc(get_typ_doc("why_max_step"))
        text_max_step.points.scale(0.85).next_to(text_state_5_steps, DOWN, buff=0.5)
        text_status_step = Text(
            "<c RED_B>状态</c>，与膨胀的<c BLUE_B>步数</c>",
            format="rich",
            font=local_font,
            depth=-10,
        )
        text_status_step.points.scale(1.5).move_to(UP * 3 + LEFT * 4)
        text_status_step_2 = Text(
            "<c RED_B>状态</c><c GREY_D>，与膨胀的</c><c BLUE_B>步数</c>",
            format="rich",
            font=local_font,
            depth=-10,
        )
        text_status_step_2.points.scale(1.5).move_to(UP * 3 + LEFT * 4)
        text_status_step_3 = text_status_step.copy()

        self.forward(1)
        self.play(Write(text_state_5_steps))
        self.forward(1.5)
        self.play(Write(text_max_step))
        self.forward(2)
        self.play(
            FadeOut(text_max_step),
            TransformMatchingShapes(text_state_5_steps, text_status_step),
        )
        self.forward(1)
        core_bb5 = TuringMachineCore(
            initial_tape="".join([random.choice("01") for _ in range(20)]),
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
        for _ in range(10):
            core_bb5.step()
        tm_bb5 = TuringMachine(
            turing_core=core_bb5,
            showcase_radius=10,
            table_scaling=1.1,
            tape_config={"center_scaling": 1},
            table_config={"transpose": True},
            counter_config={"max_value": 9999},
        )
        tm_bb5.is_table_shown = True
        tm_bb5.is_counter_shown = False
        tm_bb5.points.shift(DOWN * 0.75)
        text_10x2eq20 = TypstMath("10 times 2 = 20")
        text_10x2eq20.points.scale(2).next_to(tm_bb5.table, DOWN, buff=0.5)

        self.play(Write(tm_bb5.table))
        self.forward(0.5)
        self.play(Write(text_10x2eq20))
        self.forward(1.5)
        self.play(FadeOut(text_10x2eq20))
        self.play(
            Write(tm_bb5.tape_item),
            Write(tm_bb5.framebox),
        )
        self.forward(1.5)
        self.play(
            FadeOut(tm_bb5.tape_item),
            FadeOut(tm_bb5.framebox),
            FadeOut(tm_bb5.table),
        )

        rect_bl1 = Rect(1, 1)
        rect_bl1.fill.set(color=BLACK, alpha=1).r.stroke.set(color=WHITE, alpha=1)
        rect_bl2 = rect_bl1.copy()
        rect_bl2.points.shift(RIGHT)
        rect_wh1 = Rect(1, 1)
        rect_wh1.fill.set(color=WHITE, alpha=1).r.stroke.set(color=BLACK, alpha=1)
        rect_wh2 = rect_wh1.copy()
        rect_wh2.points.shift(RIGHT)
        triangle_ant = Triangle(depth=-10).points.scale(0.3).r
        triangle_ant.points.move_to(rect_bl1)
        triangle_ant2 = Triangle(depth=-10).points.scale(0.3).r
        triangle_ant2.stroke.set(color=BLACK, alpha=1)
        triangle_ant2.points.move_to(rect_bl2)
        
        self.play(
            Write(rect_bl1),
            Write(triangle_ant),
            lag_ratio=0.2,
            duration=0.5,
        )
        self.forward(0.5)
        self.play(
            Succession(
                Rotate(triangle_ant, PI / 2),
                triangle_ant.anim.points.shift(LEFT),
            ),
            TransformMatchingShapes(rect_bl1, rect_wh1),
            lag_ratio=0.25,
            duration=0.5,
        )
        self.forward(0.5)
        self.play(
            rect_wh1.anim.points.shift(LEFT),
            triangle_ant.anim.points.shift(LEFT),
            Write(rect_wh2),
            Write(triangle_ant2),
            duration=0.5,
        )
        self.forward(0.5)
        self.play(
            Succession(
                Rotate(triangle_ant2, -PI / 2),
                AnimGroup(
                    triangle_ant2.anim.points.shift(RIGHT),
                    triangle_ant2.anim.stroke.set(color=WHITE, alpha=1),
                )
            ),
            TransformMatchingShapes(rect_wh2, rect_bl2),
            lag_ratio=0.25,
            duration=0.5,
        )
        self.forward(1)
        self.play(
            FadeOut(triangle_ant),
            FadeOut(triangle_ant2),
        )

        grid = LangtonAntGrid(cell_size=0.25, pre_alloc=150)

        self.play(
            TransformMatchingShapes(
                Group(rect_wh1, rect_bl2),
                grid,
            ),
            TransformMatchingShapes(text_status_step, text_status_step_2),
        )
        self.forward(1)
        self.play(
            AnimGroup(
                grid.get_multi_step_anim(1000, duration=0.0003),
                rate_func=ease_inout_cubic,
                collapse=True,
            ),
            text_status_step_2.anim.points.shift(UP * 1.5 + LEFT * 1.5).scale(1.5),
            self.camera.anim.points.scale(1.5),
        )
        fast_ant_anim = Succession(
            *[
                grid.multi_step(120, duration=0.02)
                for _ in range(100)
            ],
            collapse=True,
        )
        self.play(fast_ant_anim)
        self.forward(1)
        self.prepare(
            AnimGroup(
                *[
                    AnimGroup(
                        FadeOut(cell),
                        at=random.uniform(0, 1.5),
                    )
                    for cell in grid.cells.values()
                ],
                collapse=True,
            ),
        )
        self.play(
            self.camera.anim.points.scale(2 / 3),
            TransformMatchingShapes(text_status_step_2, text_status_step_3),
            duration=2,
        )
        self.forward(1)

class s3_3(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_3 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        text_status_step = Text(
            "<c RED_B>状态</c>，与膨胀的<c BLUE_B>步数</c>",
            format="rich",
            font=local_font,
            depth=-10,
        )
        text_status_step.points.scale(1.5).move_to(UP * 3 + LEFT * 4)
        text_max_step = TypstDoc(get_typ_doc("why_max_step"))
        text_max_step.points.scale(0.85).next_to(text_status_step, DOWN, aligned_edge=LEFT, buff=0.5)

        text_status_step.show()
        self.forward(0.5)
        self.play(TransformMatchingDiff(text_status_step, text_max_step))
        self.forward(2)
        self.play(FadeOut(text_max_step))

        full_rules = Path("resources/turings_5.txt").read_text(encoding="utf-8").splitlines()
        k_tms = 20
        choiced_rules = random.choices(full_rules, k=k_tms)
        choiced_cores = [{
            "core": parse_rule_to_core(rule)[0],
            "step_count": parse_rule_to_core(rule)[1],
        } for rule in choiced_rules]
        tms = [
            TuringMachine(
                turing_core=info["core"],
                showcase_radius=15,
                table_scaling=1.0,
                tape_config={"center_scaling": 1},
                table_config={"transpose": True},
                counter_config={"max_value": 9999},
            ) for info in choiced_cores
        ]
        text_set_tms = TypstMath("{" + ", ".join([f"H_{i + 1}" for i in range(k_tms)]) + ", ...}")
        text_set_tms.points.scale(0.9).move_to(DOWN * 3.25)
        rect_set_tms = [
            SurroundingRect(text_set_tms[f"H_{i + 1}"])
            for i in range(k_tms)
        ]

        self.play(Write(text_set_tms))
        self.play(
            Write(rect_set_tms[0]),
            Write(tms[0].table),
            Write(tms[0].framebox),
            Write(tms[0].tape_item),
        )
        self.forward(0.5)
        slow_anim_tms_count = 5
        def _update_tms(i: int):
            tms[i - 1].hide()
            tms[i].table.show()
            tms[i].framebox.show()
            tms[i].tape_item.show()    
        for i in range(1, k_tms):
            if i < slow_anim_tms_count:
                dur_tms = 0.25
            else:
                dur_tms = 0.05
            self.play(
                AnimGroup(
                    TransformMatchingShapes(rect_set_tms[i - 1], rect_set_tms[i]),
                    Wait(dur_tms / 2),
                    Do(lambda: _update_tms(i)),
                ),
                duration=dur_tms,
            )
        self.play(FadeOut(rect_set_tms[-1]))
        self.forward(1.5)
        focus_table = tms[-1].table
        self.play(
            FadeOut(text_set_tms),
            FadeOut(tms[-1].framebox),
            FadeOut(tms[-1].tape_item),
            focus_table.anim.points.move_to(ORIGIN).scale(1.2),
            lag_ratio=0.2,
        )
        self.forward(1)

        brace_n = Brace(focus_table, UP, buff=0.1)
        brace_n_text = TypstMath("n").points.scale(1.75).next_to(brace_n, UP, buff=0.2).r
        brace_2 = Brace(focus_table, LEFT, buff=0.1)
        brace_2_text = TypstMath("2").points.scale(1.75).next_to(brace_2, LEFT, buff=0.2).r
        brace_n_explain = Text("表头状态", font=local_font)
        brace_n_explain.points.next_to(brace_n, UP, buff=0.2)
        brace_2_explain = Text("格子内容", font=local_font)
        brace_2_explain.points.next_to(brace_2, LEFT, buff=0.2)
        grid_cell_example = GridCell(
            state_name="",
            write_bit="",
            move_dir="",
        )
        grid_cell_example.points.scale(2).move_to(DOWN * 2 + LEFT * 5.5)
        placeholder_grid = grid_cell_example.copy().points.scale(1.3).r
        brace_cell = Brace(placeholder_grid, RIGHT, buff=0.1)
        brace_cell.points.rotate(PI)
        grid_cell_status = Group(*[
            GridCell(
                state_name=state,
                write_bit="",
                move_dir="",
            ).points.scale(0.8).r
            for state in ["A", "B", "C", "D", "E", "..."]
        ])
        grid_cell_status.points.arrange(RIGHT).next_to(brace_cell, RIGHT).shift(UP * 1)
        text_status_count = TypstMath("times n").points.scale(1.5).r
        text_status_count.points.next_to(grid_cell_status, RIGHT, buff=0.3)
        grid_cell_writings = Group(*[
            GridCell(
                state_name="",
                write_bit=write_bit,
                move_dir="",
            ).points.scale(0.8).r
            for write_bit in ["0", "1"]
        ])
        grid_cell_writings.points.arrange(RIGHT).next_to(brace_cell, RIGHT)
        text_writing_count = TypstMath("times 2").points.scale(1.5).r
        text_writing_count.points.next_to(grid_cell_writings, RIGHT, buff=0.3)
        grid_cell_directions = Group(*[
            GridCell(
                state_name="",
                write_bit="",
                move_dir=move_dir,
            ).points.scale(0.8).r
            for move_dir in ["LEFT", "RIGHT"]
        ])
        grid_cell_directions.points.arrange(RIGHT).next_to(brace_cell, RIGHT).shift(DOWN * 1)
        text_direction_count = TypstMath("times 2").points.scale(1.5).r
        text_direction_count.points.next_to(grid_cell_directions, RIGHT, buff=0.3)
        brace_multi = Brace(
            Group(
                grid_cell_status, grid_cell_writings, grid_cell_directions,
                text_status_count, text_writing_count, text_direction_count,
            ),
            RIGHT,
            buff=0.3,
        )
        brace_multi_text = TypstMath("= 4n")
        brace_multi_text.points.scale(1.5).next_to(brace_multi, RIGHT, buff=0.3)
        brace_multi_text_2 = TypstMath("= 4n+1")
        brace_multi_text_2.points.scale(1.5).next_to(brace_multi, RIGHT, buff=0.3)
        seperator_line = DashedLine(UP * 5, DOWN * 5).points.shift(RIGHT * 7.5).r
        text_final_status = TypstMath("(4n+1)^(2n)")
        text_final_status.points.scale(2).move_to(RIGHT * 10.5)
        text_tms_upperbound = Text(
            "全部<c GREEN_A> n 状态</c>图灵机\n个数<c YELLOW>上限</c>",
            format="rich",
            font=local_font
        )
        text_tms_upperbound.points.scale(1.25).next_to(text_final_status, DOWN, buff=0.5)
        text_n_eq_5 = TypstMath("n=5")
        text_n_eq_5.points.scale(2).move_to(RIGHT * 17)
        text_num_5_tm = Text("16,679,880,978,201", font=local_font)
        text_num_5_tm.points.scale(1.8).next_to(text_n_eq_5, DOWN, buff=0.75)
        text_num_5_tm.color.set(color=CYAN).r

        self.play(
            Write(brace_n),
            Write(brace_n_text),
            Write(brace_2),
            Write(brace_2_text),
            lag_ratio=0.35,
        )
        self.forward(1)
        self.play(
            TransformMatchingShapes(brace_n_text, brace_n_explain),
            TransformMatchingShapes(brace_2_text, brace_2_explain),
        )
        self.forward(1)
        self.play(
            TransformMatchingShapes(brace_n_explain, brace_n_text),
            TransformMatchingShapes(brace_2_explain, brace_2_text),
        )
        self.play(
            focus_table.anim.points.shift(UP * 1.5),
            brace_2.anim.points.shift(UP * 1.5),
            brace_n.anim.points.shift(UP * 1.5),
            brace_2_text.anim.points.shift(UP * 1.5),
            brace_n_text.anim.points.shift(UP * 1.5),
        )
        self.play(
            Transform(
                focus_table.get_cell("A", "0"), # type: ignore
                grid_cell_example,
                hide_src=False,
                flatten=True,
            )
        )
        self.forward(1)
        self.play(
            Write(brace_cell),
            Succession(
                *[
                    Write(cell) for cell in grid_cell_status
                ],
                duration=2,
            ),
        )
        self.play(Write(text_status_count))
        self.forward(1)
        self.play(
            Succession(
                *[
                    Write(cell) for cell in grid_cell_writings
                ],
                duration=2,
            ),
        )
        self.play(Write(text_writing_count))
        self.forward(1)
        self.play(
            Succession(
                *[
                    Write(cell) for cell in grid_cell_directions
                ],
                duration=2,
            ),
        )
        self.play(Write(text_direction_count))
        self.forward(2)
        self.play(
            Write(brace_multi),
            Write(brace_multi_text),
        )
        self.forward(1)
        self.play(TransformMatchingDiff(brace_multi_text, brace_multi_text_2))
        self.forward(1)
        self.play(
            self.camera.anim.points.shift(RIGHT * 6),
            Write(seperator_line),
            Write(text_final_status),
            lag_ratio=0.2,
        )
        self.forward(0.5)
        self.play(Write(text_tms_upperbound))
        self.forward(1.5)
        self.play(
            FadeOut(seperator_line),
            Group(text_final_status, text_tms_upperbound).anim.points.shift(RIGHT),
            self.camera.anim.points.shift(RIGHT * 10),
        )
        self.play(Write(text_n_eq_5))
        self.forward(0.5)
        self.play(Write(text_num_5_tm))
        self.forward(2)
        self.play(
            FadeOut(text_n_eq_5),
            FadeOut(text_num_5_tm),
            FadeOut(text_final_status),
            FadeOut(text_tms_upperbound),
        )
        self.forward(1)

class s3_4(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_4 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        text_many_tms = TypstDoc(get_typ_doc("many_tms"), depth=10)
        text_many_tms.points.move_to(ORIGIN)
        set_0_to_399 = list(range(400))
        batch_1 = random.sample(set_0_to_399, 100)
        rec_hl_1 = Group(*[
            SurroundingRect(text_many_tms[f"$H_({i})$"])
            for i in batch_1
        ])
        for i in batch_1:
            set_0_to_399.remove(i)
        batch_2 = random.sample(set_0_to_399, 150)
        rec_hl_2 = Group(*[
            SurroundingRect(text_many_tms[f"$H_({i})$"]).color.set(color=GREEN_B).r
            for i in batch_2
        ])
        for i in batch_2:
            set_0_to_399.remove(i)
        # 视觉效果考虑
        H_only = rejection_sample(
            set_0_to_399,
            k=1,
            cond=lambda m: m % 20 >= 5 and m % 20 <= 15 and 120 <= m <= 280,
        )[0]
        set_0_to_399.remove(H_only)
        batch_3 = set_0_to_399
        rec_hl_3 = Group(*[
            SurroundingRect(text_many_tms[f"$H_({i})$"]).color.set(color=RED_B).r
            for i in batch_3
        ])
        text_H_beaver = TypstMath("H_(\"BusyBeaver\")")
        text_H_beaver.points.scale(2).r.astype(VItem).color.set(color=CYAN)

        class TMShow(Timeline):
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
            def __init__(
                self,
                core: TuringMachineCore,
                text: str = "",
                stop_at: int = 5,
            ):
                self.core = core
                self.text = text
                self.stop_at = stop_at
                super().__init__()
            
            def construct(self) -> None:
                width = cast(float, Config.get.frame_width)
                height = cast(float, Config.get.frame_height)
                bg = Rect(width, height, depth=20)
                bg.fill.set(color=BLACK, alpha=1.0)
                frame_bg = Rect(width, height, depth=-20)
                frame_bg.stroke.set(color=WHITE, alpha=1.0)
                core = self.core
                tm = TuringMachine(
                    turing_core=core,
                    showcase_radius=12,
                    table_scaling=1,
                    tape_config={"center_scaling": 1},
                    table_config={"transpose": True},
                    counter_config={"max_value": 9999},
                )
                tm.points.scale(1.3)
                text = Text(self.text, font=local_font, format="rich").points.scale(1.8).next_to(tm.table, RIGHT, buff=0.5).r

                self.play(
                    FadeIn(bg),
                    FadeIn(frame_bg),
                    FadeIn(tm.table),
                    FadeIn(tm.framebox),
                    FadeIn(tm.tape_item),
                )
                self.play(Write(text))
                for _ in range(self.stop_at):
                    tm.step(duration=0.1).run_step_anim(self, compress=True)
                self.forward(1)
                self.play(
                    FadeOut(tm.table),
                    FadeOut(tm.framebox),
                    FadeOut(tm.tape_item),
                    FadeOut(bg),
                    FadeOut(frame_bg),
                    FadeOut(text),
                )

        self.play(Write(text_many_tms))
        self.forward(1)
        self.play(
            *[
                Write(rec) for rec in rec_hl_1
            ],
            lag_ratio=0.01,
            collapse=True,
        )
        core_stop = TuringMachineCore(
            initial_tape="00001",
            start_state="A",
            halt_states=["HALT"],
        )
        core_stop.add_rule("A", "0", "A", "1", "R")
        core_stop.add_rule("A", "1", "HALT", "1", "R")
        tm_stop = TMShow(core_stop, "停机类").build().to_item().show()
        clip_tm_stop = TransformableFrameClip(
            tm_stop,
            offset=(1 / 6, 0),
            scale=0.6,
        ).show()
        self.forward(5)
        self.play(
            FadeOut(rec_hl_1),
            *[
                text_many_tms[f"$H_({i})$"].astype(VItem).anim.fill.set(alpha=0.1)
                for i in batch_1
            ],
            collapse=True,
        )
        self.forward(1.5)
        self.play(
            *[
                Write(rec) for rec in rec_hl_2
            ],
            lag_ratio=0.005,
            collapse=True,
        )
        core_loop = TuringMachineCore(
            initial_tape="01",
            start_state="A",
            halt_states=["HALT"],
        )
        core_loop.add_rule("A", "0", "A", "0", "R")
        core_loop.add_rule("A", "1", "A", "1", "L")
        tm_loop = TMShow(core_loop, "配置相同类", stop_at=7).build().to_item().show()
        clip_tm_loop = TransformableFrameClip(
            tm_loop,
            offset=(-1 / 6, 0),
            scale=0.6,
        ).show()
        self.forward(6)
        self.play(
            FadeOut(rec_hl_2),
            *[
                text_many_tms[f"$H_({i})$"].astype(VItem).anim.fill.set(alpha=0.1)
                for i in batch_2
            ],
            collapse=True,
        )
        self.forward(1.5)
        self.play(
            *[
                Write(rec) for rec in rec_hl_3
            ],
            lag_ratio=0.002,
            collapse=True,
        )
        core_copy = TuringMachineCore(
            initial_tape="010101010101010101010101010",
            start_state="A",
            halt_states=["HALT"],
        )
        core_copy.add_rule("A", "0", "A", "1", "R")
        core_copy.add_rule("A", "1", "A", "0", "R")
        tm_copy = TMShow(core_copy, "配置自我复制类", stop_at=10).build().to_item().show()
        clip_tm_copy = TransformableFrameClip(
            tm_copy,
            offset=(0, 1 / 12),
            scale=0.6,
        ).show()
        self.forward(6)
        self.play(
            FadeOut(rec_hl_3),
            *[
                text_many_tms[f"$H_({i})$"].astype(VItem).anim.fill.set(alpha=0.1)
                for i in batch_3
            ],
            collapse=True,
        )
        self.forward(1.5)
        self.play(
            TransformMatchingShapes(
                text_many_tms,
                text_H_beaver,
            ),
            *[
                FadeOut(text_many_tms[f"$H_({i})$"])
                for i in range(400) if i != H_only
            ],
            collapse=True,
        )
        self.forward(2)

        image_bbchallenge = ImageItem("resources/busy_beaver_challenge.png")
        image_bbchallenge.points.scale(2).shift(UP * 1)
        text_bb_challenge = Text("忙碌海狸挑战赛", font=local_font)
        text_bb_challenge.points.scale(2).next_to(image_bbchallenge, DOWN, buff=0.5)

        self.play(FadeOut(text_H_beaver))
        self.play(
            FadeIn(image_bbchallenge),
            Write(text_bb_challenge),
        )
        self.forward(2)
        self.play(
            FadeOut(image_bbchallenge),
            FadeOut(text_bb_challenge),
        )
        self.forward(1)

class s3_5(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_5 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        def history_grid_gen(
            seq: str,
            square_size: float = 0.25,
            transpose: bool = False,
            max_per_line: int = 75,
        ) -> Group:
            DEBUG = False
            height = len(seq.splitlines())
            width = max([len(line) for line in seq.splitlines()])
            lines = seq.splitlines()
            if transpose:
                lines = list(reversed(lines))
                
            final_group = Group()
            idl_total = len(lines) // max_per_line + 1
            for idl in range(idl_total):
                slice = lines[idl * max_per_line:(idl + 1) * max_per_line]
                if len(slice) == 0:
                    continue
                group = Group()
                for i, line in enumerate(slice):
                    for j, char in enumerate(line):
                        if char == "0":
                            group.add(
                                Rect(square_size, square_size) \
                                    .fill.set(color=WHITE, alpha=1).r \
                                    .stroke.set(color=WHITE, alpha=1).r
                            )
                        else:
                            group.add(
                                Rect(square_size, square_size) \
                                    .fill.set(color=BLACK, alpha=1).r
                                    .stroke.set(color=WHITE, alpha=1).r
                            )
                if DEBUG:
                    print(f"slice {idl}: width {width}, height {height}, max_per_line {max_per_line}, actual lines {len(slice)}")
                group.points.arrange_in_grid(height, width, buff=0)
                if transpose:
                    group.points.rotate(PI / 2)
                final_group.add(group)
            if not transpose:
                final_group.points.arrange_in_grid(n_rows=1, buff=0.2, aligned_edge=UP).move_to(ORIGIN)
            else:
                final_group.points.arrange_in_grid(n_cols=1, buff=0.2, aligned_edge=LEFT).move_to(ORIGIN)
            return final_group
        
        tm_types = [
            "cycler",
            "translated_cycler",
            "bouncer",
            "counter",
            "bell",
            "fractal",
            "chaotic",
        ]
        file_txts = [
            Path(
                f"resources/different_tms_instances/{name}.txt") \
                    .read_text(encoding="utf-8")
            for name in tm_types
        ]
        text_diff_type = TypstDoc(get_typ_doc("different_turing_type"))
        text_diff_type.points.scale(0.85)
        group_types = Group(*[
            Group(
                text_diff_type.get_label(type_name),
                history_grid_gen(type_txt, square_size=0.1),
            ).points.arrange(DOWN).move_to(ORIGIN).r
            for type_name, type_txt in zip(tm_types, file_txts)
        ])
        for i, item in enumerate(group_types):
            item[1].points.next_to(item[0], DOWN, aligned_edge=LEFT, buff=0.2)
            if i > 0 and i != 5:
                group_types[i].points.next_to(group_types[i - 1][1], RIGHT, aligned_edge=UP, buff=0.35)
            if i == 5:
                group_types[i].points.next_to(group_types[1][0], RIGHT, aligned_edge=UP, buff=4.5)

        group_types.points.move_to(ORIGIN)

        self.play(
            *[
                Write(tm_type) for tm_type in group_types
            ],
            lag_ratio=0.75,
            duration=4,
        )
        self.forward(2)
        self.play(
            FadeOut(group_types),
        )
        self.forward(0.5)

        self.camera.save_state()

        text_10pow12 = TypstMath("10^(12) quad =>").points.scale(2).move_to(LEFT * 3).r
        text_symmetry_compress = TypstDoc(get_typ_doc("symmetry_compress"))
        text_symmetry_compress.points.next_to(text_10pow12, RIGHT, buff=1).scale(1.75)
        text_lr = text_symmetry_compress.get_label("lr")
        text_syn = text_symmetry_compress.get_label("syn")
        text_re = text_symmetry_compress.get_label("re")
        text_sc_other = Group(
            text_symmetry_compress[2:8], text_symmetry_compress[24],
            text_symmetry_compress[26:32],
        )
        text_many_tms = TypstDoc(get_typ_doc("many_tms"), depth=10)
        text_many_tms.points.scale(2)
        text_bb = TypstText("1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA")
        text_bb.points.scale(3)
        text_bb.astype(VItem).color.set(color=CYAN)
        
        self.play(Write(text_10pow12))
        self.forward(0.5)
        self.play(
            Write(text_lr),
            Write(text_syn),
            Write(text_re),
            Write(text_sc_other),
            lag_ratio=0.5,
        )
        self.forward(2)
        self.prepare(
            self.camera.anim.points.scale(2),
            duration=4,
            rate_func=smooth,
        )
        self.play(
            FadeOut(text_10pow12),
            FadeOut(Group(
                text_lr,
                text_syn,
                text_re,
                text_symmetry_compress[2:8], text_symmetry_compress[24],
            )),
            text_symmetry_compress[26:32].anim.points.move_to(ORIGIN).scale(1.5).r
        )
        self.play(
            Transform(
                text_symmetry_compress[26:32],
                text_many_tms,
                flatten=True,
            ),
            duration=2,
        )
        self.forward(0.5)
        self.play(
            Transform(
                text_many_tms,
                text_bb,
            ),
            duration=2,
        )
        self.forward(1.5)
        self.play(FadeOut(text_bb))

        text_1962_2024 = TypstMath("1962")
        text_1962_2024.points.scale(2.5)
        text_4bbs = Text("4 Busy Beavers", font=local_font)
        text_4bbs.points.scale(1.2).to_border(LEFT + UP)

        self.camera.load_state()
        self.play(FadeIn(text_1962_2024))
        self.forward(0.5)
        self.play(
            ItemUpdater(
                text_1962_2024,
                lambda p: TypstMath(
                    f"{1962 + int(p.alpha * (2024 - 1962))}"
                ).points.scale(2.5 + 1.5 * p.alpha).r
            ),
            duration=3,
        )
        self.forward(1)
        self.play(TransformMatchingShapes(
            text_1962_2024,
            text_4bbs,
        ))
        self.forward(0.5)

        def get_only_table(
                core_rulers: list[Callable[[TuringMachineCore], TuringMachineCore]] | Callable[[TuringMachineCore], TuringMachineCore],
                table_scaling: float = 1.0,
            ):
            from functools import reduce
            core = TuringMachineCore(
                initial_tape="",
                start_state="A",
                halt_states=["HALT"],
            )
            core = core_rulers(core) if isinstance(core_rulers, Callable) else reduce(lambda c, r: r(c), core_rulers, core)
            tm = TuringMachine(
                turing_core=core,
                showcase_radius=2,
                table_scaling=table_scaling,
                tape_config={"center_scaling": 1},
                table_config={"transpose": True},
                counter_config={"max_value": 9999},
            )
            return tm.table
        
        def ruler_bb1(c: TuringMachineCore):
            c.add_rule("A", "0", "HALT", "1", "R")
            c.add_rule("A", "1", "HALT", "1", "R")
            return c
        def ruler_bb2(c: TuringMachineCore):
            c.add_rule("A", "0", "B", "1", "R")
            c.add_rule("A", "1", "B", "1", "L")
            c.add_rule("B", "0", "A", "1", "L")
            c.add_rule("B", "1", "HALT", "1", "R")
            return c
        def ruler_bb3(c: TuringMachineCore):
            c.add_rule("A", "0", "B", "1", "R")
            c.add_rule("A", "1", "HALT", "1", "R")
            c.add_rule("B", "0", "B", "1", "L")
            c.add_rule("B", "1", "C", "0", "R")
            c.add_rule("C", "0", "C", "1", "L")
            c.add_rule("C", "1", "A", "1", "L")
            return c
        def ruler_bb4(c: TuringMachineCore):
            c.add_rule("A", "0", "B", "1", "R")
            c.add_rule("A", "1", "B", "1", "L")
            c.add_rule("B", "0", "A", "1", "L")
            c.add_rule("B", "1", "C", "0", "L")
            c.add_rule("C", "0", "HALT", "1", "R")
            c.add_rule("C", "1", "D", "1", "L")
            c.add_rule("D", "0", "D", "1", "R")
            c.add_rule("D", "1", "A", "0", "R")
            return c
        
        colors = [GREEN_B, BLUE_B, YELLOW, RED_A]
        text_H1234 = [
            TypstMath(f"\"BB\"_{i}").points.scale(2).r
            for i in range(1, 5)
        ]
        for txt, c in zip(text_H1234, colors):
            txt.astype(VItem).color.set(color=c)
        steps_bbs = [1, 6, 21, 107]
        text_steps_bbs = Group(*[
            Text(str(step), font=local_font) \
                .points.scale(1.5).r \
                .color.set(color=c).r
            for step, txt_h, c in zip(steps_bbs, text_H1234, colors)
        ])
        table_bbs = [
            get_only_table(ruler, table_scaling=0.7) \
                .points.next_to(txt, RIGHT, buff=0.5).r
            for ruler, txt in zip(
                [ruler_bb1, ruler_bb2, ruler_bb3, ruler_bb4],
                text_steps_bbs,
            )
        ]
        seqs = [
            Path(f"resources/bbs_track/bb{i}.txt").read_text(encoding="utf-8")
            for i in range(1, 5)
        ]
        bb_grids = [
            history_grid_gen(
                seq,
                square_size=0.35 - (i / 4) * 0.345,
                transpose=True,
                max_per_line=54,
            )
            for i, seq in enumerate(seqs)
        ]
        text_ellipsis = TypstMath("...").points.scale(1.5).r
        bb_grids[3] = Group( # type: ignore
            Group(
                bb_grids[3][0],
                text_ellipsis.copy().points.next_to(bb_grids[3][0], RIGHT).r
            ),
            Group(
                text_ellipsis.copy().points.next_to(bb_grids[3][1], LEFT).r,
                bb_grids[3][1]
            ),
        ).points.arrange(DOWN, buff=0.2).r
        groups_bb_info = [
            Group(
                txt, table, grid
            ).points.arrange(RIGHT, buff=0.25).r
            for txt, table, grid in zip(text_H1234, table_bbs, bb_grids)
        ]
        groups_bb_info[1].points.next_to(groups_bb_info[0], RIGHT, buff=1.5)
        group_groups_bb_info = Group(
            Group(groups_bb_info[0], groups_bb_info[1]),
            groups_bb_info[2], groups_bb_info[3],
        ).points.arrange(
            DOWN,
            buff=0.1,
            aligned_edge=LEFT,
        ).next_to(text_4bbs, DOWN, aligned_edge=LEFT, buff=0.15)

        seq_bb5 = Path("resources/bbs_track/BB5.txt").read_text(encoding="utf-8")
        grid_bb5 = history_grid_gen(
            seq_bb5,
            square_size=0.01,
            transpose=True,
            max_per_line=100,
        )

        self.play(
            Succession(*[
                Succession(
                    Write(g),
                    Wait(0.5),
                ) for g in groups_bb_info
            ])
        )
        self.forward(2)

        text_H5 = TypstMath("\"BB\"_5").points.scale(2).next_to(text_H1234[-1], DOWN, buff=3).r
        text_H5.astype(VItem).color.set(color=CYAN)
        grid_bb5.points.scale(0.8).next_to(text_H5, DOWN, aligned_edge=LEFT, buff=0.5).r
        
        self.play(
            Write(text_H5),
            self.camera.anim.points.shift(DOWN * 9),
        )
        self.play(
            Write(grid_bb5),
            duration=2,
        )
        self.forward(2)
        
        axes = Axes(
            x_range=(0, 6),
            y_range=(0, 200, 25),
            x_length=7,
            y_length=7,
        ).points.move_to(ORIGIN).r
        axes(VItem).color.set(alpha=0.5)
        pt1 = axes.coords_to_point(1, 1)
        pt2 = axes.coords_to_point(2, 6)
        pt3 = axes.coords_to_point(3, 21)
        pt4 = axes.coords_to_point(4, 107)
        pt5 = axes.coords_to_point(4, 500)
        dot1 = Dot(pt1, radius=0.075, stroke_alpha=1, fill_alpha=0, color=GREEN_B)
        dot2 = Dot(pt2, radius=0.075, stroke_alpha=1, fill_alpha=0, color=BLUE_B)
        dot3 = Dot(pt3, radius=0.075, stroke_alpha=1, fill_alpha=0, color=YELLOW)
        dot4 = Dot(pt4, radius=0.075, stroke_alpha=1, fill_alpha=0, color=RED_A)
        dot5 = Dot(pt5, radius=0.075, stroke_alpha=1, fill_alpha=0, color=CYAN)
        line1 = DashedLine(pt1, pt2).color.set(color=GREEN_B, alpha=0.5).r
        line2 = DashedLine(pt2, pt3).color.set(color=BLUE_B, alpha=0.5).r
        line3 = DashedLine(pt3, pt4).color.set(color=YELLOW, alpha=0.5).r
        line4 = DashedLine(pt4, pt5).color.set(color=RED_A, alpha=0.5).r
        rect_6 = SurroundingRect(
            axes.x_axis.get_tick(6),
            color=GREY_C,
        )
        quest_6 = TypstMath("\"BB\"_6 ?")
        quest_6.points.scale(1.5).next_to(rect_6, RIGHT + UP, buff=0.1)
        
        text_4bbs.hide()
        for i in range(4):
            table_bbs[i].hide()
            bb_grids[i].hide()
        self.play(
            self.camera.anim.points.shift(UP * 9),
            Write(axes),
            *[
                txt.anim.points.scale(0.6).next_to(pt, UP)
                for txt, pt in zip(text_H1234, [pt1, pt2, pt3, pt4])
            ],
            lag_ratio=0.2,
        )
        grid_bb5.hide()
        self.play(
            Write(dot1),
            Write(dot2),
            Write(dot3),
            Write(dot4),
            Write(line1),
            Write(line2),
            Write(line3),
            Write(line4),
            lag_ratio=0.75,
            duration=2,
        )
        self.forward(1.5)
        self.play(
            Write(rect_6),
            Write(quest_6),
        )
        self.forward(1.5)

        quest_6_sim = TypstMath("\"BB\"_6 approx").points.scale(1.5).move_to(ORIGIN).r
        text_collatz = TypstDoc(get_typ_doc("collatz")).points.scale(1.5).next_to(quest_6_sim, RIGHT, buff=0.5).r

        self.play(
            FadeOut(rect_6),
            Group(
                axes,
                line1, line2, line3, line4,
                dot1, dot2, dot3, dot4,
                *text_H1234,
            ).anim.points.shift(LEFT * 2.5),
            TransformMatchingShapes(quest_6, quest_6_sim),
        )
        self.play(Write(text_collatz))
        self.forward(2)
        self.play(
            FadeOut(
                Group(
                    axes,
                    line1, line2, line3, line4,
                    dot1, dot2, dot3, dot4,
                    *text_H1234,
                )
            ),
            FadeOut(quest_6_sim),
            FadeOut(text_collatz),
        )
        self.forward(1)

class s3_6(Timeline):
    """
    uv run janim run s3_BusyBeaver.py s3_6 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        install_dirty_patch()
        bb6_rule = "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE"
        text_bb6_1 = Text(
            bb6_rule,
            font=local_font,
            color=GREY_C,
        ).points.scale(1.25).to_border(UP).r
        bb6_core = parse_rule_to_core(bb6_rule)[0]
        tm_bb6 = TuringMachine(
            turing_core=bb6_core,
            showcase_radius=12,
            table_scaling=1,
            tape_config={"center_scaling": 1},
            table_config={"transpose": True},
            counter_config={"max_value": 9999},
        )
        tm_bb6.is_table_shown = True

        self.play(Write(text_bb6_1))
        self.play(
            FadeIn(tm_bb6.table),
            FadeIn(tm_bb6.framebox),
            FadeIn(tm_bb6.tape_item),
        )
        self.forward(0.5)
        
        for _ in range(60):
            tm_bb6.step(duration=0.01).run_step_anim(self, compress=True)

        mask_rec = Rect(20, 20)
        mask_rec.fill.set(color=BLACK, alpha=0.9).r
        text_10_nest_pow_15 = TypstDoc(get_typ_doc("10_nest_pow_15"))
        text_10_nest_pow_15.points.scale(1.5).move_to(ORIGIN)
        text_10_nest_pows = [
            text_10_nest_pow_15.get_label(f"pt{i}") \
                .points.move_to(ORIGIN).scale(1.75).r
            for i in range(1, 16)
        ]
        text_halt = Text("HALT", font=local_font, color=RED)
        text_halt.points.scale(2.5).move_to(DOWN * 2).r

        self.play(
            Write(mask_rec),
            FadeIn(text_10_nest_pows[0]),
            lag_ratio=0.5,
        )
        for i in range(1, 15):
            self.play(
                TransformMatchingDiff(
                    text_10_nest_pows[i - 1],
                    text_10_nest_pows[i],
                ),
                duration=0.2,
            )
        self.forward(1)
        self.play(Write(text_halt))
        self.forward(1.5)

        class SpecialConfigTape:
            center_idx: int
            cells: Group[TapeCell]
            bracegroup_0infL: Group
            bracegroup_1: Group
            bracegroup_0n: Group
            bracegroup_11: Group
            bracegroup_05C: Group
            bracegroup_0infR: Group
            full: Group

        def get_special_config_tape(n: int, empty_len: int = 15) -> SpecialConfigTape:
            sp_c = SpecialConfigTape()
            sp = "1" + "0" * n + "11" + "0" * 5
            left = "0" * empty_len
            right = "0" * (empty_len - n)
            string = left + sp + right
            cells = Group(*[
                TapeCell(
                    square_size=0.8,
                    tile_data=t,
                    line_color=WHITE,
                    text_scaling=1.0,
                ).points.scale(0.8).r
                for t in string
            ]).points.arrange(RIGHT, buff=0).r
            idx_first_1 = empty_len
            cells.points.shift(-cells[idx_first_1].points.box.center)

            brace_text_scale = 1

            br_0inf_L = Brace(cells[idx_first_1 - 8:idx_first_1], DOWN)
            txt_0inf_L = TypstText("固定 $oo$ 个 $0$")
            txt_0inf_L.points.scale(brace_text_scale).next_to(br_0inf_L, DOWN)
            sp_c.bracegroup_0infL = Group(br_0inf_L, txt_0inf_L)

            br_1 = Brace(cells[idx_first_1:idx_first_1 + 1], UP)
            txt_1 = TypstText("固定 $1$ 个 $1$")
            txt_1.points.scale(brace_text_scale).next_to(br_1, UP)
            sp_c.bracegroup_1 = Group(br_1, txt_1)

            max_show = 18
            end_idx = idx_first_1 + 1 + n if n <= max_show else idx_first_1 + 1 + max_show
            br_0n = Brace(cells[idx_first_1 + 1:end_idx], DOWN)
            txt_0n = TypstText(f"固定 $n$ 个 $0$")
            txt_0n["$n$"].astype(VItem).color.set(color=YELLOW).r
            txt_0n.points.scale(brace_text_scale).next_to(br_0n, DOWN)
            sp_c.bracegroup_0n = Group(br_0n, txt_0n)

            br_11 = Brace(cells[idx_first_1 + 1 + n:idx_first_1 + 1 + n + 2], UP)
            txt_11 = TypstText("固定 $2$ 个 $1$")
            txt_11.points.scale(brace_text_scale).next_to(br_11, UP)
            sp_c.bracegroup_11 = Group(br_11, txt_11)

            br_05C = Brace(cells[idx_first_1 + 1 + n + 2:idx_first_1 + 1 + n + 2 + 5], DOWN)
            txt_05C = TypstText("与表头状态相关的 $5$ 位")
            txt_05C.points.scale(brace_text_scale).next_to(br_05C, DOWN)
            sp_c.bracegroup_05C = Group(br_05C, txt_05C)

            max_show = 5
            end_idx = idx_first_1 + 1 + n + 2 + 5 + 3 if n <= max_show else idx_first_1 + 1 + max_show + 2 + 5 + 3
            br_0inf_R = Brace(cells[idx_first_1 + 1 + n + 2 + 5:end_idx], UP)
            txt_0inf_R = TypstText("固定 $oo$ 个 $0$")
            txt_0inf_R.points.scale(brace_text_scale).next_to(br_0inf_R, UP)
            sp_c.bracegroup_0infR = Group(br_0inf_R, txt_0inf_R)

            sp_c.center_idx = idx_first_1
            sp_c.cells = cells

            sp_c.full = Group(
                cells,
                sp_c.bracegroup_0infL,
                sp_c.bracegroup_1,
                sp_c.bracegroup_0n,
                sp_c.bracegroup_11,
                sp_c.bracegroup_05C,
                sp_c.bracegroup_0infR,
            )

            return sp_c

        sp_4k = get_special_config_tape(5)
        sp_4k.full.points.shift(LEFT * 3)
        text_Cn = TypstMath("C(n)").points.scale(1.5).next_to(text_bb6_1, DOWN, buff=1).r
        text_Cn["n"].astype(VItem).color.set(color=YELLOW)
        text_sp_config_rules = TypstDoc(get_typ_doc("sp_config_rules"))
        text_sp_config_rules["$ k $", ...].astype(VItem).color.set(color=BLUE_B)
        text_sp_config_rules["$ space^k $", ...].astype(VItem).color.set(color=BLUE_B)
        text_sp_config_rules.points.scale(1.25)
        text_group_sp_rules = Group(*[
            text_sp_config_rules.get_label(f"R{i}")
            for i in range(4)
        ])
        text_group_sp_rules.points.arrange_in_grid(
            n_rows=2,
            n_cols=2,
            h_buff=1.5,
            v_buff=0.5,
        ).to_border(DOWN)
        text_R1_2 = text_sp_config_rules.get_label("R1.2").points.move_to(text_group_sp_rules[1]).r
        text_R1_3 = text_sp_config_rules.get_label("R1.3").points.move_to(text_group_sp_rules[1]).r
        text_R1_4 = text_sp_config_rules.get_label("R1.4").points.move_to(text_group_sp_rules[1]).r

        self.play(
            FadeOut(mask_rec),
            FadeOut(text_halt),
            FadeOut(text_10_nest_pows[-1]),
            FadeOut(tm_bb6.table),
            FadeOut(tm_bb6.tape_item),
            FadeOut(tm_bb6.framebox),
        )
        self.play(
            TransformMatchingShapes(tm_bb6.tape_item.cells_group, sp_4k.cells)
        )
        self.play(
            Succession(
                Write(sp_4k.bracegroup_0infL),
                Write(sp_4k.bracegroup_1),
                Write(sp_4k.bracegroup_0n),
                Write(sp_4k.bracegroup_11),
                Write(sp_4k.bracegroup_05C),
                Write(sp_4k.bracegroup_0infR),
            ),
            duration=4,
        )
        self.play(Write(text_Cn))
        self.forward(2)
        self.play(
            sp_4k.full.anim.points.shift(UP * 1),
            text_Cn.anim.points.shift(UP * 0.75),
            Write(text_group_sp_rules),
            duration=1.5,
        )
        self.forward(2)

        rect_neq5 = SurroundingRect(
            Group(*sp_4k.cells[sp_4k.center_idx + 1, sp_4k.center_idx + 5]),
            color=RED,
            buff=0.1,
        )
        rect_neq5.fill.set(color=RED, alpha=0.3)
        text_neq5 = TypstMath("n=5").points.scale(1.3).next_to(rect_neq5, UP).r
        text_neq5["n"].astype(VItem).color.set(color=YELLOW)
        text_4kp1eq5 = TypstMath("4k+1=5").points.scale(1.3).next_to(rect_neq5, UP).r
        text_4kp1eq5["k"].astype(VItem).color.set(color=BLUE_B)
        text_keq1 = TypstMath("k=1").points.scale(1.3).next_to(rect_neq5, UP).r
        text_keq1["k"].astype(VItem).color.set(color=BLUE_B)
        rect_R1 = SurroundingRect(
            text_group_sp_rules[1],
            color=RED,
        )

        self.play(Write(rect_neq5))
        self.play(Write(text_neq5))
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_neq5,
                text_4kp1eq5,
            )
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_4kp1eq5,
                text_keq1,
            )
        )
        self.forward(1)
        self.play(
            Write(rect_R1),
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_group_sp_rules[1],
                text_R1_2,
            )
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_R1_2,
                text_R1_3,
            )
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_R1_3,
                text_R1_4,
            )
        )
        self.forward(2)

        sp_35 = get_special_config_tape(35)
        sp_35.full.points.move_to(sp_4k.full, aligned_edge=LEFT)
        rect_neq35 = SurroundingRect(
            Group(*sp_35.cells[sp_35.center_idx + 1, sp_35.center_idx + 18]),
            color=RED,
            buff=0.1,
        )
        rect_neq35.fill.set(color=RED, alpha=0.3)
        text_n_eq_35 = TypstMath("n=35")
        text_n_eq_35.points.scale(1.3).next_to(rect_neq35, UP).r
        text_n_eq_35["n"].astype(VItem).color.set(color=YELLOW)
        text_explodes = Group.from_iterable(
            text_sp_config_rules.get_label(f"RC.{i}") \
                .points.move_to(UP * 2).scale(1.5).r
            for i in range(1, 8)
        )
        
        self.play(
            Transform(rect_neq5, rect_neq35),
            FadeOut(sp_4k.cells),
            FadeIn(sp_35.cells),
            Transform(sp_4k.bracegroup_0infL, sp_35.bracegroup_0infL),
            Transform(sp_4k.bracegroup_1, sp_35.bracegroup_1),
            Transform(sp_4k.bracegroup_0n, sp_35.bracegroup_0n),
            Transform(sp_4k.bracegroup_05C, sp_35.bracegroup_05C),
            Transform(sp_4k.bracegroup_11, sp_35.bracegroup_11),
            sp_4k.bracegroup_0infR.anim.points.shift(RIGHT * 20),
            Transform(text_keq1, text_n_eq_35),
            duration=2,
        )
        self.forward(0.5)
        self.play(
            TransformMatchingDiff(
                text_R1_4,
                text_group_sp_rules[1],
            ),
            FadeOut(rect_R1),
        )
        self.forward(2)
        sp_35.full.remove(sp_35.bracegroup_0infR)
        self.play(
            FadeOut(sp_35.full),
            FadeOut(text_n_eq_35),
            FadeOut(rect_neq35),
            FadeOut(text_Cn),
            text_group_sp_rules.anim.points.move_to(DOWN * 1),
            Write(text_explodes[0]),
        )
        self.forward(0.5)
        for i in range(1, 7):
            self.play(
                TransformMatchingDiff(
                    text_explodes[i - 1],
                    text_explodes[i],
                ),
                duration=0.75,
            )
            self.forward(1)

        
        rec_r0 = SurroundingRect(
            text_group_sp_rules[0],
            color=RED,
        )
        text_stop_condition = TypstText("停止条件 $n equiv 0 space (mod 4)$")
        text_stop_condition.points.scale(1.25).next_to(rec_r0, UP, buff=0.1).r
        text_stop_condition.astype(VItem).color.set(color=RED_B)
        text_stop_condition_2 = text_stop_condition.copy()
        text_stop_condition_2.points.scale(1.25)
        
        self.forward(1)
        self.play(Write(rec_r0))
        self.play(Write(text_stop_condition))
        self.forward(2)

        text_Cs = Group.from_iterable(
            TypstMath(f"C(#text(fill: rgb(\"#87CEEB\"))[{m}])").points.scale(1.5).r
            for m in ["5", "35", "88574", "1062300...696959", "..."]
        ).points.arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN).r
        self.play(FadeOut(text_group_sp_rules))
        self.play(
            FadeOut(rec_r0),
            FadeOut(text_stop_condition),
            TransformMatchingDiff(text_explodes[-1].copy(), text_Cs[0]),
            TransformMatchingDiff(text_explodes[-1].copy(), text_Cs[1]),
            TransformMatchingDiff(text_explodes[-1].copy(), text_Cs[2]),
            TransformMatchingDiff(text_explodes[-1].copy(), text_Cs[3]),
            TransformMatchingDiff(text_explodes[-1], text_Cs[4]),
        )
        text_stop_condition_2.points.next_to(text_Cs[0], UP, aligned_edge=LEFT, buff=0.35)
        self.play(FadeIn(text_stop_condition_2))
        self.forward(1)

        list_formulas_table = [
            ["n", "A_n space \"formula\"", "A_n space (mod 2^m)", "k_n", "r_n"],
            ["0", "", "5", "1", "1"],
            ["1", "A_1 = (3^(k_0+3)-11)/2=", "35", "8", "3"],
            ["2", "A_2 = (3^(k_1+3)+1)/2=", "88574", "22143", "2"],
            ["3", "A_3 = (3^(k_2+3)-11)/2=", "255 space (mod 2^(14))", "63 space (mod 2^(12))", "3"],
            ["4", "A_4 = (3^(k_3+3)+1)/2=", "4741 space (mod 2^(13))", "1185 space (mod 2^(11))", "1"],
            ["5", "A_5 = (3^(k_4+3)-11)/2=", "2147 space (mod 2^(12))", "536 space (mod 2^(10))", "3"],
            ["6", "A_6 = (3^(k_5+3)+1)/2=", "990 space (mod 2^(11))", "247 space (mod 2^9)", "2"],
            ["7", "A_7 = (3^(k_6+3)-11)/2=", "175 space (mod 2^(10))", "43 space (mod 2^8)", "3"],
            ["8", "A_8 = (3^(k_7+3)+1)/2=", "253 space (mod 2^9)", "63 space (mod 2^7)", "1"],
            ["9", "A_9 = (3^(k_8+3)-11)/2=", "127 space (mod 2^8)", "31 space (mod 2^6)", "3"],
            ["10", "A_10 = (3^(k_9+3)+1)/2=", "69 space (mod 2^7)", "17 space (mod 2^5)", "1"],
            ["11", "A_11 = (3^(k_10+3)-11)/2=", "3 space (mod 2^6)", "0 space (mod 2^4)", "3"],
            ["12", "A_12 = (3^(k_11+3)+1)/2=", "14 space (mod 2^5)", "3 space (mod 2^3)", "2"],
            ["13", "A_13 = (3^(k_12+3)-11)/2=", "7 space (mod 2^4)", "1 space (mod 2^2)", "3"],
            ["14", "A_14 = (3^(k_13+3)+1)/2=", "1 space (mod 2^3)", "0 space (mod 2^1)", "1"],
            ["15", "A_15 = (3^(k_14+3)-11)/2=", "0 space (mod 2^2)", "", "0"]
        ]
        from functools import reduce
        flatten_formulas_table = reduce(lambda a, b: a + b, list_formulas_table)
        group_formulas_table = Group.from_iterable(
            TypstMath(cell).points.scale(1.2).r
            for cell in flatten_formulas_table
        ).points.arrange_in_grid(
            n_cols=5,
            v_buff=0.1,
            aligned_edge=LEFT,
        ).r
        group_f_t_col_n = Group(*group_formulas_table[0::5])
        group_f_t_col_An = Group(*group_formulas_table[1::5])
        group_f_t_col_An_mod = Group(*group_formulas_table[2::5])
        group_f_t_col_kn = Group(*group_formulas_table[3::5])
        group_f_t_col_rn = Group(*group_formulas_table[4::5])
        group_f_t_col_n.points.next_to(group_f_t_col_An, LEFT, buff=0.3).shift(UP * 0.075)
        group_f_t_col_n.astype(VItem).color.set(color=GREY_D)
        group_f_t_col_An_mod.astype(VItem).color.set(color=YELLOW)
        group_f_t_col_kn.astype(VItem).color.set(color=BLUE_B)
        group_f_t_col_rn.astype(VItem).color.set(color=RED)
        group_formulas_table.points.move_to(ORIGIN).to_border(UP, buff=2.5)
        rec_stop_condition = SurroundingRect(
            text_stop_condition_2,
            color=RED,
        )
        rec_rn = SurroundingRect(
            group_f_t_col_rn,
            color=RED,
        )
        arrow_stop_con_rn = Arrow(
            text_stop_condition_2.points.box.right,
            rec_rn.points.box.top,
            buff=0.5,
            color=RED,
        )
        rec_halt = SurroundingRect(
            group_f_t_col_rn[-1],
            color=RED,
        )
        rec_15 = SurroundingRect(
            group_f_t_col_n[-1],
            color=GREY_A,
        )
        text_rec_halt = Text("到达终止条件", font=local_font)
        text_rec_halt2 = Text("15 轮 C(n) 迭代到达终止条件", font=local_font)
        text_rec_halt.points.next_to(rec_halt, LEFT, buff=0.2)
        text_rec_halt2.points.next_to(rec_halt, LEFT, buff=0.2)
        text_10_pow_tower_15 = TypstMath("10 arrow.t arrow.t 15")
        text_10_pow_tower_15.points.scale(3)

        self.play(FadeOut(text_Cs))
        self.play(Write(group_formulas_table))
        self.forward(2)
        self.play(
            Write(rec_stop_condition),
            Write(arrow_stop_con_rn),
            Write(rec_rn),
            lag_ratio=0.5,
        )
        self.forward(2)
        self.prepare(
            FadeOut(rec_rn),
            FadeOut(arrow_stop_con_rn),
        )
        self.play(
            self.camera.anim.points.shift(DOWN * 14),
            duration=5.0,
        )
        self.forward(1.5)
        self.play(Write(rec_halt))
        self.play(Write(text_rec_halt))
        self.forward(1)
        self.play(Write(rec_15))
        self.play(TransformMatchingDiff(
            text_rec_halt,
            text_rec_halt2,
        ))
        self.forward(2)
        self.play(self.camera.anim.points.shift(UP * 14))
        self.play(FadeOutToPoint(group_formulas_table, DOWN * 10))
        self.play(FadeIn(text_10_pow_tower_15))
        self.forward(1.5)
        self.play(FadeOut(text_10_pow_tower_15))
        self.play(
            FadeOut(rec_stop_condition),
            FadeOut(text_stop_condition_2),
            text_bb6_1.anim.points.move_to(ORIGIN)
        )

        text_x = Text("×", font=local_font).points.scale(3).r
        text_x.astype(VItem).color.set(color=RED_B)
        text_x.points.next_to(text_bb6_1, RIGHT, buff=0.5)
        bb6_rule_2 = "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE"
        text_bb6_2 = Text(
            bb6_rule_2,
            font=local_font,
            color=GREY_A,
        )
        text_bb6_2.points.scale(1.25)
        text_2_pow_nested_3_5 = TypstMath("2 arrow.t arrow.t arrow.t 5")
        text_2_pow_nested_3_5.points.scale(3.5).next_to(text_bb6_2, DOWN, buff=0.5)
        text_2_pow_nested_3_5.astype(VItem).color.set(color=LIGHT_PINK)
        
        self.forward(2)
        self.play(Write(text_x))
        self.forward(1)
        self.play(
            FadeOut(text_x),
            TransformMatchingDiff(text_bb6_1, text_bb6_2),
            lag_ratio=0.25,
        )
        self.forward(1)
        self.play(Write(text_2_pow_nested_3_5))
        self.forward(2)
        self.play(
            FadeOut(text_bb6_2),
            FadeOut(text_2_pow_nested_3_5),
        )
        self.forward(1)