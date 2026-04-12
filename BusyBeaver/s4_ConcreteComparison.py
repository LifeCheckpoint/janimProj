from janim.imports import * # type: ignore
from tools import (
    get_typ_doc,
    local_font,
    CYAN,
)
from turing_machine.components.tape_cell import TapeCell
from turing_machine.components.grid_cell import GridCell
from turing_machine.components.grid_table import GridTable, Transition
from turing_machine.effects.lens import LensEffect
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.turing_machine import TuringMachine
import math

class s4_1(Timeline):
    """
    uv run janim run s4_ConcreteComparison.py s4_1 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        
        quest_6_sim = TypstMath("\"BB\"_6 approx").points.scale(1.5).move_to(ORIGIN).r
        quest_6_sim["\"BB\"_6"].astype(VItem).color.set(color=GREY_B)
        text_collatz = TypstDoc(get_typ_doc("collatz")).points.scale(1.5).next_to(quest_6_sim, RIGHT, buff=0.5).r
        Group(quest_6_sim, text_collatz).points.move_to(ORIGIN)
        text_collatz_2 = text_collatz.copy()
        text_Hc_eq = TypstText("Halting problem of $H_c =$").points.scale(1.5).r
        text_Hc_eq["$H_c$"].astype(VItem).color.set(color=GREEN_C)
        Group(text_Hc_eq, text_collatz_2).points.arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        rect_Hc = SurroundingRect(
            text_Hc_eq["$H_c$"],
            color=GREEN_C,
        )
        text_bb6_ge = TypstMath("\"BB\"_6 >=").points.scale(1.5).r
        text_bb6_ge["\"BB\"_6"].astype(VItem).color.set(color=GREY_B)
        text_bb6_ge.points.next_to(text_Hc_eq, DOWN, aligned_edge=RIGHT, buff=1.5)
        text_collatz_p = TypstText("Collatz conjecture").points.scale(1.5).r
        text_collatz_p.points.next_to(text_bb6_ge, RIGHT, buff=0.25)
        text_halt_implies_collatz = TypstText("停机 $=>$ Collatz 猜想不成立 \\ 不停机 $=>$ Collatz 猜想成立")
        text_halt_implies_collatz.points.scale(1.1).next_to(text_Hc_eq, DOWN, aligned_edge=LEFT, buff=0.1)
        text_halt_implies_collatz["停机"].astype(VItem).color.set(color=RED_A)
        text_halt_implies_collatz["不停机"].astype(VItem).color.set(color=RED_A)
        rec_bb6 = SurroundingRect(
            text_bb6_ge["\"BB\"_6"],
            color=GREY_B,
        )
        text_S_step = TypstText("$S$ steps").points.scale(1.5).r
        text_S_step.points.next_to(rec_bb6, DOWN, buff=0.25)
        text_S_step.astype(VItem).color.set(color=GREY_B)
        # def step_compress(alpha: float, to_step: int = 1000000, k: float = 10000000):
        #     _s = to_step * math.log(1 + to_step * alpha) / math.log(1 + k)
        #     return int(np.clip(_s, 1, to_step))
        # def get_hc_step_text(
        #     step: int,
        #     next_to: VItem | None = None,
        #     final_S: int = 500000,
        #     ellipsis_threshold: int = 7,
        #     scaling_coeff: float = 0.8,
        # ):
        #     step_text = str(step)
        #     if len(step_text) > ellipsis_threshold:
        #         step_text = f"{step_text[:ellipsis_threshold // 2]}...{step_text[-ellipsis_threshold // 2:]}"
        #     t = f"{step_text} \"steps\" " + ("<= " if step <= final_S else "> ") + "S"
        #     text = TypstMath(t).points.scale(1.75).r
        #     text[f"{step_text} \"steps\""].astype(VItem).color.set(color=GREEN_C)
        #     text["S"].astype(VItem).color.set(color=GREY_B)
        #     if step <= final_S:
        #         text["<= "].astype(VItem).color.set(color=WHITE)
        #     else:
        #         text["> "].astype(VItem).color.set(color=RED_A)
        #     if next_to is not None:
        #         text.points.next_to(next_to, UP, buff=0.5)
        #     return text
        # text_Hc_steps = get_hc_step_text(0, next_to=rect_Hc)
        
        self.play(
            Write(quest_6_sim),
            Write(text_collatz),
        )
        self.forward(2)
        self.play(
            TransformMatchingDiff(text_collatz, text_collatz_2),
            TransformMatchingDiff(quest_6_sim, text_Hc_eq),
        )
        self.play(Write(text_halt_implies_collatz))
        self.play(Write(rect_Hc))
        self.forward(2)
        self.play(
            self.camera.anim.points.shift(DOWN * 1),
            Write(text_bb6_ge),
        )
        self.play(TransformMatchingDiff(
            text_collatz_2.copy(),
            text_collatz_p,
        ))
        self.forward(1)
        self.play(
            Write(rec_bb6),
            Write(text_S_step),
        )
        self.forward(1)

        self.play(
            Group(
                text_halt_implies_collatz,
                text_Hc_eq[:-1],
            ).anim.points.move_to(LEFT * 4 + UP * 4),
            Group(
                text_bb6_ge,
                text_collatz_p,
                rec_bb6,
                text_S_step,
            ).anim.points.move_to(RIGHT * 4 + UP * 4).scale(0.8),
            FadeOut(
                Group(
                    text_Hc_eq[-1:],
                    rect_Hc,
                    text_collatz_2,
                )
            ),
            self.camera.anim.points.move_to(UP),
        )

        core_collatz = TuringMachineCore(
            initial_tape=["0"],
            start_state="P",
            halt_states=["HALT"]
        )
        core_collatz.add_rule("P", "0", "Q", "1", "R")
        core_collatz.add_rule("P", "1", "R", "1", "R")
        core_collatz.add_rule("Q", "0", "P", "0", "L")
        core_collatz.add_rule("Q", "1", "Z", "0", "R")
        core_collatz.add_rule("R", "0", "Z", "1", "R")
        core_collatz.add_rule("R", "1", "Q", "0", "L")
        core_collatz.add_rule("X", "0", "R", "1", "L")
        core_collatz.add_rule("X", "1", "Y", "0", "R")
        core_collatz.add_rule("Y", "0", "HALT", "1", "L")
        core_collatz.add_rule("Y", "1", "Z", "0", "L")
        core_collatz.add_rule("Z", "0", "Q", "0", "R")
        core_collatz.add_rule("Z", "1", "P", "0", "R")
        tm_collatz = TuringMachine(
            turing_core=core_collatz,
            showcase_radius=11,
            table_scaling=1,
            tape_config={"center_scaling": 1},
            table_config={"transpose": True},
            counter_config={"max_value": 9999},
        )
        tm_collatz.is_table_shown = True
        tm_collatz.is_counter_shown = False
        rec_table_collatz = SurroundingRect(
            tm_collatz.table,
            color=GREEN,
        )
        text_table_explaination = TypstText("试图找到猜想反例的图灵机 $H_c$\n\n（示意机器）")
        text_table_explaination["$H_c$"].astype(VItem).color.set(color=GREEN)
        text_table_explaination["找到猜想反例"].astype(VItem).color.set(color=RED_A)
        text_table_explaination["（示意机器）"].astype(VItem).color.set(color=GREY_C)
        text_table_explaination.points \
            .next_to(rec_table_collatz, DOWN, aligned_edge=LEFT, buff=0.25) \
            .shift(LEFT * 1.5)
        text_bb6_max_step = TypstText("$\"BB\"(6)$ 停机前 \\ 至多运行 $S$ 步")
        text_bb6_max_step.points \
            .next_to(rec_table_collatz, DOWN, aligned_edge=RIGHT, buff=0.1)
        text_bb6_max_step["$S$"].astype(VItem).color.set(color=BLUE)
        triangle_tip = Triangle()
        triangle_tip.color.set(color=BLUE, alpha=1).r.stroke.set(alpha=0)
        triangle_tip.points.scale(0.1).rotate(PI).next_to(text_bb6_max_step["$S$"], DOWN, buff=0.1)
        rec_back_progress = Rect(3, 0.25)
        rec_back_progress.color.set(color=GREY_E, alpha=1)
        rec_back_progress.points \
            .next_to(rec_table_collatz, DOWN, aligned_edge=RIGHT, buff=1.25)
        rec_front_progress = Rect(0.01, 0.25)
        rec_front_progress.color.set(color=GREEN, alpha=1)
        rec_front_progress.points.move_to(rec_back_progress.points.box.left, aligned_edge=LEFT)
        text_exceed_S = TypstText("超出 $S$ 步 \\ 不停机")
        text_exceed_S.points.next_to(rec_back_progress, RIGHT, buff=0.5)
        text_exceed_S["$S$"].astype(VItem).color.set(color=BLUE)
        text_exceed_S["不停机"].astype(VItem).color.set(color=RED_A)

        self.play(
            Write(tm_collatz.table),
            Write(tm_collatz.tape_item),
        )
        self.play(
            Write(rec_table_collatz),
            Write(text_table_explaination),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(FadeOut(rec_table_collatz))
        self.play(
            Write(triangle_tip),
            Write(rec_back_progress),
            Write(rec_front_progress),
            Write(text_bb6_max_step),
        )
        self.forward(1.5)

        def update_progress(progress_front_item: VItem, alpha: float, threshold: float = 0.82):
            progress_front_item.points.set_width(rec_back_progress.points.box.width * alpha, stretch=True)
            progress_front_item.points.move_to(rec_back_progress.points.box.left, aligned_edge=LEFT)
            if alpha >= threshold:
                progress_front_item.color.set(color=BLUE)
            else:
                progress_front_item.color.set(color=GREEN)

        self.prepare(
            DataUpdater(
                rec_front_progress,
                lambda item, p: update_progress(item, p.alpha),
            ),
            duration=5,
        )
        self.prepare(
            Flash(rec_back_progress.points.box.right, color=WHITE),
            at=5,
        )
        self.prepare(
            Write(text_exceed_S),
            at=5.5,
        )
        for _ in range(100):
            tm_collatz.step(duration=0.01).run_step_anim(self, compress=True)

        self.forward(3)
        rec_collatz_q = SurroundingRect(
            text_halt_implies_collatz["不停机 $=>$ Collatz 猜想成立"],
            color=YELLOW,
            depth=10,
        )
        rec_collatz_q.fill.set(alpha=0.25)
        self.play(Write(rec_collatz_q))
        self.forward(1)
        self.play(FadeOut(rec_collatz_q))

        # self.play(Write(text_Hc_steps))
        # self.forward(0.5)
        # self.play(
        #     ItemUpdater(
        #         text_Hc_steps,
        #         lambda p: get_hc_step_text(
        #             step=step_compress(p.alpha, to_step=10000000, k=10**65),
        #             next_to=rect_Hc,
        #             final_S=1000000,
        #             ellipsis_threshold=6,
        #         )
        #     ),
        #     duration=5.0,
        # )
        
        # rec_ge = SurroundingRect(
        #     text_Hc_steps["> S"],
        #     color=RED_A,
        # )
        # text_no_halt = Text("不停机", font=local_font, color=RED_A)
        # text_no_halt.points.scale(1.5).next_to(rec_ge, UP, buff=0.25)

        # self.play(
        #     Write(rec_ge),
        #     Write(text_no_halt),
        # )
        # self.forward(0.5)
        # self.play(Write(rec_collatz_q))
        self.forward(2)

        text_bb27_ge_goldbach = TypstText("计算 $\"BB\"(27)$ 难度 $>=$ Goldbach's 猜想")
        text_bb744_ge_riemann = TypstText("计算 $\"BB\"(744)$ 难度 $>=$ Riemann 猜想")
        group_ges = Group()
        for t, step in zip(
            [text_bb27_ge_goldbach, text_bb744_ge_riemann],
            [27, 744],
        ):
            t.points.scale(1.25)
            t[f"$\"BB\"({step})$"].astype(VItem).color.set(color=YELLOW)
            group_ges.add(t)
        group_ges.points.arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_border(RIGHT)
        arxiv_bb27 = TypstDoc(get_typ_doc("arxiv_bb27")).points.scale(0.75).r
        arxiv_bb27.points.move_to(LEFT * 7)
        group_arxiv_hl = Group(
            arxiv_bb27.get_label("par1"),
            arxiv_bb27.get_label("par2"),
            arxiv_bb27.get_label("par3"),
        )
        for txt in group_arxiv_hl:
            txt.depth.set(-20)
        rects_hl = Group.from_iterable(
            SurroundingRect(
                txt,
                color=CYAN,
                buff=0.01,
                depth=-10,
            ).color.set(alpha=1).r
            for txt in group_arxiv_hl
        )
        blog_riemann = TypstDoc(get_typ_doc("bb_744_blog")).points.scale(0.75).r
        blog_riemann.points.move_to(LEFT * 7)
        group_riemann_hl = Group(
            blog_riemann.get_label("par1"),
            blog_riemann.get_label("par2"),
        )
        for txt in group_riemann_hl:
            txt.depth.set(-20)
        rects_riemann_hl = Group.from_iterable(
            SurroundingRect(
                txt,
                color=RED_A,
                buff=0.01,
                depth=-10,
            ).color.set(alpha=1).r
            for txt in group_riemann_hl
        )

        tm_collatz.framebox.hide()
        fadeouts = [
            text_S_step,
            rec_bb6,
            text_halt_implies_collatz,
            tm_collatz.table,
            tm_collatz.tape_item,
            Group(rec_back_progress, rec_front_progress, triangle_tip),
            text_exceed_S,
            text_bb6_max_step,
            text_table_explaination,
        ]
        self.play(
            AnimGroup(
                *[
                    FadeOut(t) for t in fadeouts
                ],
                lag_ratio=0.2,
            ),
            # TransformMatchingDiff(
            #     Group(text_bb6_ge, text_collatz_p),
            #     group_ges[0],
            # ),
            self.camera.anim.points.move_to(ORIGIN),
        )
        self.play(
            self.camera.anim.points.shift(LEFT * 4),
            Write(arxiv_bb27),
        )
        self.play(Write(rects_hl))
        self.forward(1)
        self.play(Uncreate(rects_hl))
        self.play(
            self.camera.anim.points.shift(RIGHT * 4),
            FadeOut(arxiv_bb27),
            Write(group_ges[0]),
        )
        self.forward(1)
        self.play(
            self.camera.anim.points.shift(LEFT * 4),
            Write(blog_riemann),
        )
        self.play(Write(rects_riemann_hl))
        self.forward(1)
        self.play(Uncreate(rects_riemann_hl))
        self.play(
            Write(group_ges[1]),
            self.camera.anim.points.shift(RIGHT * 4),
            FadeOut(blog_riemann),
        )
        self.forward(2)
        self.play(FadeOut(group_ges))
        self.forward(1)

class s4_2(Timeline):
    """
    uv run janim run s4_ConcreteComparison.py s4_2 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        all_states = ["A", "B", "C", "D", "E", "F", "G", "H"]
        symbols = ["0", "1"]

        def make_table(n):
            states = all_states[:n]
            return GridTable(
                states=states,
                symbols=symbols,
                transitions={
                    (st, sy): Transition(
                        next_state="", write_symbol="", direction="R",
                    ) for st in states for sy in symbols
                },
                transpose=True,
            )

        def make_brace_label(table, n):
            brace = Brace(table, UP, buff=0.1)
            label = TypstMath(f"\"BB\"({n})").points.scale(1.5).next_to(brace, UP, buff=0.2).r
            label[f"\"BB\"({n})"].astype(VItem).color.set(color=YELLOW)
            return brace, label

        cur = make_table(1)
        cur.points.scale(1.35)
        cur_brace, cur_label = make_brace_label(cur, 1)
        self.play(Write(cur), Write(cur_brace), Write(cur_label))

        for n in range(2, 9):
            nxt = make_table(n)
            nxt.points.scale(1.35)
            nxt_brace, nxt_label = make_brace_label(nxt, n)
            prev_states = all_states[:n - 1]

            shared_cur = Group.from_iterable(
                cur.get_cell(st, sy) for st in prev_states for sy in symbols
            )
            shared_nxt = Group.from_iterable(
                nxt.get_cell(st, sy) for st in prev_states for sy in symbols
            )

            dur = 0.75 / (n - 1)

            self.forward(dur)
            self.play(
                *[
                    TransformMatchingShapes(c, nx) # type: ignore
                    for c, nx in zip(shared_cur, shared_nxt)
                ],
                FadeOut(Group.from_iterable(
                    t for t in cur if t not in shared_cur
                )),
                FadeIn(Group.from_iterable(
                    t for t in nxt if t not in shared_nxt
                )),
                TransformMatchingDiff(cur_brace, nxt_brace),
                TransformMatchingDiff(cur_label, nxt_label),
                duration=dur,
            )
            cur = nxt
            cur_brace = nxt_brace
            cur_label = nxt_label

        self.forward(1)
        self.play(
            FadeOut(cur),
            FadeOut(cur_brace),
            FadeOut(cur_label),
        )

        axes = Axes(
            x_range=(0, 6, 1),
            y_range=(0, 150, 25),
            x_length=8,
            y_length=6,
        ).points.move_to(ORIGIN).r
        axes(VItem).color.set(alpha=0.5)

        seqs = {
            "n^2": ([i**2 for i in range(6)], BLUE_B),
            "2^n": ([2**i for i in range(6)], GREEN_B),
            "n!": ([math.factorial(i) for i in range(6)], RED_B),
        }

        def make_seq_vis(vals, color):
            pts = [axes.coords_to_point(i, v) for i, v in enumerate(vals)]
            return Group(
                *[Line(pts[i], pts[i + 1]).color.set(color=color, alpha=0.7).r for i in range(len(pts) - 1)],
                *[Dot(pt, radius=0.05, fill_alpha=1, color=color) for pt in pts],
            ), pts

        seq_groups = {}
        seq_labels = {}
        for name, (vals, color) in seqs.items():
            grp, pts = make_seq_vis(vals, color)
            seq_groups[name] = grp
            lbl = TypstMath(name).points.scale(1.2).r
            lbl.astype(VItem).color.set(color=color)
            lbl.points.next_to(pts[-1], RIGHT, buff=0.2)
            seq_labels[name] = lbl

        # BB(0)~BB(4)
        bb_vals = [0, 1, 6, 21, 107]
        bb_pts = [axes.coords_to_point(i, v) for i, v in enumerate(bb_vals)]
        bb_dots = Group(*[
            Dot(pt, radius=0.08, stroke_alpha=1, fill_alpha=0, color=YELLOW)
            for pt in bb_pts
        ])
        bb_lines = Group(*[
            DashedLine(bb_pts[i], bb_pts[i + 1]).color.set(color=YELLOW, alpha=0.5).r
            for i in range(4)
        ])
        label_bb = TypstMath("\"BB\"(n)").points.scale(1.2).r
        label_bb.astype(VItem).color.set(color=YELLOW)
        label_bb.points.next_to(bb_pts[-1], UP, buff=0.2)

        self.play(Write(axes), duration=0.5)
        for name in ["n^2", "2^n", "n!"]:
            self.play(Write(seq_groups[name]), Write(seq_labels[name]), duration=0.5)
        self.play(
            *[Write(d) for d in bb_dots],
            *[Write(l) for l in bb_lines],
            Write(label_bb),
            lag_ratio=0.2,
            duration=0.75,
        )
        self.forward(1)

        bb4_top = np.array(bb_pts[-1]).copy()
        bb4_top[1] = axes.coords_to_point(0, 150)[1]
        line_vert = DashedLine(bb_pts[-1], bb4_top).color.set(color=YELLOW, alpha=0.7).r
        arrow_up = Arrow(
            bb4_top, bb4_top + UP * 0.8,
            color=YELLOW, buff=0,
        )
        text_bb5_val = TypstMath("\"BB\"(5) = 47176870").points.scale(1.2).r
        text_bb5_val.astype(VItem).color.set(color=YELLOW)
        text_bb5_val.points.next_to(arrow_up, LEFT, buff=0.3)

        self.play(Write(line_vert), Write(arrow_up), duration=0.75)
        self.play(Write(text_bb5_val), duration=0.5)
        self.forward(1.5)

        self.play(FadeOut(Group(
            axes, bb_dots, bb_lines, label_bb,
            line_vert, arrow_up, text_bb5_val,
            *seq_groups.values(), *seq_labels.values(),
        )))
        self.forward(0.5)

