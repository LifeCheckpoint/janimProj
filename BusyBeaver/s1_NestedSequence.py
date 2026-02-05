from janim.imports import * # type: ignore
from tools import get_typ_doc

local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]

from dowhen import goto
from janim.render.renderer_vitem_plane import VItemPlaneRenderer
source_hash = "f746551d"
goto("if self.vbo_points.size != self.vbo_mapped_points.size:").when(
    VItemPlaneRenderer._update_points_normal,
    "if new_attrs.points is not self.attrs.points \\",
    source_hash=source_hash
)

class s1_2(Timeline):
    """
    uv run janim run s1_NestedSequence.py s1_2 -i
    """

    def construct(self):
        text_n100 = TypstMath(R"n^(100)").points.shift(LEFT * 3).scale(3).r
        axes1 = Axes(
            x_range=(0, 11, 11 / 10),
            y_range=(0, 250, 25),
            x_length=5,
            y_length=4.5,
        ).points.next_to(LEFT * 3 + UP * 3, DOWN, buff=1).r
        axes1(VItem).color.set(alpha=0.5)
        log_tag_1 = TypstText(R"$log$ scale").points.scale(0.75).r
        log_tag_1.astype(VItem).fill.set(alpha=0.5)
        log_tag_2 = log_tag_1.copy()
        graph_n100 = axes1.get_graph(
            lambda x: 100 * np.log(x),
            x_range=(1, 10),
        )
        graph_n100(VItem).color.set(color=BLUE_B).r
        points_n100 = Group(*[
            Dot(axes1.c2p(x, 100 * np.log(x))).points.scale(0.9).r \
                                              .color.set(color=YELLOW).r
            for x in range(1, 11)
        ])
        point_dynamic_n100 = Dot(axes1.c2p(1, 0)).points.scale(1.5).r \
                                                 .color.set(color=YELLOW).r \
                                                 .fill.set(alpha=0).r \
                                                 .stroke.set(alpha=1).r
        text_dynamic_n100 = TypstText("")

        text_2n = TypstMath(R"2^n").points.shift(RIGHT * 3).scale(3).r
        axes2 = Axes(
            x_range=(0, 11, 11 / 10),
            y_range=(0, 250, 25),
            x_length=5,
            y_length=4.5,
        ).points.next_to(RIGHT * 3 + UP * 3, DOWN, buff=1).r
        axes2.astype(VItem).color.set(alpha=0.5)
        graph_2n = axes2.get_graph(
            lambda x: np.log(2) * x,
            x_range=(1, 10),
        )
        graph_2n.astype(VItem).color.set(color=GREEN_A)
        points_2n = Group(*[
            Dot(axes2.c2p(x, np.log(2) * x)).points.scale(0.9).r \
                                            .color.set(color=RED_A).r
            for x in range(1, 11)
        ])
        point_dynamic_2n = Dot(axes2.c2p(1, 0)).points.scale(1.5).r \
                                               .color.set(color=RED_A).r \
                                               .fill.set(alpha=0).r \
                                               .stroke.set(alpha=1).r
        text_dynamic_2n = TypstText("")

        log_tag_1.points.next_to(axes1.get_axes()[1].get_tick(250), LEFT, buff=0.1)
        log_tag_2.points.next_to(axes2.get_axes()[1].get_tick(250), LEFT, buff=0.1)

        self.play(Write(text_n100))
        self.play(Write(text_2n))
        self.forward(1)
        self.play(
            text_n100.anim.points.shift(UP * 3),
            text_n100.anim.points.scale(0.5),
            text_2n.anim.points.shift(UP * 3),
            text_2n.anim.points.scale(0.5),
            Write(axes1),
            Write(axes2),
            Write(log_tag_1),
            Write(log_tag_2),
        )
        self.play(Write(graph_n100))
        self.play(Write(graph_2n))
        self.play(
            *[Write(dot) for dot in points_n100],
            *[Write(dot) for dot in points_2n],
            Write(point_dynamic_n100),
            Write(point_dynamic_2n),
            duration=2,
            lag_ratio=0.25,
        )
        self.forward(0.5)
        self.play(
            DataUpdater(
                point_dynamic_n100,
                lambda data, p: data.points.move_to(
                    axes1.c2p(p.alpha * 9 + 1, 100 * np.log(p.alpha * 9 + 1))
                )
            ),
            DataUpdater(
                point_dynamic_2n,
                lambda data, p: data.points.move_to(
                    axes2.c2p(p.alpha * 9 + 1, np.log(2) * (p.alpha * 9 + 1))
                )
            ),
            ItemUpdater(
                text_dynamic_n100,
                lambda p: TypstText(
                    f"#text(fill: color.rgb(\"#b1f2eb\"))[$f({int(p.alpha * 9 + 1)})={int(p.alpha * 9 + 1)}^(100)$]"
                ).points.next_to(point_dynamic_n100.current()).r
            ),
            ItemUpdater(
                text_dynamic_2n,
                lambda p: TypstText(
                    f"#text(fill: color.rgb(\"#f2b1b1\"))[$g({int(p.alpha * 9 + 1)})=2^{int(p.alpha * 9 + 1)}$]"
                ).points.next_to(point_dynamic_2n.current(), UP).r
            ),
            duration=3,
        )
        self.forward(2)
        self.play(
            FadeOut(text_dynamic_n100),
            FadeOut(text_dynamic_2n),
            FadeOut(point_dynamic_n100),
            FadeOut(point_dynamic_2n),
            FadeOut(points_2n),
            FadeOut(points_n100),
            lag_ratio=0.25,
        )
        self.forward(1)
        
        graph_full_length = 10.0
        map_x_ticks: Callable[[float], float] = lambda x: 1 + (graph_full_length - 1) * np.log(x) / (graph_full_length + np.log(x))
        unmap_x_ticks: Callable[[float], float] = lambda y: np.exp(graph_full_length * (y - 1) / (graph_full_length - y))
        # map_x_ticks: [1, +inf) -> [1, graph_full_length)
        # unmap_x_ticks: [1, graph_full_length) -> [1, +inf)

        max_10n = 10  # 指数范围
        log_arc_tickes = [map_x_ticks(i * 10**j) for j in range(max_10n + 1) for i in range(1, 10)]

        axes1_l = Axes(
            x_range=(0, 11, 20),
            y_range=(0, 250, 25),
            x_length=5,
            y_length=4.5,
        ).points.next_to(LEFT * 3 + UP * 3, DOWN, buff=1).r
        axes1_l(VItem).color.set(alpha=0.5)
        axes1_l_new_ticks = Group(
            *[
                axes1_l.get_axes()[0].get_tick(lt)
                for lt in log_arc_tickes
            ],
            inf_tick := axes1_l.get_axes()[0].get_tick(graph_full_length),
        )
        inf_tick_text_1 = TypstMath("infinity").points.scale(0.75).next_to(inf_tick, DOWN, buff=0.1).r
        graph_n100_l = axes1_l.get_graph(
            lambda x: np.clip(100 * np.log(unmap_x_ticks(x)) / 100, -100, 500),
            x_range=(1, 9.7, 0.001)
        )
        graph_n100_l(VItem).color.set(color=BLUE_B).r

        axes2_l = Axes(
            x_range=(0, 11, 20),
            y_range=(0, 250, 25),
            x_length=5,
            y_length=4.5,
        ).points.next_to(RIGHT * 3 + UP * 3, DOWN, buff=1).r
        axes2_l(VItem).color.set(alpha=0.5)
        axes2_l_new_ticks = Group(
            *[
                axes2_l.get_axes()[0].get_tick(lt)
                for lt in log_arc_tickes
            ],
            inf_tick := axes2_l.get_axes()[0].get_tick(graph_full_length),
        )
        inf_tick_text_2 = TypstMath("infinity").points.scale(0.75).next_to(inf_tick, DOWN, buff=0.1).r
        graph_2n_l = axes2_l.get_graph(
            lambda x: np.clip(np.log(2) * unmap_x_ticks(x) / 100, -100, 500),
            x_range=(1, 5.65, 0.001)
        )
        graph_2n_l(VItem).color.set(color=GREEN_A).r

        self.play(
            TransformMatchingDiff(axes1, axes1_l),
            TransformMatchingDiff(axes2, axes2_l),
            rate_func=smooth,
        )
        self.play(
            FadeIn(axes1_l_new_ticks, lag_ratio=0.2),
            Write(inf_tick_text_1),
            Transform(graph_n100, graph_n100_l),
            duration=2,
        )
        self.play(
            FadeIn(axes2_l_new_ticks, lag_ratio=0.2),
            Write(inf_tick_text_2),
            Transform(graph_2n, graph_2n_l),
            duration=2,
        )
        self.forward(2)
        self.play(
            axes1_l.anim.points.shift(RIGHT * 3),
            axes2_l.anim.points.shift(LEFT * 3),
            axes2_l_new_ticks.anim.points.shift(LEFT * 3),
            axes1_l_new_ticks.anim.points.shift(RIGHT * 3),
            inf_tick_text_1.anim.points.shift(RIGHT * 3),
            inf_tick_text_2.anim.points.shift(LEFT * 3),
            graph_n100_l.anim.points.shift(RIGHT * 0.001), # fix
            graph_2n_l.anim.points.shift(LEFT * 0.001), # fix
            axes1_l_new_ticks.anim.astype(VItem).color.set(alpha=0.25),
            axes2_l_new_ticks.anim.astype(VItem).color.set(alpha=0.25),
            text_2n.anim.points.scale(0.75).shift(LEFT * 3.25 + DOWN * 1.5),
            text_n100.anim.points.scale(0.75).shift(RIGHT * 4.5 + DOWN * 1.5),
            log_tag_1.anim.points.shift(RIGHT * 3),
            log_tag_2.anim.points.shift(LEFT * 3),
        )
        self.forward(1.5)

        dot_2n_slider = Dot(axes2_l.c2p(1, 0)).points.scale(1.25).r \
                                              .stroke.set(alpha=1, color=GREEN_A).r \
                                              .fill.set(alpha=0).r
        dot_n100_slider = Dot(axes1_l.c2p(1, 0)).points.scale(1.25).r \
                                                .stroke.set(alpha=1, color=BLUE_A).r \
                                                .fill.set(alpha=0).r
        dashline_sliders = DashedLine()
        
        self.play(
            FadeIn(dot_2n_slider),
            FadeIn(dot_n100_slider),
            DataUpdater(
                self.camera,
                lambda data, p: data.points.scale(1 - 0.6 * p.alpha).shift(DOWN * 2.5 * p.alpha),
                rate_func=ease_inout_cubic,
            )
        )
        self.forward(0.5)
        final_point_buff = 4
        self.prepare(
            DataUpdater(
                dot_2n_slider,
                lambda data, p: data.points.move_to(
                    axes2_l.c2p(
                        1 + (graph_full_length - final_point_buff) * p.alpha,
                        np.clip(100 * np.log(unmap_x_ticks(1 + (graph_full_length - final_point_buff) * p.alpha)) / 100, -100, 500)
                    )
                )
            ),
            DataUpdater(
                dot_n100_slider,
                lambda data, p: data.points.move_to(
                    axes1_l.c2p(
                        1 + (graph_full_length - final_point_buff) * p.alpha,
                        np.clip(np.log(2) * unmap_x_ticks(1 + (graph_full_length - final_point_buff) * p.alpha) / 100, -100, 500)
                    )
                )
            ),
            ItemUpdater(
                dashline_sliders,
                lambda p: DashedLine(
                    dot_2n_slider.current().points.box.center,
                    dot_n100_slider.current().points.box.center,
                    buff=0.1
                )
            ),
            DataUpdater(
                self.camera,
                lambda data, p: data.points.shift(UP * 2.5 * p.alpha),
            ),
            duration=3.5,
            rate_func=smooth,
        )
        self.forward(1)
        self.play(          
            DataUpdater(
                self.camera,
                lambda data, p: data.points.scale(1 + 1 * p.alpha),
            ),
            duration=2.5,
            rate_func=smooth,
        )
        self.forward(1)
        self.play(
            FadeOut(dashline_sliders),
            FadeOut(dot_2n_slider),
            FadeOut(dot_n100_slider),
        )
        self.forward(1)
        self.play(
            FadeOut(axes1_l),
            FadeOut(axes2_l),
            FadeOut(axes1_l_new_ticks),
            FadeOut(axes2_l_new_ticks),
            FadeOut(inf_tick_text_1),
            FadeOut(inf_tick_text_2),
            FadeOut(graph_n100_l),
            FadeOut(graph_2n_l),
            FadeOut(text_n100),
            FadeOut(text_2n),
            FadeOut(log_tag_1),
            FadeOut(log_tag_2),
        )
        self.forward(1)


