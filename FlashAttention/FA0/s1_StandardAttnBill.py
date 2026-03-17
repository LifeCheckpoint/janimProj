import sys
from pathlib import Path
root = Path(__file__).parent.parent
sys.path.append(str(root))

from janim.imports import * # type: ignore

with reloads():
    from components.utils import *
    from components.colors import FAColor
    from components.grid_matrix import *
    from components.memory_bar import *
    from components.stride_background import *
if TYPE_CHECKING:
    from components.utils import *
    from components.colors import FAColor
    from components.grid_matrix import *
    from components.memory_bar import *
    from components.stride_background import *

class s1_1(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background_dark),
        typst_shared_preamble=get_typ_doc("preamble"),
    )
    def construct(self) -> None:
        dim_N = 6
        dim_d = 2
        mat_Q = create_grid_query(dim_N, dim_d)
        mat_K = create_grid_key(dim_N, dim_d)
        mat_KT = create_grid_key(dim_d, dim_N, names=lambda i, j: f"K^T_({i}, {j})")
        mat_V = create_grid_value(dim_N, dim_d)
        mat_Q.points.move_to(LEFT * 3)
        mat_K.points.move_to(ORIGIN)
        mat_V.points.move_to(RIGHT * 3)
        mat_KT.points.move_to(UP * 5 + RIGHT)
        text_Q = TypstMath("Q").points.scale(1.3).next_to(mat_Q, DOWN, buff=0.2).r
        text_K = TypstMath("K").points.scale(1.3).next_to(mat_K, DOWN, buff=0.2).r
        text_KT = TypstMath("K^T").points.scale(1.3).next_to(mat_KT, RIGHT, buff=1.5).r
        text_V = TypstMath("V").points.scale(1.3).next_to(mat_V, DOWN, buff=0.2).r
        brace_Q_dims = Group(
            Brace(mat_Q, LEFT, buff=0.1),
            Brace(mat_Q, UP, buff=0.1),
        ).points.shift(LEFT * 1).r
        brace_Q_dims.add(
            brace_Q_dims[0].points.create_typst(f"N={dim_N}"),
            brace_Q_dims[1].points.create_typst(f"d={dim_d}"),
        )
        brace_V_dims = Group(
            Brace(mat_V, LEFT, buff=0.1),
            Brace(mat_V, UP, buff=0.1),
        ).points.shift(RIGHT * 1).r
        brace_V_dims.add(
            brace_V_dims[0].points.create_typst(f"N={dim_N}"),
            brace_V_dims[1].points.create_typst(f"d={dim_d}"),
        )
        brace_KT_dims = Group(
            Brace(mat_KT, DOWN, buff=0.1),
            Brace(mat_KT, RIGHT, buff=0.1),
        )
        brace_KT_dims.add(
            brace_KT_dims[0].points.create_typst(f"N={dim_N}"),
            brace_KT_dims[1].points.create_typst(f"d={dim_d}"),
        )
        brace_K_dims = Group(
            Brace(mat_K, LEFT, buff=0.1),
            Brace(mat_K, UP, buff=0.1),
        )
        brace_K_dims.add(
            brace_K_dims[0].points.create_typst(f"N={dim_N}"),
            brace_K_dims[1].points.create_typst(f"d={dim_d}"),
        )
        memory_bar = MemoryBar(
            self,
            text_color=FAColor.light_text,
            overflow_max=3.2,
        )
        memory_bar.item.hide()
        Group(memory_bar.bg, memory_bar.tip).points.scale(1.2).move_to(UP * 5)

        self.forward(1)
        self.play(
            Write(mat_Q),
            Write(mat_K),
            Write(mat_V),
            Write(text_Q),
            Write(text_K),
            Write(text_V),
            lag_ratio=0.2,
            duration=2,
        )
        self.forward(1)
        self.play(
            Group(mat_Q, text_Q).anim.points.shift(LEFT * 1),
            Group(mat_V, text_V).anim.points.shift(RIGHT * 1),
            FadeIn(brace_Q_dims),
            FadeIn(brace_K_dims),
            FadeIn(brace_V_dims),
            duration=2,
        )
        self.forward(3)
        self.play(
            self.camera.anim.points.shift(UP * 2),
            FadeIn(memory_bar.item)
        )
        self.play(memory_bar.progress.anim.set_value(0.08))
        self.forward(1)

        text_attention = TypstMath("\"Softmax\"((Q dot.c K^T) / sqrt(d)) dot.c V")
        text_attention.points.scale(1.5).move_to(LEFT * 5.5 + UP * 5)
        rect_attention_QK = SurroundingRect(text_attention["Q dot.c K^T"])
        rect_attention_softmax = SurroundingRect(text_attention["\"Softmax\"((Q dot.c K^T)/sqrt(d))"])
        rect_attention_V = SurroundingRect(text_attention["dot.c V"])


        self.play(
            AnimGroup(
                self.camera.anim.points.scale(1.5),
                memory_bar.progress.anim.set_value(0.05),
                Group(mat_V, brace_V_dims).anim.points.shift(RIGHT * 12),
                FadeOut(brace_K_dims),
                FadeOut(text_K),
                FadeOut(text_V),
            ),
            AnimGroup(
                self.camera.anim.points.shift(RIGHT * 2),
                *[
                    TransformMatchingShapes(v, vt)
                    for v, vt in zip(transform_group(mat_K, 5), mat_KT)
                ],
                Group(memory_bar.bg, memory_bar.tip).anim.points.shift(UP * 2.25 + RIGHT * 1),
            ),
            AnimGroup(
                FadeIn(brace_KT_dims),
                Write(text_KT),
            ),
            Write(text_attention),
            duration=2,
            lag_ratio=0.2,
        )
        mat_V.hide()
        brace_V_dims.hide()
        self.forward(1)
        self.play(Write(rect_attention_QK))
        self.forward(0.5)

        mat_S = create_grid_matrix(
            dim_N, dim_N,
            create_cell_fn_by_2d=lambda i, j: create_grid_matrix_cell(
                value=f"S_({i},{j})",
                fill=FAColor.score_fill,
                text_color=FAColor.dark_text,
            ),
            buff=0,
        )
        mat_S.points.align_to(mat_KT, LEFT)
        mat_S.points.align_to(mat_Q, UP)
        text_S = TypstMath("S")
        text_S.points.scale(1.3).next_to(mat_S, DOWN, buff=0.2)
        rect_Qrow = SurroundingRect(Group(*mat_Q[0:dim_d]), color=BLUE_B, buff=0)
        rect_KTcol = SurroundingRect(Group(mat_KT[0::dim_N]), color=RED_B, buff=0)
        rect_Qrow.glow.set(color=BLUE_B, alpha=0.8, size=0.4)
        rect_KTcol.glow.set(color=RED_B, alpha=0.8, size=0.4)

        self.play(Write(rect_Qrow), Write(rect_KTcol))
        self.forward(1)
        for qi in range(dim_N):
            for kj in range(dim_N):
                if qi == 0 and kj <= 2:
                    play_time = 0.75
                    wait_time = 0.25
                elif qi <= 1:
                    play_time = 0.25
                    wait_time = 0.1
                else:
                    play_time = 0.1
                    wait_time = 0
                
                self.play(
                    *[
                        TransformMatchingShapes(
                            cell_k.copy().depth.set(-10).r, cells
                        ) for cell_k, cells in zip(
                            mat_KT[kj::dim_N], mat_S[qi * dim_N + kj]
                        )
                    ],
                    *[
                        TransformMatchingShapes(
                            cell_q.copy().depth.set(-10).r, cells
                        ) for cell_q, cells in zip(
                            mat_Q[qi * dim_d:qi * dim_d + dim_d], mat_S[qi * dim_N + kj]
                        )
                    ],
                    memory_bar.progress.anim.set_value(
                        memory_bar.progress.get_value() + 0.35 / dim_N ** 2
                    ),
                    duration=play_time,
                )

                if kj != dim_N - 1:
                    self.play(
                        rect_KTcol.anim.points.shift(RIGHT),
                        duration=play_time,
                    )

                self.forward(wait_time)

            if qi != dim_N - 1:
                self.play(
                    rect_KTcol.anim.points.shift(LEFT * (dim_N - 1)),
                    rect_Qrow.anim.points.shift(DOWN),
                    duration=0.2,
                )

        self.forward(1)
        self.play(
            Write(text_S),
            FadeOut(rect_KTcol),
            FadeOut(rect_Qrow),
        )
        
        text_softmax = TypstMath("arrow.r.long^(\"Softmax\")")
        text_softmax.points.scale(1.3).next_to(mat_S, RIGHT, buff=0.5)
        mat_P = create_grid_matrix(
            dim_N, dim_N,
            create_cell_fn_by_2d=lambda i, j: create_grid_matrix_cell(
                value=f"P_({i},{j})",
                fill=FAColor.probability_fill,
                text_color=FAColor.dark_text,
            ),
            buff=0,
        )
        mat_P.points.next_to(text_softmax, RIGHT, buff=0.5)
        text_P = TypstMath("P")
        text_P.points.scale(1.3).next_to(mat_P, DOWN, buff=0.2)

        self.forward(1)
        self.play(Transform(rect_attention_QK, rect_attention_softmax))
        self.play(Write(text_softmax))
        self.play(
            AnimGroup(
                *[
                    TransformMatchingShapes(si.copy(), pi)
                    for si, pi in zip(
                        wave_reorder(mat_S),
                        wave_reorder(mat_P)
                    )
                ],
                lag_ratio=0.03,
                duration=1,
            ),
            memory_bar.progress.anim.set_value(0.8),
            duration=3.0,
        )
        self.play(Write(text_P))
        self.forward(2)

        self.forward(1)
        mat_V.points.next_to(mat_P, RIGHT, buff=1)
        Group(mat_V, brace_V_dims).points.align_to(mat_KT, DOWN)
        brace_V_dims.points.shift(LEFT * 1.85)
        text_V.points.next_to(mat_V, RIGHT, buff=0.5)
        mat_O = create_grid_matrix(
            dim_N, dim_d,
            create_cell_fn_by_2d=lambda i, j: create_grid_matrix_cell(
                value=f"O_({i},{j})",
                fill=FAColor.output_fill,
                text_color=FAColor.dark_text,
            ),
            buff=0,
        )
        mat_O.points.align_to(mat_V, LEFT)
        mat_O.points.align_to(mat_P, UP)
        text_O = TypstMath("O")
        text_O.points.scale(1.3).next_to(mat_O, DOWN, buff=0.2)

        self.play(
            self.camera.anim.points.shift(RIGHT * 2 + UP * 1.5).scale(1.25),
            memory_bar.progress.anim.set_value(0.83),
            Write(mat_V),
            Write(brace_V_dims),
            Write(text_V),
            Transform(rect_attention_softmax, rect_attention_V),
        )
        self.forward(1)
        for pj in range(dim_N):
            for vi in range(dim_d):
                play_time = 0.1
                wait_time = 0
                
                self.play(
                    *[
                        TransformMatchingShapes(
                            cell_v.copy().depth.set(-10).r, cell_o
                        ) for cell_v, cell_o in zip(
                            mat_V[vi::dim_d], mat_O[pj * dim_d + vi]
                        )
                    ],
                    *[
                        TransformMatchingShapes(
                            cell_p.copy().depth.set(-10).r, cell_o
                        ) for cell_p, cell_o in zip(
                            mat_P[pj * dim_N:pj * dim_N + dim_N], mat_O[pj * dim_d + vi]
                        )
                    ],
                    memory_bar.progress.anim.set_value(
                        memory_bar.progress.get_value() + 0.03 / dim_N ** 2
                    ),
                    duration=play_time,
                )

                self.forward(wait_time)

        self.play(Write(text_O))
        self.forward(1)
        self.play(
            FadeOut(brace_KT_dims),
            FadeOut(brace_Q_dims),
            FadeOut(brace_V_dims),
            text_KT.anim.points.shift(LEFT),
        )

        sep_p0 = (mat_KT.points.box.get(DL) + mat_Q.points.box.get(UR)) / 2
        sep_p1 = (mat_P.points.box.get(UR) + mat_V.points.box.get(DL)) / 2
        sep_group = Group(
            DashedLine(sep_p0, sep_p0 + DOWN * 10),
            DashedLine(sep_p0, sep_p0 + RIGHT * 25),
            DashedLine(sep_p1, sep_p1 + DOWN * 10)
        )
        text_input = TypstText("输入矩阵 $Q$, $K$, $V$")
        text_middle = TypstText("中间矩阵 $S$, $P$")
        text_output = TypstText("输出矩阵 $O$")
        Group(text_input, text_middle, text_output).points.scale(1.5)
        text_input.points.next_to(text_KT, RIGHT, buff=2)
        text_middle.points.next_to(text_softmax, DOWN).align_to(text_S, DOWN).shift(DOWN * 0.75)
        text_output.points.move_to(text_middle).align_to(text_O, LEFT)

        self.play(
            self.camera.anim.points.shift(DOWN * 1.5 + RIGHT * 1).scale(0.9),
            FadeOut(rect_attention_V),
            FadeOut(text_attention),
            Write(sep_group),
        )
        self.play(
            Write(text_input),
            Write(text_middle),
            Write(text_output),
            lag_ratio=0.2,
        )
        self.forward(2)

        def make_fit_box(fill: str, ref: Group):
            box = Rect(
                ref.points.box.width,
                ref.points.box.height
            )
            box.fill.set(color=fill, alpha=1)
            box.stroke.set(color=FAColor.background_light, alpha=1)
            box.points.move_to(ref)
            return box
        
        mats = [mat_Q, mat_KT, mat_V, mat_S, mat_P, mat_O]
        box_Q = make_fit_box(FAColor.query_fill, mat_Q)
        box_KT = make_fit_box(FAColor.key_fill, mat_KT)
        box_V = make_fit_box(FAColor.value_fill, mat_V)
        box_S = make_fit_box(FAColor.score_fill, mat_S)
        box_P = make_fit_box(FAColor.probability_fill, mat_P)
        box_O = make_fit_box(FAColor.output_fill, mat_O)
        boxes = [box_Q, box_KT, box_V, box_S, box_P, box_O]
        group_boxes = Group(box_Q, box_KT, box_V, box_S, box_P, box_O)
        group_texts = Group(text_Q, text_KT, text_V, text_S, text_P, text_O)
        group_boxes.points.shift(LEFT * 5)
        text_OOM = Text("Out Of Memory", font="Linux Libertine", depth=-15)
        text_OOM.points.move_to(RIGHT * 6 + DOWN * 3)
        text_OOM.points.scale(10)
        text_OOM.astype(VItem).fill.set(color=FAColor.c_shanhu_red, alpha=0.85)

        self.prepare(
            self.camera.anim.points.move_to(UP * 2),
            rate_func=ease_inout_cubic
        )
        self.play(
            FadeOut(sep_group),
            FadeOut(Group(text_input, text_middle, text_output)),
            *[
                Transform(mat, box, flatten=True)
                for mat, box in zip(mats, boxes)
            ],
            group_texts.anim.points.shift(LEFT * 5),
        )
        self.forward(1)
        self.play(
            FadeOut(Group(box_O, box_V, text_O, text_V)),
            memory_bar.progress.anim.set_value(0.8),
        )
        text_softmax.hide()
        self.forward(1)
        KT_width = box_KT.points.box.width
        Q_height = box_Q.points.box.height
        def align_box_KT(item: VItem, p: UpdaterParams):
            item.points.set_width((1 + p.alpha) * KT_width, stretch=True)
            item.points.align_to(box_S, LEFT)
        def align_box_Q(item: VItem, p: UpdaterParams):
            item.points.set_height((1 + p.alpha) * Q_height, stretch=True)
            item.points.align_to(box_S, UP)
        self.prepare(
            self.camera.anim.points.shift(RIGHT * 4 + DOWN * 3).scale(1.5),
            AnimGroup(
                AnimGroup(
                    text_KT.anim.points.shift(RIGHT * box_KT.points.box.width),
                    DataUpdater(box_KT, align_box_KT),
                ),
                AnimGroup(
                    text_Q.anim.points.shift(DOWN * box_Q.points.box.height),
                    DataUpdater(box_Q, align_box_Q),
                ),
                lag_ratio=0.5,
            ),
            duration=3.0,
        )
        box_Ss = [box_S.copy() for _ in range(4 - 1)]
        box_Ps = [box_P.copy() for _ in range(4 - 1)]
        self.play(
            Group(box_Ss[0], box_Ss[2]).anim.points.next_to(box_S, RIGHT, buff=0),
            text_S.anim.points.shift(RIGHT * box_S.points.box.width / 2),
            Group(box_P, box_Ps[1]).anim.points.shift(RIGHT * box_S.points.box.width),
            Group(box_Ps[0], box_Ps[2]).anim.points.shift(RIGHT * (box_S.points.box.width + box_P.points.box.width)),
            text_P.anim.points.shift(RIGHT * (box_S.points.box.width + box_P.points.box.width / 2)),
            memory_bar.progress.anim.set_value(1.6),
        )
        self.forward(0.5)
        self.prepare(
            Write(text_OOM),
            duration=2.0,
        )
        self.play(
            Group(box_Ss[1], box_Ss[2]).anim.points.shift(DOWN * box_S.points.box.height),
            Group(box_Ps[1], box_Ps[2]).anim.points.shift(DOWN * box_P.points.box.height),
            text_S.anim.points.shift(DOWN * box_S.points.box.height),
            text_P.anim.points.shift(DOWN * box_P.points.box.height),
            memory_bar.progress.anim.set_value(3.2),
        )
        self.forward(2)

        def align_box_KT_2(item: VItem, p: UpdaterParams):
            item.points.set_width((2 - p.alpha) * KT_width, stretch=True)
            item.points.align_to(box_S, LEFT)
        def align_box_Q_2(item: VItem, p: UpdaterParams):
            item.points.set_height((2 - p.alpha) * Q_height, stretch=True)
            item.points.align_to(box_S, UP)
        self.play(
            FadeOut(text_OOM),
            self.camera.anim.points.move_to(UP * 2).scale(2 / 3),
            memory_bar.progress.anim.set_value(0.8),
            text_KT.anim.points.shift(LEFT * box_KT.points.box.width / 2),
            text_Q.anim.points.shift(UP * box_Q.points.box.height / 2),
            text_S.anim.points.next_to(box_S, DOWN, buff=0.2),
            text_P.anim.points.next_to(box_P, DOWN, buff=0.2),
            DataUpdater(box_KT, align_box_KT_2),
            DataUpdater(box_Q, align_box_Q_2),
            FadeOut(Group.from_iterable(box_Ss)),
            FadeOut(Group.from_iterable(box_Ps))
        )
        self.play(
            Group(text_P, box_P).anim.points.next_to(
                Group(text_S, box_S),
                RIGHT,
                buff=1.5,
            )
        )
        self.forward(2)
        
        hbm_shade, hbm_shade_mask = create_stride_background(
            width=box_P.points.box.width + box_S.points.box.width + 2,
            height=box_S.points.box.height + 1,
            color_1="#624329",
            use_stroke=False,
        )
        hbm_shade_mask.show()
        hbm_shade_mask.points.move_to((box_S.points.box.center + box_P.points.box.center) / 2 + DOWN * 0.25)

        self.play(
            FadeIn(text_O),
            FadeIn(box_O),
            FadeIn(text_V),
            FadeIn(box_V),
        )
        self.forward(1)
        box_S.depth.set(-10)
        box_P.depth.set(-10)
        text_S.depth.set(-10)
        text_P.depth.set(-10)
        self.prepare(
            hbm_shade.anim.points.shift(DOWN * 4),
            duration=10.0,
        )
        self.play(
            memory_bar.progress.anim.set_value(0.08),
            box_S.anim.color.set(alpha=0.45),
            box_P.anim.color.set(alpha=0.45),
            text_S.astype(VItem).anim.color.set(alpha=0.45),
            text_P.astype(VItem).anim.color.set(alpha=0.45),
            FadeIn(hbm_shade),
        )
        self.forward(1)
        text_KT.depth.set(-10)
        box_KT.depth.set(-10)
        self.play(
            self.camera.anim.points.move_to(DOWN * 8),
            Group(box_Q, text_Q).anim.points.move_to(LEFT * 6 + DOWN * 8),
            box_KT.anim.points.move_to(DOWN * 8),
            text_KT.anim.points.next_to(DOWN * (8 + box_KT.points.box.height / 2), DOWN, buff=0.2),
            box_V.anim.points.move_to(RIGHT * 6 + DOWN * 8),
            text_V.anim.points.next_to(RIGHT * 6 + DOWN * (8 + box_V.points.box.height / 2), DOWN, buff=0.2),
        )
        self.forward(1)

        brace_QKTV = Brace(
            Group(text_Q, text_V, box_Q, box_V),
            direction=DOWN,
            buff=0.5,
        )
        self.play(
            self.camera.anim.points.shift(DOWN * 6),
            Write(brace_QKTV),
            Group(box_O, text_O).anim.points.next_to(brace_QKTV, DOWN, buff=0.5),
        )
        self.forward(2)
        self.play(
            FadeOut(Group(
                box_Q, box_KT, box_V,
                text_Q, text_KT, text_V,
                brace_QKTV,
                box_O, text_O,
            ))
        )
        self.forward(0.5)