class s4_3(Timeline):
    """
    uv run janim run s4_ConcreteComparison.py s4_3 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        text_calculable = Text("可计算", font=local_font, color=WHITE)
        text_calculable.points.scale(1.5)
        text_definable = Text("可定义", font=local_font, color=WHITE)
        text_definable.points.scale(1.5).next_to(text_calculable, DOWN, buff=0.5)
        Group(text_calculable, text_definable).points.move_to(ORIGIN)
        rec_calculable = SurroundingRect(text_calculable, depth=10)
        rec_calculable.color.set(color=RED, alpha=1)
        rec_definable = SurroundingRect(text_definable, depth=10)
        rec_definable.color.set(color=GREEN, alpha=1)
        group_calculable = Group(text_calculable, rec_calculable)
        group_definable = Group(text_definable, rec_definable)
        list_seq_an = [
            "1", "2", "3", "4", "5", "6", "7", "8", "...",
            "0", "2", "6", "12", "20", "30", "42", "56", "...",
        ]
        table_seq_an = Group.from_iterable(
            TypstMath(item).points.scale(1.1).r for item in list_seq_an
        ).points.arrange_in_grid(
            n_rows=2, n_cols=9,
            h_buff=0.75, v_buff=0.25,
            aligned_edge=LEFT,
        ).r
        group_seq_n = Group.from_iterable(table_seq_an[0:9])
        group_seq_an = Group.from_iterable(table_seq_an[9:])
        group_seq_an.astype(VItem).color.set(color=BLUE)
        group_seq_an.astype(VItem).color.set(color=YELLOW)
        text_seq_n = TypstMath("n").points.scale(1.1).r
        text_seq_an = TypstMath("f(n)=n^2-n").points.scale(1.1).r
        text_seq_an.astype(VItem).color.set(color=YELLOW)
        Group(text_seq_n, text_seq_an).points.arrange(DOWN, buff=0.25, aligned_edge=LEFT) \
            .next_to(table_seq_an, LEFT, buff=0.75)
        Group(table_seq_an, text_seq_n, text_seq_an).points.move_to(DOWN * 0.5)
        group_example = Group(group_seq_n[2], group_seq_an[2])
        rect_example = SurroundingRect(group_example, color=CYAN, buff=0.25)

        self.play(
            Write(text_calculable),
            Transform(
                Rect(0.01, rec_calculable.points.box.height) \
                    .points.move_to(rec_calculable.points.box.left).r,
                rec_calculable,
            ),
        )
        self.forward(0.5)
        self.play(
            Write(text_definable),
            Transform(
                Rect(0.01, rec_definable.points.box.height) \
                    .points.move_to(rec_definable.points.box.left).r,
                rec_definable,
            ),
        )
        self.forward(2)
        self.play(
            group_calculable.anim.points.move_to(LEFT * 5.5 + UP * 3.25),
            group_definable.anim.points.move_to(LEFT * 3.5 + UP * 3.25),
            self.camera.anim.points.shift(DOWN * 0.25),
        )
        self.play(Write(group_seq_n), Write(text_seq_n))
        self.play(Write(group_seq_an), Write(text_seq_an))
        self.forward(1.5)

        data_1_original = ["...", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "..."]
        data_2_write_n = ["...", "0", "0", "0", "1", "1", "0", "0", "0", "0", "0", "0", "0", "..."]
        data_3_write_an = ["...", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "0", "..."]
        data_4_clear_all = ["...", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "..."]
        tapes = [
            Group.from_iterable(
                TapeCell(square_size=1, tile_data=data)
                for data in datas
            ).points.arrange(RIGHT, buff=0).move_to(DOWN * 2).r
            for datas in [data_1_original, data_2_write_n, data_3_write_an, data_4_clear_all]
        ]
        tape_center_idx = 4
        tape_frame = SVGItem("turing_machine/svgs/choice_frame.svg")
        tape_frame.points.scale(0.35).move_to(tapes[0][tape_center_idx].points.box.center).r
        grid_chain_n = Group.from_iterable(
            GridCell(
                state_name=f"A<fs 0.6>{i}</fs>",
                write_bit="1",
                move_dir="RIGHT",
            ) for i in range(1, 3)
        ).points.arrange(RIGHT, buff=0.1).to_border(LEFT).shift(UP * 1).r
        brace_grid_chain_n = Brace(grid_chain_n, UP)
        label_grid_chain_n = TypstText("$ceil(log_2 n)$ 个").points.scale(1.25).next_to(brace_grid_chain_n, UP).r
        grid_chain_fn = Group.from_iterable(
            GridCell(
                state_name=name,
                write_bit="1",
                move_dir="RIGHT",
            ) for i, name in enumerate(
                ["F<fs 0.6>1</fs>", "F<fs 0.6>2</fs>", "F<fs 0.6>3</fs>", "...", "F<fs 0.6>m</fs>"]
            )
        ).points.arrange(RIGHT, buff=0.1).next_to(grid_chain_n, RIGHT, buff=0.75).r
        brace_grid_chain_fn = Brace(grid_chain_fn, UP)
        label_grid_chain_fn = TypstText("常数 $F_m$ 个").points.scale(1.25).next_to(brace_grid_chain_fn, UP).r
        label_grid_chain_fn["$F_m$"].astype(VItem).color.set(color=ORANGE)
        grid_chain_constant = Group.from_iterable(
            GridCell(
                state_name=f"C<fs 0.6>{i}</fs>",
                write_bit="0",
                move_dir="LEFT" if i < 3 else "STOP",
            ) for i in range(3)
        ).points.arrange(RIGHT, buff=0.1).next_to(grid_chain_fn, RIGHT, buff=0.75).r
        brace_grid_chain_constant = Brace(grid_chain_constant, UP)
        label_grid_chain_constant = TypstText("常数 $c$ 个").points.scale(1.25).next_to(brace_grid_chain_constant, UP).r
        label_grid_chain_constant["$c$"].astype(VItem).color.set(color=ORANGE)
        brace_tape_n = Brace(tapes[1][tape_center_idx:tape_center_idx + 2], DOWN)
        brace_tape_an = Brace(tapes[1][tape_center_idx + 2:tape_center_idx + 8], DOWN)
        label_tape_n = TypstMath("n=3 \\\n ceil(log_2 n)=2").points.scale(1.3).next_to(brace_tape_n, DOWN, buff=0.2).r
        label_tape_an = TypstMath("a_n=6").points.scale(1.3).next_to(brace_tape_an, DOWN, buff=0.2).r
        label_tape_an.astype(VItem).color.set(color=YELLOW)

        self.play(
            Write(tapes[0]),
            Write(tape_frame),
        )
        self.play(Write(rect_example))
        self.forward(1.5)
        self.play(
            Write(grid_chain_n),
            Write(brace_grid_chain_n),
            Write(label_grid_chain_n),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            Succession(
                TransformMatchingShapes(
                    tapes[0][tape_center_idx],
                    tapes[1][tape_center_idx],
                ),
                tape_frame.anim.points.move_to(tapes[1][tape_center_idx + 1]),
                TransformMatchingShapes(
                    tapes[0][tape_center_idx + 1],
                    tapes[1][tape_center_idx + 1],
                ),
                duration=1,
            )
        )
        self.play(
            Write(brace_tape_n),
            Write(label_tape_n),
            lag_ratio=0.2,
        )
        self.forward(2)
        self.play(
            Write(grid_chain_fn), 
            Write(brace_grid_chain_fn),
            Write(label_grid_chain_fn),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            Succession(
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 2]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 2],
                    tapes[2][tape_center_idx + 2],
                ),
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 3]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 3],
                    tapes[2][tape_center_idx + 3],
                ),
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 4]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 4],
                    tapes[2][tape_center_idx + 4],
                ),
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 5]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 5],
                    tapes[2][tape_center_idx + 5],
                ),
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 6]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 6],
                    tapes[2][tape_center_idx + 6],
                ),
                tape_frame.anim.points.move_to(tapes[2][tape_center_idx + 7]),
                TransformMatchingShapes(
                    tapes[1][tape_center_idx + 7],
                    tapes[2][tape_center_idx + 7],
                ),
                duration=1.5,
            )
        )
        self.play(
            Write(brace_tape_an),
            Write(label_tape_an),
            lag_ratio=0.2,
        )
        self.forward(2)
        self.play(
            Write(grid_chain_constant),
            Write(brace_grid_chain_constant),
            Write(label_grid_chain_constant),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            TransformMatchingShapes(
                tapes[2][tape_center_idx + 7],
                tapes[3][tape_center_idx + 7],
            ),
            duration=0.5,
        )
        for i in range(6, -1, -1):
            self.play(
                Succession(
                    tape_frame.anim.points.move_to(tapes[3][tape_center_idx + i]),
                    TransformMatchingShapes(
                        tapes[2][tape_center_idx + i],
                        tapes[3][tape_center_idx + i],
                    ),
                    duration=0.5,
                )
            )
        self.forward(2)

        text_steps = TypstText("运行步数 $>= overbrace(f(n), \"Write\")+overbrace(f(n), \"Clear\")$")
        text_steps.points.scale(1.25).move_to(DOWN * 3)
        text_steps["$f(n)$", ...].astype(VItem).color.set(color=YELLOW)
        text_steps_2 = TypstText("运行步数 $\"steps\">= 2f(n)$")
        text_steps_2.points.scale(1.25).move_to(DOWN * 3)
        text_steps_2["$f(n)$"].astype(VItem).color.set(color=YELLOW)
        text_steps_2["$\"steps\"$"].astype(VItem).color.set(color=BLUE_B)
        brace_all_states = Brace(Group(grid_chain_n, grid_chain_fn, grid_chain_constant), UP)
        label_all_states = TypstText("共 $ceil(log_2 n)+F_m+c$ 个状态").points.scale(1.25).next_to(brace_all_states, UP).r
        label_all_states["$F_m$"].astype(VItem).color.set(color=ORANGE)
        label_all_states["$c$"].astype(VItem).color.set(color=ORANGE)
        label_all_states_2 = TypstText("共 $log_2 n+F_m+c$ 个状态").points.scale(1.25).next_to(brace_all_states, UP).r
        label_all_states_2["$F_m$"].astype(VItem).color.set(color=ORANGE)
        label_all_states_2["$c$"].astype(VItem).color.set(color=ORANGE)
        label_all_states_3 = TypstText("共 $log_2 n+C$ 个状态").points.scale(1.25).next_to(brace_all_states, UP).r
        label_all_states_3["$C$"].astype(VItem).color.set(color=ORANGE)
        text_most_bb = TypstText("共 $log_2 n+C$ 个状态 $=>$ 该图灵机步数一定不超过 $\"BB\"(log_2 n + C)$")
        text_most_bb.points.scale(1.25).next_to(brace_all_states, UP)
        text_most_bb["$C$", ...].astype(VItem).color.set(color=ORANGE)
        text_most_bb["步数"].astype(VItem).color.set(color=BLUE_B)
        text_bb_ge_bb_log = TypstMath("\"BB\"(n) >= \"BB\"(log_2 n + C)").points.scale(1.25).move_to(DOWN * 3 + LEFT * 3).r
        text_bb_ge_bb_log["C"].astype(VItem).color.set(color=ORANGE)
        rec_running_steps = SurroundingRect(text_steps_2["运行步数 $\"steps\"$"], color=BLUE_B)
        rec_bb_log2n_plus_C = SurroundingRect(text_bb_ge_bb_log["\"BB\"(log_2 n + C)"], color=BLUE_B)
        text_bb_ge_2f = TypstMath("\"BB\"(n) >= \"BB\"(log_2 n + C) >= 2f(n)")
        text_bb_ge_2f["C"].astype(VItem).color.set(color=ORANGE)
        text_bb_ge_2f["f"].astype(VItem).color.set(color=YELLOW)
        text_bb_ge_2f.points.scale(1.5).move_to(text_steps_2)

        Group(tapes[0][4:12], tapes[1][4:12]).hide()
        self.play(
            FadeOut(Group(group_seq_n, group_seq_an, text_seq_n, text_seq_an, rect_example)),
            Group(
                tapes[0][0:4], tapes[3][4:12], tapes[0][12:],
                tape_frame,
                brace_tape_n, brace_tape_an, label_tape_n, label_tape_an,
            ).anim.points.move_to(DOWN * 1),
        )
        self.forward(1)
        self.play(Write(text_steps))
        self.forward(1)
        self.play(TransformMatchingDiff(text_steps, text_steps_2))
        self.forward(1)
        self.play(
            Transform(
                Group(brace_grid_chain_n, brace_grid_chain_fn, brace_grid_chain_constant),
                Group(brace_all_states),
            )
        )
        self.play(
            FadeOut(Group(
                label_grid_chain_n["个"],
                label_grid_chain_fn["常数"],
                label_grid_chain_fn["个"],
                label_grid_chain_constant["常数"],
                label_grid_chain_constant["个"],
            )),
            AnimGroup(
                TransformMatchingDiff(
                    label_grid_chain_n["$ceil(log_2 n)$"],
                    label_all_states["$ceil(log_2 n)$"],
                    path_arc=PI / 2,
                ),
                TransformMatchingDiff(
                    label_grid_chain_fn["$F_m$"],
                    label_all_states["$F_m$"],
                    path_arc=PI / 2,
                ),
                TransformMatchingDiff(
                    label_grid_chain_constant["$c$"],
                    label_all_states["$c$"],
                    path_arc=PI / 2,
                ),
            ),
            FadeIn(Group(
                label_all_states["$+$", ...],
                label_all_states["共"],
                label_all_states["个状态"],
            )),
            lag_ratio=0.3,
            duration=2,
        )
        self.forward(1)
        self.play(TransformMatchingDiff(label_all_states, label_all_states_2))
        self.forward(1)
        self.play(TransformMatchingDiff(label_all_states_2, label_all_states_3))
        self.forward(1)
        self.play(TransformMatchingDiff(label_all_states_3, text_most_bb))
        self.forward(1)

        # region 坐标轴动画
        axe_comparison = Axes(
            x_range=(0, 5, 1),
            y_range=(0, 5, 1),
            x_length=7,
            y_length=6,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "include_numbers": True,
            }
        )
        axe_comparison.points.move_to(DOWN * 1)
        axe_comparison(VItem).color.set(alpha=0.5)
        axes_labels = axe_comparison.get_axis_labels(x_label="n", y_label="f(n)")
        axes_labels[0].points.shift(DOWN * 0.75)
        axes_labels[1].points.shift(LEFT * 1.5 + DOWN * 0.5)
        axes_labels(VItem).fill.set(alpha=0.5)
        graph_n = axe_comparison.get_graph(lambda x: x, color=GREEN_A)
        label_n = TypstMath("n")
        label_n(VItem).fill.set(color=GREEN_A)
        label_n.points.next_to(axe_comparison.coords_to_point(5, 5), RIGHT, buff=0.2)
        graph_log2n = axe_comparison.get_graph(
            lambda x: math.log2(x) if x > 0.001 else -10,
            color=BLUE_A,
            x_range=(0.001, 5, 0.001),
        )
        label_log2n = TypstMath("log_2 n")
        label_log2n(VItem).fill.set(color=BLUE_A)
        label_log2n.points.next_to(axe_comparison.coords_to_point(5, math.log2(5)), RIGHT, buff=0.2)
        graph_log2n_plus_2 = axe_comparison.get_graph(
            lambda x: math.log2(x) + 2 if x > 0.001 else -10,
            color=BLUE_A,
            x_range=(0.001, 5, 0.001),
        )
        label_log2n_plus_2 = TypstMath("log_2 n + 2")
        label_log2n_plus_2(VItem).fill.set(color=BLUE_A)
        label_log2n_plus_2.points.next_to(axe_comparison.coords_to_point(5, math.log2(5) + 2), RIGHT, buff=0.2)
        intersection_log2n_p2_with_n = axe_comparison.coords_to_point(4, 4)
        intersection_log2n_p2_with_n_right = axe_comparison.coords_to_point(5, 4)
        brace_log_2n_p2_with_n = Brace(
            Line(intersection_log2n_p2_with_n, intersection_log2n_p2_with_n_right),
        )
        brace_log_2n_p2_with_n_label = brace_log_2n_p2_with_n.points.create_typst("n > log_2 n + 2")

        self.play(
            FadeOut(Group(
                text_most_bb, brace_all_states,
                grid_chain_n, grid_chain_fn, grid_chain_constant,
                tapes[0][0:4], tapes[3][4:12], tapes[0][12:], tape_frame,
                brace_tape_n, brace_tape_an,
                label_tape_n, label_tape_an,
                text_steps_2,
            ))
        )
        self.play(
            self.camera.anim.points.shift(DOWN * 1),
            # FadeOut(Group(grid_chain_n, grid_chain_fn, grid_chain_constant)),
            # Group(rect_n_1, rect_n_2, rect_c, text_bb_ge_2f).anim.points.shift(UP * 2.25),
            Write(axe_comparison),
            Write(axes_labels),
        )
        self.play(
            Succession(
                Write(Group(graph_n, label_n)),
                Write(Group(graph_log2n, label_log2n)),
            )
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(label_log2n, label_log2n_plus_2, duration=1.5),
            Transform(graph_log2n, graph_log2n_plus_2, duration=1.5),
        )
        self.forward(1)
        self.play(
            Write(brace_log_2n_p2_with_n),
            Write(brace_log_2n_p2_with_n_label),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            FadeOut(Group(
                brace_log_2n_p2_with_n, brace_log_2n_p2_with_n_label,
            ))
        )

        axe_comparison_2 = Axes(
            x_range=(0, 10, 1),
            y_range=(0, 10, 1),
            x_length=7,
            y_length=6,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "include_numbers": True,
            }
        )
        axe_comparison_2.points.move_to(axe_comparison)
        axe_comparison_2(VItem).color.set(alpha=0.5)
        graph_n_2 = axe_comparison_2.get_graph(lambda x: x, color=GREEN_A)
        label_n_2 = TypstMath("n")
        label_n_2(VItem).fill.set(color=GREEN_A)
        label_n_2.points.next_to(axe_comparison_2.coords_to_point(10, 10), RIGHT, buff=0.2)
        graph_log2n_plus_2_2 = axe_comparison_2.get_graph(
            lambda x: math.log2(x) + 2 if x > 0.001 else -10,
            color=BLUE_A,
            x_range=(0.001, 10, 0.01),
        )
        label_log2n_plus_2_2 = TypstMath("log_2 n + 2")
        label_log2n_plus_2_2(VItem).fill.set(color=BLUE_A)
        label_log2n_plus_2_2.points.next_to(axe_comparison_2.coords_to_point(10, math.log2(10) + 2), RIGHT, buff=0.2)
        graph_log2n_plus_6_2 = axe_comparison_2.get_graph(
            lambda x: math.log2(x) + 6 if x > 0.001 else -10,
            color=BLUE_A,
            x_range=(0.001, 10, 0.01),
        )
        label_log2n_plus_6_2 = TypstMath("log_2 n + 6")
        label_log2n_plus_6_2(VItem).fill.set(color=BLUE_A)
        label_log2n_plus_6_2.points.next_to(axe_comparison_2.coords_to_point(10, math.log2(10) + 6), RIGHT, buff=0.2)
        intersection_log2n_p6_with_n = axe_comparison_2.coords_to_point(9.20194, 9.20194)
        intersection_log2n_p2_with_n_right = axe_comparison_2.coords_to_point(10, 9.20194)
        brace_log_2n_p6_with_n = Brace(
            Line(intersection_log2n_p6_with_n, intersection_log2n_p2_with_n_right),
        )
        brace_log_2n_p6_with_n_label = brace_log_2n_p6_with_n.points.create_typst("n > log_2 n + 6")

        self.play(
            TransformMatchingShapes(axe_comparison, axe_comparison_2, path_arc=PI / 2, duration=2),
            Transform(graph_n, graph_n_2, duration=2),
            Transform(label_n, label_n_2, duration=2),
            TransformMatchingDiff(label_log2n_plus_2, label_log2n_plus_2_2, duration=2),
            Transform(graph_log2n_plus_2, graph_log2n_plus_2_2, duration=2),
        )
        self.forward(1.5)
        self.play(
            Transform(graph_log2n_plus_2_2, graph_log2n_plus_6_2, duration=1.5),
            TransformMatchingDiff(label_log2n_plus_2_2, label_log2n_plus_6_2, duration=1.5),
        )
        self.forward(1)
        self.play(
            Write(brace_log_2n_p6_with_n),
            Write(brace_log_2n_p6_with_n_label),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(FadeOut(Group(
            brace_log_2n_p6_with_n, brace_log_2n_p6_with_n_label,
        )))

        axe_comparison_3 = Axes(
            x_range=(0, 100, 10),
            y_range=(0, 100, 10),
            x_length=7,
            y_length=6,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "include_numbers": True,
            }
        )
        axe_comparison_3.points.move_to(axe_comparison_2)
        axe_comparison_3(VItem).color.set(alpha=0.5)
        graph_n_3 = axe_comparison_3.get_graph(lambda x: x, color=GREEN_A)
        label_n_3 = TypstMath("n")
        label_n_3(VItem).fill.set(color=GREEN_A)
        label_n_3.points.next_to(axe_comparison_3.coords_to_point(100, 100), RIGHT, buff=0.2)
        graph_log2n_plus_6_3 = axe_comparison_3.get_graph(
            lambda x: math.log2(x) + 6 if x > 0.001 else -10,
            color=BLUE_A,
            x_range=(0.001, 100, 0.001),
        )
        label_log2n_plus_6_3 = TypstMath("log_2 n + 6")
        label_log2n_plus_6_3(VItem).fill.set(color=BLUE_A)
        label_log2n_plus_6_3.points.next_to(axe_comparison_3.coords_to_point(100, math.log2(100) + 6), RIGHT, buff=0.2)
        text_n_ge_log2n = TypstText("对于足够大的 $n$ \\\n$n > log_2 n + C$")
        text_n_ge_log2n.points.scale(1.25).move_to(RIGHT * 4 + DOWN * 1)
        text_n_ge_log2n["$C$"].astype(VItem).color.set(color=ORANGE)
        text_n_ge_log2n["$n$", 1].astype(VItem).color.set(color=GREEN_A)
        text_n_ge_log2n["$log_2 n$"].astype(VItem).color.set(color=BLUE_A)
        rec_group_1 = Group(
            SurroundingRect(text_n_ge_log2n["$n$", 1], color=GREEN_A),
            SurroundingRect(text_n_ge_log2n["$log_2 n + C$"], color=BLUE_A),
        )
        text_bb_n_ge_bb_log2n = TypstText("对于足够大的 $n$ \\\n$\"BB\"(n) > \"BB\"(log_2 n + C)$")
        text_bb_n_ge_bb_log2n.points.scale(1.25).move_to(text_n_ge_log2n)
        text_bb_n_ge_bb_log2n["$C$"].astype(VItem).color.set(color=ORANGE)
        text_bb_n_ge_bb_log2n["$n$", 1].astype(VItem).color.set(color=GREEN_A)
        text_bb_n_ge_bb_log2n["$log_2 n$"].astype(VItem).color.set(color=BLUE_A)
        rec_group_2 = Group(
            SurroundingRect(text_bb_n_ge_bb_log2n["$n$", 1], color=GREEN_A, buff=0.05),
            SurroundingRect(text_bb_n_ge_bb_log2n["$log_2 n + C$"], color=BLUE_A, buff=0.05),
        )

        def intersection_position_sol_with_c(c: float):
            """交点坐标随着 C 变化的情况，帕德展开"""
            x = c
            if x <= 50:
                final = (2175.08 - 8445.36 * x - 5101.48 * x ** 2 + 30152. * x ** 3 - 8508.27 * x ** 4 \
                        - 11088.3 * x ** 5 - 1109.61 * x ** 6) / (323.731 - 5216.47 * x + 8535.71 * x ** 2 \
                        + 2837.12 * x ** 3 - 6406.35 * x ** 4 - 1035.45 * x ** 5 - 1. * x ** 6)
            else:
                final = (5.441380144053301e11 + 3.5143912338124725e11 * x + 8.882157939136904e9 * x ** 2 + 
                        2.4985369276173228e8 * x ** 3 + 375085.5264803801 * x ** 4 + 29261.98128528243 * x ** 5 - 
                        316.45751520221734 * x ** 6) / (2.617571874508069e11 + 9.591097502383093e9 * x + 1.746713728786957e8 * x ** 2 + 
                        1.7921879588214043e6 * x ** 3 + 6307.78304394071 * x ** 4 - 84.51166760997418 * x ** 5 - 1. * x ** 6)
            return axe_comparison_3.coords_to_point(final, final), axe_comparison_3.coords_to_point(100, final)
        
        def get_brace(c: float):
            it = intersection_position_sol_with_c(c)
            line = Line(*it)
            brace = Brace(line, UP)
            brace.points.shift(UP * 0.2)
            return brace
        def get_label(c: float, brace: Brace):
            label = brace.points.create_typst(f"n > log_2 n + {c:.0f}")
            return label
        def get_graph(c: float):
            graph = axe_comparison_3.get_graph(
                lambda x: math.log2(x) + c if x > 0.001 else -10,
                color=BLUE_A,
                x_range=(0.001, 100, 0.001),
            )
            return graph
        def get_graph_label(c: float):
            label = TypstMath(f"log_2 n + {c:.0f}")
            label(VItem).fill.set(color=BLUE_A)
            label.points.next_to(axe_comparison_3.coords_to_point(100, math.log2(100) + c), RIGHT, buff=0.2)
            return label
        
        brace_log_2n_pc_with_n = get_brace(6)
        brace_log_2n_pc_with_n_label = get_label(6, brace_log_2n_pc_with_n)
        
        self.play(
            TransformMatchingShapes(axe_comparison_2, axe_comparison_3, duration=2),
            Transform(graph_n_2, graph_n_3, duration=2),
            Transform(label_n_2, label_n_3, duration=2),
            Transform(graph_log2n_plus_6_2, graph_log2n_plus_6_3, duration=2),
            Transform(label_log2n_plus_6_2, label_log2n_plus_6_3, duration=2),
        )
        self.forward(1)
        self.play(
            Write(brace_log_2n_pc_with_n),
            Write(brace_log_2n_pc_with_n_label),
        )
        self.forward(0.5)
        alpha2c = lambda alpha: alpha * 74 + 6
        self.prepare(FadeOut(brace_log_2n_pc_with_n_label))
        self.play(
            ItemUpdater(
                graph_log2n_plus_6_3,
                lambda p: get_graph(alpha2c(p.alpha))
            ),
            ItemUpdater(
                label_log2n_plus_6_3,
                lambda p: get_graph_label(alpha2c(p.alpha))
            ),
            ItemUpdater(
                brace_log_2n_pc_with_n,
                lambda p: get_brace(alpha2c(p.alpha))
            ),
            duration=4,
        )
        self.forward(1.5)
        self.play(
            Write(text_n_ge_log2n),
        )
        self.play(Write(rec_group_1))
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_n_ge_log2n,
                text_bb_n_ge_bb_log2n,
                duration=1.5,
            ),
            Transform(
                rec_group_1,
                rec_group_2,
                duration=1.5,
            ),
        )
        self.play(
            FadeOut(rec_group_2),
        )
        self.forward(1.5)
        self.play(
            FadeOut(Group(
                axe_comparison_3, axes_labels,
                graph_log2n_plus_6_3, label_log2n_plus_6_3,
                graph_n_3, label_n_3,
                brace_log_2n_pc_with_n,
                text_bb_n_ge_bb_log2n,
            ))
        )
        self.play(
            FadeIn(Group(
                text_most_bb, brace_all_states,
                grid_chain_n, grid_chain_fn, grid_chain_constant,
                tapes[0][0:4], tapes[3][4:12], tapes[0][12:], tape_frame,
                brace_tape_n, brace_tape_an,
                label_tape_n, label_tape_an,
                text_steps_2,
            )),
            self.camera.anim.points.shift(UP * 1),
        )
        # endregion

        rec_running_steps.points.shift(RIGHT * 3)
        self.play(
            text_steps_2.anim.points.shift(RIGHT * 3),
            Write(text_bb_ge_bb_log),
        )
        self.forward(1)
        self.play(
            Write(rec_running_steps),
            Write(rec_bb_log2n_plus_C),
        )
        self.forward(0.5)
        self.play(
            FadeOut(rec_running_steps),
            FadeOut(rec_bb_log2n_plus_C),
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_steps_2["$>= 2f(n)$"],
                text_bb_ge_2f[">= 2f(n)"],
            ),
            TransformMatchingDiff(
                text_bb_ge_bb_log,
                text_bb_ge_2f["\"BB\"(n) >= \"BB\"(log_2 n + C)"],
            ),
            FadeOut(text_steps_2["运行步数 $\"steps\"$"]),
            FadeOut(brace_all_states),
            FadeOut(text_most_bb),
            Group(grid_chain_n, grid_chain_fn, grid_chain_constant).anim.points.shift(UP * 0.5),
        )
        self.play(
            FadeOut(Group(
                label_tape_n,
                label_tape_an,
                tapes[0][0:4], tapes[3][4:12], tapes[0][12:],
                brace_tape_an, brace_tape_n,
                tape_frame,
            )),
            FadeOut(Group(grid_chain_n, grid_chain_fn, grid_chain_constant)),
            text_bb_ge_2f.anim.points.move_to(ORIGIN),
            self.camera.anim.points.move_to(UP),
        )
        self.forward(1.5)

        rect_n_1 = SurroundingRect(
            text_bb_ge_2f["n", 0],
            color=GREEN_A,
            buff=0.05,
        )
        rect_n_2 = SurroundingRect(
            text_bb_ge_2f["log_2 n", 0],
            color=BLUE_A,
            buff=0.05,
        )
        rect_c = SurroundingRect(
            text_bb_ge_2f["C"],
            color=ORANGE,
            buff=0.05,
        )
        text_bb_ge_2f_ge_fnpc = TypstMath("\"BB\"(n) >= 2f(n)")
        text_bb_ge_2f_ge_fnpc["f", ...].astype(VItem).color.set(color=YELLOW)
        text_bb_ge_2f_ge_fnpc.points.scale(1.5).move_to(text_steps_2)
        text_bb_ge_fnpc = TypstMath("\"BB\"(n) >= f(n)")
        text_bb_ge_2f_ge_fnpc["f", ...].astype(VItem).color.set(color=YELLOW)
        text_bb_ge_fnpc.points.scale(1.5).move_to(text_steps_2)
        text_bb_ge_fnpc["f"].astype(VItem).color.set(color=YELLOW)
        text_bb_ge_fn = TypstMath("\"BB\"(n)>=f(n)").points.scale(1.5).move_to(text_steps_2).r
        text_bb_ge_fn["f"].astype(VItem).color.set(color=YELLOW)
        text_bb_gg_fn = TypstMath("\"BB\"(n) >> f(n)").points.scale(1.5).move_to(text_steps_2).r
        text_bb_gg_fn["f"].astype(VItem).color.set(color=YELLOW)
        text_bb_gg_fn[">>"].astype(VItem).color.set(color=RED)
        rec_bb_gg_fn = SurroundingRect(
            text_bb_gg_fn,
            color=RED,
            buff=0.25,
        )
        
        self.play(
            Write(rect_n_1),
            Write(rect_n_2),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(Write(rect_c))
        self.forward(1)



        self.play(FadeOut(Group(
            rect_n_1,
            rect_n_2,
            rect_c,
        )))
        self.forward(1)
        text_bb_ge_2f_ge_fnpc.points.move_to(ORIGIN)
        text_bb_ge_fnpc.points.move_to(ORIGIN)
        text_bb_ge_fn.points.move_to(ORIGIN)
        text_bb_gg_fn.points.move_to(ORIGIN)
        rec_bb_gg_fn.points.move_to(text_bb_gg_fn)
        self.play(
            FadeOut(text_bb_ge_2f[">= \"BB\"(log_2 n + C)"]),
            TransformMatchingDiff(
                Group(text_bb_ge_2f["\"BB\"(n)"], text_bb_ge_2f[">= 2f(n)"]),
                text_bb_ge_2f_ge_fnpc,
            ),
            lag_ratio=0.3,
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_bb_ge_2f_ge_fnpc,
                text_bb_ge_fnpc,
            )
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_bb_ge_fnpc,
                text_bb_ge_fn,
            )
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_bb_ge_fn,
                text_bb_gg_fn,
            ),
            Write(rec_bb_gg_fn),
        )
        self.forward(3)
        self.play(
            FadeOut(Group(
                text_bb_gg_fn, rec_bb_gg_fn,
                rec_calculable, rec_definable,
                text_calculable, text_definable,
            ))
        )
        self.forward(1)

class s4_4(Timeline):
    """
    uv run janim run s4_ConcreteComparison.py s4_4 -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        
        text_H = TypstMath("H").points.scale(1.5).r
        text_use_finite_steps_calc = Text(
            "可以用有限步骤进行计算",
            font=local_font,
            format="rich"
        ).points.scale(1.5).r
        Group(text_H, text_use_finite_steps_calc).points.arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        rec_finite_steps = SurroundingRect(
            text_use_finite_steps_calc[0][3:7],
            color=GREEN,
            buff=0,
            depth=10,
        ).color.set(alpha=1).r
        rec_finite_steps.points.set_height(rec_finite_steps.points.box.height * 1.2, stretch=True)
        rec_calculate = SurroundingRect(
            text_use_finite_steps_calc[0][9:],
            color=RED,
            buff=0,
            depth=10,
        ).color.set(alpha=1).r
        rec_calculate.points.set_height(rec_calculate.points.box.height * 1.2, stretch=True)

        self.play(Write(text_H))
        self.play(Write(text_use_finite_steps_calc))
        self.forward(1)
        self.play(
            Transform(
                Rect(0.01, rec_finite_steps.points.box.height) \
                    .points.move_to(rec_finite_steps.points.box.left).r,
                rec_finite_steps,
            ),
            Transform(
                Rect(0.01, rec_calculate.points.box.height) \
                    .points.move_to(rec_calculate.points.box.left).r,
                rec_calculate,
            ),
            lag_ratio=0.5
        )
        self.forward(2)
        self.play(Uncreate(Group(
            text_H,
            text_use_finite_steps_calc,
            rec_finite_steps,
            rec_calculate,
        )))
        self.forward(2)

        text_fastest = Text("增长最快数列", font=local_font).points.scale(1.5).r
        text_no_fastest = Text("不存在增长最快数列", font=local_font).points.scale(1.5).r
        rec_no_fastest = Rect(
            text_no_fastest[0][0:3].points.box.width,
            0.02,
            color=RED,
        ).points.move_to(text_no_fastest[0][0:3].points.box.bottom + DOWN * 0.05).r
        formulas = [
            "1", "alpha(n)", "log^(***)(n)", "log^(**)(n)", "log^*(n)", "log(log(log(log(n))))", "log(log(log(n)))", "log(log(n))", "sqrt(log(n))", "log(n)",
            "(log(n))^2", "(log(n))^3", "e^(sqrt(log(n)))", "n^(1/log(log(n)))", "n^0.1", "sqrt(n)", "n/log(n)", "n", "n log(n)", "n (log(n))^2",
            "n^1.5", "n^2", "n^3", "n^(log(log(n)))", "n^(log(n))", "e^(sqrt(n))", "n^(sqrt(n))", "e^(n/log(n))", "(sqrt(2))^n", "2^n",
            "e^n", "3^n", "n!", "n^n", "product_(k=1)^n k^k", "n^(n^2)", "2^(2^n)", "3^(3^n)", "e^(e^n)", "2^(2^(2^n))",
            "n^(n^n)", "n^(n^(n^n))", "2 arrow.t.double n", "3 arrow.t.double n", "n arrow.t.double n", "n arrow.t.double (n+1)", "2 arrow.t.triple n", "n arrow.t.triple n", "2 arrow.t^4 n", "n arrow.t^4 n",
            "n arrow.t^5 n", "A(n, n)", "A(n, A(n, n))", "f_(omega+1)(n)", "f_(omega+2)(n)", "f_(omega dot 2)(n)", "f_(omega dot 3)(n)", "f_(omega^2)(n)", "f_(omega^3)(n)", "f_(omega^omega)(n)",
            "n -> n -> n -> n", "n -> n -> n -> n -> 2", "n -> n -> n -> n -> 3", "n -> n -> n -> n -> n", "f_(omega^(omega^omega))(n)", "f_(epsilon_0)(n)", "G(n)", "f_(epsilon_0+1)(n)", "f_(epsilon_0+omega)(n)", "f_(epsilon_1)(n)",
            "f_(epsilon_2)(n)", "f_(epsilon_omega)(n)", "f_(epsilon_(epsilon_0))(n)", "f_(zeta_0)(n)", "f_(eta_0)(n)", "f_(Gamma_0)(n)", "f_(Gamma_1)(n)", "f_(Gamma_(Gamma_0))(n)", "f_(\"LVO\")(n)", "f_(\"BHO\")(n)",
            "\"TREE\"(n)", "f_(psi(Omega^(Omega^omega)))(n)", "\"SSCG\"(n)", "\"SCG\"(n)", "f_(psi_0(Omega_omega))(n)", "f_(psi_0(Omega_Omega))(n)",
        ]
        text_formulas = Group.from_iterable(
            TypstMath(formula)
            for formula in formulas
        )
        standard_width = text_no_fastest.points.box.width / 3 * 2
        for t in text_formulas:
            t.depth.set(10)
            t.points.scale(standard_width / t.points.box.width).move_to(ORIGIN)
            t.astype(VItem).color.set(color=GREY_A, alpha=0.2)
            t.astype(VItem).stroke.set(alpha=0)
        def get_formula_by_alpha(alpha: float):
            plateau: Callable[[float, float], float] = lambda x, e: \
                (t := max(0, min(1, x/e)))*t*(3-2*t) * (s := max(0, min(1, (1-x)/e)))*s*(3-2*s)
            last_idx = len(formulas) - 1
            idx = int(alpha * last_idx)
            transparent_beta = plateau(alpha, 0.05) * 0.06
            text_formulas[idx].astype(VItem).color.set(alpha=transparent_beta)
            return text_formulas[idx]
        text_2_pow_bb = TypstMath("2^\"BB\"(n)").points.scale(1.5).move_to(DOWN * 1).r
        text_2_pow_bb_gt_bb = TypstMath("2^\"BB\"(n) > \"BB\"(n)").points.scale(1.5).move_to(DOWN * 1).r
        video_bb = Video("resources/bb.mp4", depth=-10).points.scale(1.5).r

        self.prepare(
            ItemUpdater(
                get_formula_by_alpha(0),
                lambda p: get_formula_by_alpha(p.alpha),
            ),
            duration=16,
            rate_func=linear,
        )
        self.play(FadeIn(text_fastest))
        self.play(
            TransformMatchingDiff(text_fastest, text_no_fastest),
            Write(rec_no_fastest),
            duration=1.5,
        )
        self.forward(2)
        self.play(Write(text_2_pow_bb))
        self.forward(1)
        self.play(TransformMatchingDiff(text_2_pow_bb, text_2_pow_bb_gt_bb))
        video_bb.start()
        self.forward(2)
        self.play(FadeIn(video_bb))
        rec_no_fastest.hide()
        text_no_fastest.hide()
        text_2_pow_bb_gt_bb.hide()
        self.forward(5)
        self.play(FadeOut(video_bb))

        class BBLine(Timeline):
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
            def construct(self) -> None:
                def window_num(nums: Iterable[int], k: int):
                    return sorted(x + d for x in nums for d in range(-k, k + 1) if x + d > 0)
                group_text_bbs = NamedGroup(
                    **{
                        f"{n}": TypstMath(f"\"BB\"({n})").points.scale(1.5).r
                        for n in window_num([0, 15, 27, 744, 7918], k=20)
                    }
                ).points.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_border(LEFT + UP, buff=1).shift(RIGHT * 2).r
                for t in group_text_bbs:
                    t.astype(VItem).color.set(color=GREY_C)
                group_text_bbs["15"].astype(VItem).color.set(color=WHITE)
                group_text_bbs["27"].astype(VItem).color.set(color=WHITE)
                group_text_bbs["744"].astype(VItem).color.set(color=WHITE)
                group_text_bbs["7918"].astype(VItem).color.set(color=WHITE)
                text_erdos = TypstText("- #block[Erdős $2^n$ 三进制猜想 \\ Stérin & Woods]").points.scale(1.3).r
                text_goldbach = TypstText("- #block[Goldbach 猜想 \\ Aaronson 等]").points.scale(1.3).r
                text_riemann = TypstText("- #block[Riemann 猜想 \\ Aaronson 等]").points.scale(1.3).r
                text_ZFC_independent = TypstText("- #block[ZFC 独立性验证 \\ Yedidia & Aaronson]").points.scale(1.3).r
                text_erdos.points.next_to(group_text_bbs["15"], RIGHT, aligned_edge=UP, buff=0.75)
                text_goldbach.points.next_to(group_text_bbs["27"], RIGHT, aligned_edge=UP, buff=0.75)
                text_riemann.points.next_to(group_text_bbs["744"], RIGHT, aligned_edge=UP, buff=0.75)
                text_ZFC_independent.points.next_to(group_text_bbs["7918"], RIGHT, aligned_edge=UP, buff=0.75)
                group_all_bbs = Group(
                    group_text_bbs,
                    text_erdos, text_goldbach, text_riemann, text_ZFC_independent,
                )

                self.play(FadeIn(group_text_bbs))
                self.forward(1)
                self.play(
                    group_all_bbs.anim.points.shift(
                        group_text_bbs["5"].points.box.left - group_text_bbs["15"].points.box.left
                    ),
                    duration=2,
                )
                self.forward(0.5)
                self.play(
                    group_all_bbs.anim.points.shift(
                        group_text_bbs["15"].points.box.left - group_text_bbs["27"].points.box.left
                    ),
                    rate_func=ease_inout_cubic,
                    duration=1.5,
                )
                self.forward(0.5)
                self.play(
                    group_all_bbs.anim.points.shift(
                        group_text_bbs["27"].points.box.left - group_text_bbs["744"].points.box.left
                    ),
                    rate_func=ease_inout_cubic,
                    duration=1,
                )
                self.forward(0.5)
                self.play(
                    group_all_bbs.anim.points.shift(
                        group_text_bbs["744"].points.box.left - group_text_bbs["7918"].points.box.left
                    ),
                    rate_func=ease_inout_cubic,
                    duration=1,
                )
                self.forward(2)
                self.play(FadeOut(group_all_bbs))

        timeline_bb_line = BBLine().build().to_item().show()
        clip_bb_line = TransformableFrameClip(timeline_bb_line).show()
        effect_bb_line = LensEffect(
            clip_bb_line,
            lens_strength=0.75,
            lens_radius=1.75,
        ).show()
        self.forward(12)
        self.forward(1)

        class BBLine2(Timeline):
            CONFIG = Config(
                typst_shared_preamble=get_typ_doc("preamble")
            )
            def construct(self) -> None:
                w = 0.06
                lh = 0.05
                k = 8
                lens = 8
                pieces = 100
                exp_map = lambda x: 1 - 1 / (1 + x) ** k
                ratio = exp_map(6 / pieces)
                rect_green = Rect(lens * ratio, w, color=GREEN, depth=-10)
                rect_green.fill.set(alpha=1)
                rect_green.stroke.set(alpha=0)
                rect_red = Rect(lens * (1 - ratio), w, color=RED, depth=-10)
                rect_red.fill.set(alpha=1)
                rect_red.stroke.set(alpha=0)
                rect_group = Group(rect_green, rect_red).points.arrange(RIGHT, buff=0).move_to(DOWN * 0.5).r
                s1 = rect_group.points.box.left + UP * w / 2
                s2 = rect_group.points.box.right + UP * w / 2
                smid = rect_green.points.box.right + UP * w / 2
                lines = Group.from_iterable(
                    Line(
                        start=s2 * p + (1 - p) * s1,
                        end=s2 * p + (1 - p) * s1 + UP * lh,
                        color=GREY_B,
                        depth=10,
                    ).radius.set(radius=0.01).r
                    for p in exp_map(np.linspace(0, 1, pieces))
                )
                group_axes = Group(
                    rect_group,
                    lines,
                )
                triangle_pointer = Triangle()
                triangle_pointer.points.rotate(PI).scale(0.1).move_to(s1, aligned_edge=DOWN)
                triangle_pointer.radius.set(radius=0.01)
                triangle_pointer.color.set(color=WHITE, alpha=1)
                text_bb_x = TypstMath("")
                text_quote = TypstText("对于不可言说之物，\\ 我们必须保持沉默。\n\n$quad quad$—— Ludwig Wittgenstein", depth=-20)
                text_quote.points.scale(1.5).move_to(RIGHT * 0.5)

                self.play(Write(group_axes))
                self.forward(0.5)
                self.play(Write(triangle_pointer))
                self.play(
                    DataUpdater(
                        triangle_pointer,
                        lambda item, p: item.points.move_to(smid * p.alpha + (1 - p.alpha) * s1, aligned_edge=DOWN)
                    ),
                    ItemUpdater(
                        text_bb_x,
                        lambda p: TypstMath(f"\"BB\"({int(p.alpha * 6 + 0.01)})") \
                            .points.scale(0.75).next_to(triangle_pointer.current(), UP, buff=0.1).r
                    ),
                    duration=2,
                    rate_func=ease_inout_cubic,
                )
                self.forward(2)
                self.play(
                    AnimGroup(
                        rect_red.anim.points.set_height(20, stretch=True),
                        rect_red.anim.points.set_width(20, stretch=True),
                    ),
                    rect_red.anim.color.set(BLUE_B),
                    Write(text_quote),
                    duration=3,
                    lag_ratio=0.5,
                )
                self.forward(2)
                

        timeline_bb_line_2 = BBLine2().build().to_item().show()
        clip_bb_line_2 = TransformableFrameClip(timeline_bb_line_2).show()
        effect_bb_line_2 = LensEffect(
            clip_bb_line_2,
            lens_strength=0.85,
            lens_radius=1.75,
        ).show()
        self.forward(9)
        self.play(DataUpdater(
            effect_bb_line_2,
            lambda item, p: item.apply_uniforms_set(lens_strength=0.85 * (1 - p.alpha))
        ))
        self.forward(2)