class s1_3(Timeline):
    """
    uv run janim run s1_NestedSequence.py s1_3 -i
    """
    def construct(self):
        text_2n = TypstMath("2^n").points.shift(LEFT * 2).scale(2).r
        text_2n.astype(VItem).color.set(color=GREEN_A).r
        text_fact = TypstMath("n!").points.shift(RIGHT * 2).scale(2).r
        text_fact.astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n = TypstMath("(2^n)/(n!)").points.scale(2).r
        text_frac_fact_2n["2^n"].astype(VItem).color.set(color=GREEN_A).r
        text_frac_fact_2n["n!"].astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n_expanded = TypstMath("overbrace(2 times 2 times 2 times ... times 2, \"n\")/(1 times 2 times 3 times ... times n)").points.scale(2).r
        text_frac_fact_2n_expanded["overbrace(2 times 2 times 2 times ... times 2, \"n\")"].astype(VItem).color.set(color=GREEN_A).r
        text_frac_fact_2n_expanded["1 times 2 times 3 times ... times n"].astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n_split = TypstMath("2/1 times 2/2 times 2/3 times ... times 2/n").points.scale(2).r
        for i in range(5):
            if i != 2:
                text_frac_fact_2n_split["2", i].astype(VItem).color.set(color=GREEN_A).r
        text_frac_fact_2n_split["1"].astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n_split["2", 2].astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n_split["3"].astype(VItem).color.set(color=RED_A).r
        text_frac_fact_2n_split["n"].astype(VItem).color.set(color=RED_A).r
        box_1 = SurroundingRect(text_frac_fact_2n_split["2/2"]).color.set(color=YELLOW).r
        box_2 = SurroundingRect(text_frac_fact_2n_split["2/2 times 2/3"]).color.set(color=YELLOW).r
        box_3 = SurroundingRect(text_frac_fact_2n_split["2/2 times 2/3 times ... times 2/n"]).color.set(color=YELLOW).r
        text_prod_res_1 = TypstMath("1.000").points.next_to(box_1, DOWN, buff=0.5).scale(1.5).r
        text_prod_res_2 = TypstMath("0.667").points.next_to(box_2, DOWN, buff=0.5).scale(1.5).r
        text_prod_res_3 = TypstMath("")

        self.play(Write(text_2n))
        self.play(Write(text_fact))
        self.forward(1)
        self.play(
            TransformMatchingDiff(text_2n, text_frac_fact_2n),
            TransformMatchingDiff(text_fact, text_frac_fact_2n),
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(text_frac_fact_2n, text_frac_fact_2n_expanded),
        )
        self.forward(2)
        self.play(
            TransformMatchingDiff(text_frac_fact_2n_expanded, text_frac_fact_2n_split),
        )
        self.forward(2)
        self.play(Write(box_1))
        self.play(Write(text_prod_res_1))
        self.forward(1)
        self.play(
            Transform(box_1, box_2),
            TransformMatchingShapes(text_prod_res_1, text_prod_res_2)
        )
        self.forward(1)
        text_prod_res_2.hide()
        self.play(
            Transform(box_2, box_3),
            ItemUpdater(
                text_prod_res_3,
                lambda p: TypstMath(
                    "{:.3f}".format((1 - p.alpha) * 2 / 3, 3)
                ).points.move_to(
                    text_prod_res_2.points.box.center + \
                    p.alpha * (box_3.points.box.bottom - box_2.points.box.bottom)
                ).scale(1.5).r,
                hide_at_begin=False,
            ),
            duration=2.5,
            rate_func=smooth,
        )
        self.forward(1)

