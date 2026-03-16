from janim.imports import * # type: ignore
from .colors import FAColor
from .utils import get_perceptual_gradient_function

class MemoryBar:
    """
    内存占用可视化
    """
    bg: Rect
    bar: Rect
    tip: TypstText
    triangle: Triangle
    stat_text: TypstMath
    progress: ValueTracker
    item: Group

    def __init__(
        self,
        timeline: Timeline,
        width: float = 3.0,
        height: float = 0.1,
        value: float = 0.0,
        tip_text: str = "GPU 显存占用量",
        overflow_max: float = 1.2,
    ):
        self.item = Group()
        self.progress = ValueTracker(value)

        self.bg = Rect(width, height)
        self.bg.fill.set(color=FAColor.memory_bar_bg_fill, alpha=1.0)
        self.bg.stroke.set(alpha=0.0)
        
        self.bar = Rect(width * value, height)
        self.bar.fill.set(color=FAColor.memory_bar_fill_start, alpha=1.0)
        self.bar.stroke.set(alpha=0.0)
        
        def arrange_bar(bar: VItem, p: UpdaterParams | None):
            # 超过 overflow_max 就截断
            cur_val = self.progress.current().get_value()
            cur_val = np.clip(cur_val, 0.0001, overflow_max)
            
            bar.points.set_width(
                width * cur_val,
                stretch=True,
            )
            bar.points.set_height(
                height,
                stretch=True,
            )
            bar.points.align_to(self.bg, LEFT)

            # 继承显隐
            if p:
                vis = timeline.item_appearances[self.bg].is_visible_at(p.global_t)
                if vis:
                    self.bar.show()
                else:
                    self.bar.hide()

            # 继承透明度
            ref_alpha = self.bg.current().fill.get()[0][-1]
            # [0, 1] 和 [1, overflow_max] 颜色插值
            if cur_val <= 1:
                bar.fill.set(
                    color=get_perceptual_gradient_function(
                        [
                            FAColor.memory_bar_fill_start,
                            FAColor.memory_bar_fill_end
                        ]
                    )(cur_val),
                    alpha=ref_alpha,
                )
            else:
                bar.fill.set(
                    color=get_perceptual_gradient_function(
                        [
                            FAColor.memory_bar_fill_end,
                            FAColor.memory_bar_fill_overflow
                        ]
                    )(cur_val),
                    alpha=ref_alpha,
                )
        
        arrange_bar(self.bar, None)
        timeline.play(
            DataUpdater(self.bar, arrange_bar, duration=FOREVER)
        )

        self.triangle = Triangle()
        self.triangle.points.scale(0.15)
        self.triangle.fill.set(color=FAColor.memory_bar_fill_start, alpha=1.0)
        self.triangle.stroke.set(alpha=0.0)

        def arrange_triangle(triangle: VItem, p: UpdaterParams | None):
            triangle.points.next_to(self.bar.current(), DOWN, aligned_edge=RIGHT, buff=0.0)
            triangle.points.shift(RIGHT * triangle.points.box.width / 2)

            # 继承显隐
            if p:
                vis = timeline.item_appearances[self.bg].is_visible_at(p.global_t)
                if vis:
                    self.triangle.show()
                else:
                    self.triangle.hide()

            triangle.fill.set_rgbas(rgbas=self.bar.current().fill.get())
        
        arrange_triangle(self.triangle, None)
        timeline.play(
            DataUpdater(self.triangle, arrange_triangle, duration=FOREVER)
        )

        def get_stat_text(p: UpdaterParams | None):
            stat_text = TypstMath(
                str(round(self.progress.current().get_value() * 100, 0)) + "%"
            )
            stat_text.points.scale(0.9)
            stat_text.points.next_to(self.triangle.current(), DOWN, buff=0.1)
            ref_alpha = self.triangle.current().fill.get()[0][-1]
            stat_text.astype(VItem).fill.set(alpha=ref_alpha)

            # 继承显隐
            if p:
                vis = timeline.item_appearances[self.bg].is_visible_at(p.global_t)
                if vis:
                    stat_text.show()
                else:
                    stat_text = TypstMath("")
            
            # 继承透明度
            if p:
                ref_alpha = self.triangle.current(as_time=p.global_t + 0.001).fill.get()[0][-1]
                stat_text.astype(VItem).fill.set(alpha=ref_alpha)

            return stat_text

        self.stat_text = TypstMath("").hide()
        
        timeline.play(
            ItemUpdater(
                self.stat_text,
                get_stat_text,
                duration=FOREVER
            )
        )
        
        self.tip = TypstText(tip_text)
        self.tip.points.next_to(self.bg, UP, aligned_edge=LEFT, buff=0.1)

        self.item.add(self.bg, self.bar, self.triangle, self.stat_text, self.tip)