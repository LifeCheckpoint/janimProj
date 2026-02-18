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
    def construct(self) -> None:
        install_dirty_patch()
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
        self.forward(3)

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
        )
        self.forward(1)
        self.play(
            Succession(
                Rotate(triangle_ant, PI / 2),
                triangle_ant.anim.points.shift(LEFT),
            ),
            TransformMatchingShapes(rect_bl1, rect_wh1),
            lag_ratio=0.25,
        )
        self.forward(1)
        self.play(
            rect_wh1.anim.points.shift(LEFT),
            triangle_ant.anim.points.shift(LEFT),
            Write(rect_wh2),
            Write(triangle_ant2),
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
    def construct(self) -> None:
        install_dirty_patch()
        def history_grid_gen(seq: str, square_size: float = 0.25) -> Group:
            height = len(seq.splitlines())
            width = max([len(line) for line in seq.splitlines()])
            group = Group()
            for i, line in enumerate(seq.splitlines()):
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
            group.points.arrange_in_grid(height, width, buff=0)
            return group
        
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
            duration=5,
        )