class s1_4(Timeline):
    """
    uv run janim run s1_NestedSequence.py s1_4 -i
    """
    def construct(self):
        def tansform_matching_diff_in_segments(
            item_from: Item,
            segments_from: list[list[int]],
            item_to: Item,
            segments_to: list[list[int]],
            **trs_kwargs,
        ):
            return [
                TransformMatchingDiff(item_from[l1:r1], item_to[l2:r2], **trs_kwargs)
                for (l1, r1), (l2, r2) in TransformInSegments.parse_segments(segments_from, segments_to)
            ]

        text_2times3 = TypstMath("2 times 3").points.scale(1.75).r
        text_2times3_eq_2p2p2 = TypstMath("2 times 3 = 2 + 2 + 2").points.scale(1.75).r
        text_2pow3 = TypstMath("2^3").points.scale(1.75).shift(DOWN * 0.5).r
        text_2pow3_eq_2times2times2 = TypstMath("2^3 = 2 times 2 times 2").points.scale(1.75).shift(DOWN * 0.5).r
        text_quest_2pow2pow2 = TypstMath("?=2^(2^2)").points.scale(1.75).shift(DOWN * 1).r
        text_pow_2_nest_3 = TypstMath("2^(2^2)").points.scale(2.5).r
        text_pow_2_nest_4 = TypstMath("2^(2^(2^2))").points.scale(2.5).r
        text_pow_2_nest_5 = TypstMath("2^(2^(2^(2^2)))").points.scale(2.5).r
        text_pow_2_nest_5_gt_fact_5000 = TypstMath("2^(2^(2^(2^2))) > 5000!").points.scale(2.5).r
        text_tmp_pows = TypstMath("")
        text_pow_2_nest_5_cpy = text_pow_2_nest_5.copy()
        textdict_text_pow_2_nest_5_gt_fact_expanded = {
            k: TypstMath(f"2^(2^(2^(2^2))) > {5000 - k}! & dot.op {" dot.op ".join(str(5000 - i - 1) + (R" \ & " if (5000 - i - 1) % 10 == 0 else "") for i in range(0, k))}").points.scale(2.5).r
            for k in range(0, 50)
        }
        text_pow_2_nest_10 = TypstMath("2^(2^(2^(2^(2^(2^(2^(2^(2^2))))))))").points.scale(2.5).r

        self.play(Write(text_2times3))
        self.forward(1)
        self.play(
            *tansform_matching_diff_in_segments(
                text_2times3,
                [[0, 3], [1, 2], [1, 2], [0, 1], [0, 1], [0, 1]],
                text_2times3_eq_2p2p2,
                [[0, 3], [5, 6], [7, 8], [4, 5], [6, 7], [8, 9]],
                path_arc=PI / 2,
            ),
            FadeIn(text_2times3_eq_2p2p2["="]),
            lag_ratio=0.02,
        )
        self.forward(1.5)
        self.play(
            Write(text_2pow3),
            text_2times3_eq_2p2p2.anim.points.shift(UP * 0.5),
        )
        self.forward(1)
        self.play(
            *[
                TransformMatchingDiff(
                    text_2pow3["2"],
                    text_2pow3_eq_2times2times2["2", i],
                    path_arc=PI / 2,
                )
                for i in range(1, 4)
            ],
            TransformMatchingDiff(
                text_2pow3["2^3"],
                text_2pow3_eq_2times2times2["2^3"],
            ),
            FadeIn(text_2pow3_eq_2times2times2["="]),
            FadeIn(text_2pow3_eq_2times2times2["times", ...]),
            lag_ratio=0.02,
        )
        self.forward(1.5)
        self.play(
            text_2times3_eq_2p2p2.anim.points.shift(UP * 0.5),
            text_2pow3_eq_2times2times2.anim.points.shift(UP * 0.5),
            FadeIn(text_quest_2pow2pow2),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(text_quest_2pow2pow2, text_pow_2_nest_3),
            FadeOut(text_2times3_eq_2p2p2),
            FadeOut(text_2pow3_eq_2times2times2),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(TransformMatchingDiff(text_pow_2_nest_3, text_pow_2_nest_4))
        self.forward(1)
        self.play(TransformMatchingDiff(text_pow_2_nest_4, text_pow_2_nest_5))
        self.forward(1)
        self.play(TransformMatchingDiff(text_pow_2_nest_5, text_pow_2_nest_5_gt_fact_5000))
        self.forward(1.5)
        text_pow_2_nest_5_gt_fact_5000.hide()
        
        def get_nest_frac_text(alpha: float):
            total = 50
            index = int(np.clip(1 + alpha * (total - 1), 1, total - 1))
            text_item = textdict_text_pow_2_nest_5_gt_fact_expanded[index]
            alpha_transform_start = 0.75
            alpha = 1 - max(alpha - alpha_transform_start, 0) / (1 - alpha_transform_start)
            text_item.astype(VItem).fill.set(alpha=alpha)
            return text_item

        self.play(
            ItemUpdater(
                text_tmp_pows,
                lambda p: get_nest_frac_text(p.alpha),
                rate_func=ease_out_sine,
            ),
            DataUpdater(
                self.camera,
                lambda data, p: data.points.scale(1 + 1.5 * p.alpha),
                rate_func=ease_out_expo,
            ),
            duration=5,
        )
        self.forward(1)
        self.camera.points.reset()
        self.play(FadeIn(text_pow_2_nest_5_cpy))
        self.play(TransformMatchingDiff(text_pow_2_nest_5_cpy, text_pow_2_nest_10))

        text_knuth_up = TypstMath("arrow.t").points.scale(2.5).r
        text_knuth_name = Group(
            Text("高德纳符号", font=local_font).color.set(color=GREEN_C).r.points.scale(2).r,
            Text("Knuth's up-arrow notation", font=local_font).color.set(color=GREEN_A).r,
        )
        text_knuth_name[1].points.next_to(text_knuth_name[0], DOWN, aligned_edge=LEFT, buff=0.2)
        text_knuth_name.points.move_to(ORIGIN)
        text_A_knuth_B = TypstMath("A arrow.t B").points.scale(2.5).r
        text_A_knuth_B_eq_A_pow_B = TypstMath("A arrow.t B = A^B").points.scale(2.5).r
        text_pow_2_nest_10_cpy = text_pow_2_nest_10.copy()
        surround_10 = SurroundingRect(text_pow_2_nest_10_cpy["space^(2^(2^(2^(2^(2^(2^(2^(2^2))))))))"])
        surround_2 = SurroundingRect(text_pow_2_nest_10_cpy["2"]).color.set(color=BLUE_A).r
        text_2_knuth_2nest_n_eq_pow_2_nest_n = TypstMath("2 arrow.t arrow.t n = 2^(2^(2^(dots.up ^ 2)))").points.scale(2.5).r
        text_2_knuth_2nest_n_explain = TypstMath("2 arrow.t (2 arrow.t arrow.t (n-1) )").points.scale(2.5).r
        text_2_knuth_2nest_n_explain.match_pattern(
            text_2_knuth_2nest_n_eq_pow_2_nest_n,
            "arrow.t arrow.t",
        )
        text_2_knuth_2nest_n_explain.points.shift(DOWN * 1)
        text_2_knuth_2nest_n = TypstMath("2 arrow.t arrow.t n").points.scale(2.5).r
        text_2_knuth_2nest_n.match_pattern(
            text_2_knuth_2nest_n_eq_pow_2_nest_n,
            "2 arrow.t arrow.t n",
        )
        text_2_knuth_2nest_n.points.shift(DOWN * 1)
        
        self.forward(1)
        self.play(
            FadeOut(text_pow_2_nest_10),
            Write(text_knuth_up),
        )
        self.forward(1)
        self.play(
            FadeIn(text_knuth_name),
            text_knuth_up.anim.points.next_to(LEFT * 0.5, LEFT),
            text_knuth_name.anim.points.next_to(RIGHT * 0.5, RIGHT),
        )
        self.forward(2)
        self.play(
            FadeOut(text_knuth_name),
            text_knuth_up.anim.points.move_to(ORIGIN),
        )
        self.play(
            TransformMatchingDiff(text_knuth_up, text_A_knuth_B),
            rate_func=smooth,
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_A_knuth_B["A", 0],
                text_A_knuth_B_eq_A_pow_B["A", 0],
            ),
            TransformMatchingDiff(
                text_A_knuth_B["A", 0],
                text_A_knuth_B_eq_A_pow_B["A", 1],
            ),
            TransformMatchingDiff(
                text_A_knuth_B["arrow.t"],
                text_A_knuth_B_eq_A_pow_B["arrow.t"],
            ),
            TransformMatchingDiff(
                text_A_knuth_B["B", 0],
                text_A_knuth_B_eq_A_pow_B["B", 0],
            ),
            TransformMatchingDiff(
                text_A_knuth_B["B", 0],
                text_A_knuth_B_eq_A_pow_B["space^B", 0],
            ),
            FadeIn(text_A_knuth_B_eq_A_pow_B["="]),
        )
        self.forward(1.5)
        self.play(
            FadeOut(text_A_knuth_B_eq_A_pow_B)
        )
        self.forward(1)
        self.play(Write(text_pow_2_nest_10_cpy))
        self.forward(1)
        self.play(Write(surround_10))
        self.forward(1.5)
        temp_pos_2nests = text_pow_2_nest_10_cpy["space^(2^(2^(2^(2^(2^(2^(2^(2^2))))))))"].points.box.center
        self.play(
            FadeOut(surround_10),
            FadeOut(text_pow_2_nest_10_cpy["2"]),
            text_pow_2_nest_10_cpy["space^(2^(2^(2^(2^(2^(2^(2^(2^2))))))))"].anim.points.move_to(ORIGIN),
            lag_ratio=0.4,
        )
        self.forward(1.5)
        self.play(
            FadeIn(text_pow_2_nest_10_cpy["2"]),
            text_pow_2_nest_10_cpy["space^(2^(2^(2^(2^(2^(2^(2^(2^2))))))))"].anim.points.move_to(temp_pos_2nests),
        )
        self.play(Write(surround_2))
        self.forward(1.5)
        self.play(FadeOut(surround_2))
        self.play(TransformMatchingDiff(text_pow_2_nest_10_cpy, text_2_knuth_2nest_n_eq_pow_2_nest_n))
        self.forward(2)
        self.play(
            FadeIn(text_2_knuth_2nest_n),
            text_2_knuth_2nest_n_eq_pow_2_nest_n.anim.points.shift(UP * 1),
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_2_knuth_2nest_n,
                text_2_knuth_2nest_n_explain,
                path_arc=PI / 2,
            ),
            rate_func=smooth,
        )
        self.forward(2)
        self.play(
            FadeOut(text_2_knuth_2nest_n_explain),
            FadeOut(text_2_knuth_2nest_n_eq_pow_2_nest_n),
        )

        text_A_knuth_3nest_B = TypstMath("A arrow.t arrow.t arrow.t B").points.scale(2.5).r
        text_3_knuth_3nest_3 = TypstMath("3 arrow.t arrow.t arrow.t 3").points.scale(2.5).r
        text_3_knuth_3nest_3_eq_3_2nest_2nest_3 = TypstMath("3 arrow.t arrow.t arrow.t 3 = 3 arrow.t arrow.t (3 arrow.t arrow.t 3)").points.scale(2.5).r
        text_3_knuth_3nest_3_eq_3_2nest_7dot6 = TypstMath("3 arrow.t arrow.t arrow.t 3 = 3 arrow.t arrow.t (7625597484987)").points.scale(2.5).r
        text_3_knuth_3nest_3_eq_3_2nest_7dot6["7625597484987"].astype(VItem).color.set(color=RED_A).r
        pow_tower_len = 200
        nested_str_3 = "3^(" * (pow_tower_len - 1) + "3^3" + ")" * (pow_tower_len - 1)
        text_3_knuth_3nest_3_eq_3_pow_nearest_inf = TypstMath("3 arrow.t arrow.t arrow.t 3 = " + nested_str_3).points.scale(2.5).r
        delta_pos_knuth_nested_eqs = text_3_knuth_3nest_3_eq_3_2nest_7dot6["="].points.box.center - text_3_knuth_3nest_3_eq_3_pow_nearest_inf["="].points.box.center
        text_3_knuth_3nest_3_eq_3_pow_nearest_inf.points.shift(delta_pos_knuth_nested_eqs)

        self.play(Write(text_A_knuth_3nest_B))
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_A_knuth_3nest_B["A"],
                text_3_knuth_3nest_3["3", 0],
            ),
            TransformMatchingDiff(
                text_A_knuth_3nest_B["arrow.t arrow.t arrow.t"],
                text_3_knuth_3nest_3["arrow.t arrow.t arrow.t"],
            ),
            TransformMatchingDiff(
                text_A_knuth_3nest_B["B"],
                text_3_knuth_3nest_3["3", 1],
            ),
            duration=2,
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_3_knuth_3nest_3,
                text_3_knuth_3nest_3_eq_3_2nest_2nest_3,
                path_arc=PI / 2,
            ),
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_3_knuth_3nest_3_eq_3_2nest_2nest_3,
                text_3_knuth_3nest_3_eq_3_2nest_7dot6,
            ),
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(
                text_3_knuth_3nest_3_eq_3_2nest_7dot6,
                text_3_knuth_3nest_3_eq_3_pow_nearest_inf,
                duration=1,
            ),
            DataUpdater(
                self.camera,
                lambda item, p: item.points.scale(1 - 0.5 * p.alpha) \
                                    .move_to((UP * 30 + RIGHT * 55) * p.alpha),
                at=0.25,
                rate_func=ease_inout_expo,
                duration=1.5,
            ),
            FadeOut(
                text_3_knuth_3nest_3_eq_3_pow_nearest_inf,
                at=0.8,
                duration=1,
            ),
            duration=4,
        )
        self.forward(2)

