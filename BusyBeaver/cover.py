from janim.imports import * # type: ignore
from tools import get_typ_doc, local_font
import math

class cover(Timeline):
    """
    uv run janim run cover.py cover -i
    """
    CONFIG = Config(
        typst_shared_preamble=get_typ_doc("preamble")
    )
    def construct(self) -> None:
        def make_concave_lens_transform(
            strength: float = 0.15,
            radius: float = 1.0,
            center: np.ndarray | None = None,
        ) -> Callable[[np.ndarray], Vect]:
            if center is None:
                center = np.zeros(3)
            center = np.asarray(center, dtype=float)
            def transform(p: np.ndarray) -> Vect:
                p = np.asarray(p, dtype=float)
                q = p - center
                x, y, z = q
                r = np.hypot(x, y)
                # 凹透镜式径向压缩：离中心越远，缩得越多
                scale = 1.0 / (1.0 + strength * (r / radius) ** 2)
                return center + np.array([x * scale, y * scale, z], dtype=float)
            return transform

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
        glow_size = 0.5
        glow_alpha=0.2
        bb_lines = Group(*[
            DashedLine(bb_pts[i], bb_pts[i + 1]) \
                .color.set(color=YELLOW, alpha=0.5).r \
                .astype(VItem).glow.set(alpha=glow_alpha, size=glow_size).r
            for i in range(4)
        ])
        label_bb = TypstMath("\"BB\"(n)").points.scale(1.2).r
        label_bb.astype(VItem).color.set(color=YELLOW)
        label_bb.points.next_to(bb_pts[-1], UP, buff=0.2)
        label_bb.points.shift(RIGHT * 1.25 + UP * 1.5).scale(1.5)
        label_bb.astype(VItem).glow.set(alpha=glow_alpha, size=glow_size)

        self.play(Write(axes), duration=0.5)
        for name in ["n^2", "2^n", "n!"]:
            self.play(Write(seq_groups[name]), Write(seq_labels[name]), duration=0.5)
        bb4_top = np.array(bb_pts[-1]).copy()
        bb4_top[1] = axes.coords_to_point(0, 150)[1]
        line_vert = DashedLine(bb_pts[-1], bb4_top) \
            .color.set(color=YELLOW, alpha=0.7).r \
            .astype(VItem).glow.set(alpha=glow_alpha, size=glow_size).r
        arrow_up = Arrow(
            bb4_top, bb4_top + UP * 0.8,
            color=YELLOW, buff=0,
        ).astype(VItem).glow.set(alpha=glow_alpha, size=glow_size).r

        text_bb_n = Text("BB(n)", font=local_font, depth=-20)
        text_bb_n.points.scale(8)
        text_increse = Text("增长最快的数列", font=local_font, depth=-20)
        text_increse.points.scale(6).next_to(text_bb_n, DOWN, aligned_edge=LEFT, buff=0.5)
        Group(text_bb_n, text_increse).points.apply_point_fn(
            make_concave_lens_transform(strength=0.01, radius=5),
            about_point=text_increse.points.box.center
        )
        Group(text_bb_n, text_increse).points.rotate(PI / 6, axis=UP, about_edge=LEFT).shift(LEFT * 3 + UP * 2)

        beaver_svg = SVGItem("resources/beaver.svg")
        beaver_svg.points.scale(0.5).move_to(RIGHT * 5.5 + UP * 0.5)

        bb_1 = TypstMath("1")
        bb_2 = TypstMath("6")
        bb_3 = TypstMath("21")
        bb_4 = TypstMath("107")
        bb_5 = TypstMath("47176870")
        bb_6 = TypstMath("?")
        for i, bb in enumerate([bb_1, bb_2, bb_3, bb_4, bb_5, bb_6]):
            bb.astype(VItem).color.set(color=YELLOW)
            bb.points.next_to(axes.coords_to_point(i + 1, 0), DOWN, buff=0.25)
            bb.astype(VItem).glow.set(alpha=glow_alpha / 2, size=glow_size)
            # t = TypstMath(f"\"BB\"({i + 1})")
            # t.points.next_to(bb, DOWN, buff=0.1)
            # t.astype(VItem).color.set(color=YELLOW_A)
            # t.astype(VItem).glow.set(alpha=glow_alpha / 2, size=glow_size)
            # t.show()

        for d in bb_dots:
            d.show()
        for ll in bb_lines:
            ll.show()
        label_bb.show()
        line_vert.show()
        arrow_up.show()
        text_bb_n.show()
        bb_1.show()
        bb_2.show()
        bb_3.show()
        bb_4.show()
        bb_5.show()
        bb_6.show()
        text_increse.show()
        beaver_svg.show()
        self.forward(1.5)
