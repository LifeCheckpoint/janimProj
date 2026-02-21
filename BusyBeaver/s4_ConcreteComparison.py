from janim.imports import * # type: ignore
from tools import (
    get_typ_doc,
    local_font,
    parse_rule_to_core,
    CYAN,
)
from turing_machine.components.tape_cell import TapeCell
from turing_machine.logic.turingcore import TuringMachineCore
from turing_machine.turing_machine import TuringMachine
from turing_machine.components.grid_cell import GridCell
from turing_machine.components.grid_table import GridTable, Transition
from langton_ant.langton_ant_grid import LangtonAntGrid
from dirty_patch import install_dirty_patch
import random
import math

class s4_1(Timeline):
    """
    uv run janim run s4_ConcreteComparison.py s4_1 -i
    """
    def construct(self) -> None:
        install_dirty_patch()
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
        rec_collatz_q = SurroundingRect(
            text_halt_implies_collatz["不停机 $=>$ Collatz 猜想成立"],
            color=YELLOW,
            depth=10,
        )
        rec_collatz_q.fill.set(alpha=0.25)
        rec_bb6 = SurroundingRect(
            text_bb6_ge["\"BB\"_6"],
            color=GREY_B,
        )
        text_S_step = TypstText("$S$ steps").points.scale(1.5).r
        text_S_step.points.next_to(rec_bb6, DOWN, buff=0.25)
        text_S_step.astype(VItem).color.set(color=GREY_B)
        def step_compress(alpha: float, to_step: int = 1000000, k: float = 10000000):
            _s = to_step * math.log(1 + to_step * alpha) / math.log(1 + k)
            return int(np.clip(_s, 1, to_step))
        def get_hc_step_text(
            step: int,
            next_to: VItem | None = None,
            final_S: int = 500000,
            ellipsis_threshold: int = 7,
            scaling_coeff: float = 0.8,
        ):
            step_text = str(step)
            if len(step_text) > ellipsis_threshold:
                step_text = f"{step_text[:ellipsis_threshold // 2]}...{step_text[-ellipsis_threshold // 2:]}"
            t = f"{step_text} \"steps\" " + ("<= " if step <= final_S else "> ") + "S"
            text = TypstMath(t).points.scale(1.75).r
            text[f"{step_text} \"steps\""].astype(VItem).color.set(color=GREEN_C)
            text["S"].astype(VItem).color.set(color=GREY_B)
            if step <= final_S:
                text["<= "].astype(VItem).color.set(color=WHITE)
            else:
                text["> "].astype(VItem).color.set(color=RED_A)
            if next_to is not None:
                text.points.next_to(next_to, UP, buff=0.5)
            return text
        text_Hc_steps = get_hc_step_text(0, next_to=rect_Hc)
        
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
        self.play(Write(text_Hc_steps))
        self.forward(0.5)
        self.play(
            ItemUpdater(
                text_Hc_steps,
                lambda p: get_hc_step_text(
                    step=step_compress(p.alpha, to_step=10000000, k=10**65),
                    next_to=rect_Hc,
                    final_S=1000000,
                    ellipsis_threshold=6,
                )
            ),
            duration=5.0,
        )
        
        rec_ge = SurroundingRect(
            text_Hc_steps["> S"],
            color=RED_A,
        )
        text_no_halt = Text("不停机", font=local_font, color=RED_A)
        text_no_halt.points.scale(1.5).next_to(rec_ge, UP, buff=0.25)

        self.play(
            Write(rec_ge),
            Write(text_no_halt),
        )
        self.forward(0.5)
        self.play(Write(rec_collatz_q))
        self.forward(2)

        text_bb6_ge_collatz = TypstText("Difficulty of $\"BB\"(6) >=$ Collatz conjecture")
        text_bb27_ge_goldbach = TypstText("Difficulty of $\"BB\"(27) >=$ Goldbach's conjecture")
        text_bb744_ge_riemann = TypstText("Difficulty of $\"BB\"(744) >=$ Riemann conjecture")
        group_ges = Group()
        for t, step in zip(
            [text_bb6_ge_collatz, text_bb27_ge_goldbach, text_bb744_ge_riemann],
            [6, 27, 744],
        ):
            t.points.scale(1.25)
            t[f"$\"BB\"({step})$"].astype(VItem).color.set(color=YELLOW)
            group_ges.add(t)
        group_ges.points.arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_border(RIGHT)
        arxiv_bb27 = TypstDoc(get_typ_doc("arxiv_bb27")).points.scale(0.75).r
        arxiv_bb27.points.move_to(LEFT * 6)
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
        blog_riemann.points.move_to(LEFT * 6.5)
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

        self.play(
            FadeOut(Group(
                text_Hc_steps,
                rec_ge,
                text_no_halt,
                rect_Hc,
                text_Hc_eq,
                text_collatz_2,
                text_S_step,
                rec_bb6,
                text_halt_implies_collatz,
                rec_collatz_q,
            )),
            TransformMatchingDiff(
                Group(text_bb6_ge, text_collatz_p),
                group_ges[0],
            ),
            self.camera.anim.points.shift(UP * 1),
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
            Write(group_ges[1]),
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
            Write(group_ges[2]),
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

        