class s1_5(Timeline):
    """
    uv run janim run s1_NestedSequence.py s1_5 -i
    """
    def construct(self):
        text_a1 = TypstMath("a_1 = 3 arrow.t 3").points.scale(2).r
        text_a1_a2 = TypstMath("a_1 = 3 arrow.t 3 quad a_2 = 3 arrow.t arrow.t 3").points.scale(1.7).r
        text_a1_a3 = TypstMath("a_1 = 3 arrow.t 3 quad a_2 = 3 arrow.t arrow.t 3 quad a_3 = 3 arrow.t arrow.t arrow.t 3").points.scale(1.4).r
        text_a1_an = TypstMath("a_1 = 3 arrow.t 3 quad a_2 = 3 arrow.t arrow.t 3 quad a_3 = 3 arrow.t arrow.t arrow.t 3quad ... quad a_n = 3 underbrace(arrow.t ... arrow.t, n) 3").points.scale(1.1).r
        for t in [text_a1, text_a1_a2, text_a1_a3, text_a1_an]:
            t["a_1"].astype(VItem).color.set(color="#C5F0F1")
            t["arrow.t", ...].astype(VItem).color.set(color="#FFB6B6")
        for t in [text_a1_a2, text_a1_a3, text_a1_an]:
            t["a_2"].astype(VItem).color.set(color="#96E7F3")
            t["arrow.t arrow.t", ...].astype(VItem).color.set(color="#FF7A7A")
        for t in [text_a1_a3, text_a1_an]:
            t["a_3"].astype(VItem).color.set(color="#67DDF4")
            t["arrow.t arrow.t arrow.t", ...].astype(VItem).color.set(color="#FF3F3F")
        text_a1_an["a_n"].astype(VItem).color.set(color="#38D3F6")
        text_a1_an["underbrace(arrow.t ... arrow.t, n)"].astype(VItem).color.set(color="#FF0000")
        text_ackermann_function = TypstDoc(get_typ_doc("ackermann"))
        text_ackermann_function.points.move_to(DOWN * 1)

        self.play(Write(text_a1))
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_a1,
                text_a1_a2,
                path_arc=PI / 2,
            ),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_a1_a2,
                text_a1_a3,
                path_arc=PI / 2,
            ),
            lag_ratio=0.2,
        )
        self.forward(1)
        self.play(
            TransformMatchingDiff(
                text_a1_a3,
                text_a1_an,
                path_arc=PI / 2,
            )
        )
        self.forward(1.5)
        self.play(
            text_a1_an.anim.points.shift(UP * 2),
            Write(text_ackermann_function.get_label("intro").points.shift(DOWN * 0.5).r),
        )
        self.forward(2)
        self.play(
            Write(text_ackermann_function.get_label("calc"))
        )
        self.forward(2)
        self.play(
            Succession(
                text_ackermann_function.get_label("GDef").anim.astype(VItem).glow.set(color=WHITE, alpha=0.5),
                text_ackermann_function.get_label("GDef").anim.astype(VItem).glow.set(color=WHITE, alpha=0),
                text_ackermann_function.get_label("GDef").anim.astype(VItem).glow.set(color=WHITE, alpha=0.5),
                text_ackermann_function.get_label("GDef").anim.astype(VItem).glow.set(color=WHITE, alpha=0),
                duration=2,
            )
        )
        self.forward(2)
        self.play(
            FadeOut(text_a1_an),
            FadeOut(text_ackermann_function)
        )
        self.forward(1)

        big_numbers = [
            "googolplex",
            "moser",
            "g64",
            "c3333",
            "gongulus",
            "g4",
            "tree3",
            "sscg",
            "loader",
            "bb"
        ] # 10 numbers
        number_colors = [
            "#FFF3DD", "#FFDDCF", "#FFC5C0",
            "#FFAFB2", "#FF97A2", "#FF8194",
            "#FF6985", "#FF5377", "#FF3F69",
            BLUE_C,
        ]
        text_big_number = TypstDoc(get_typ_doc("big_numbers").replace("beaver.png", "typ_docs/beaver.png"))
        text_big_numbers = [
            text_big_number.get_label(bn)
            for bn in big_numbers
        ]
        for c, t in zip(number_colors, text_big_numbers):
            t.points.move_to(ORIGIN).scale(1.3).r
            t.astype(VItem).fill.set(color=c)
        image_busy_beaver = ImageItem("typ_docs/beaver.png")
        image_busy_beaver.points.scale(0.5).move_to(
            text_big_number.get_label("beaver_image").points.box.center
        )

        self.play(
            FadeIn(text_big_numbers[0])
        )
        self.forward(1.2)
        text_big_numbers[0].hide()
        text_big_numbers[1].show()
        self.forward(0.8)
        text_big_numbers[1].hide()
        text_big_numbers[2].show()
        self.forward(0.65)
        text_big_numbers[2].hide()
        text_big_numbers[3].show()
        self.forward(0.55)
        text_big_numbers[3].hide()
        text_big_numbers[4].show()
        self.forward(0.4)
        text_big_numbers[4].hide()
        text_big_numbers[5].show()
        self.forward(0.3)
        text_big_numbers[5].hide()
        text_big_numbers[6].show()
        self.forward(0.4)
        text_big_numbers[6].hide()
        text_big_numbers[7].show()
        self.forward(0.5)
        text_big_numbers[7].hide()
        text_big_numbers[8].show()
        self.forward(0.8)
        text_big_numbers[8].hide()
        text_big_numbers[9].show()
        image_busy_beaver.show()
        self.forward(1.5)
        self.play(FadeOut(text_big_numbers[9]), FadeOut(image_busy_beaver))
        self.forward(1)