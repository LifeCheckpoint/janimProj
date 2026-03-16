from janim.imports import * # type: ignore
from .colors import FAColor

def create_stride_background(
    width: float = 3.0,
    height: float = 3.0,
    color_1: str = FAColor.c_wumai_blue,
    color_2: str = FAColor.background,
    angle: float = PI / 6,
    gap: float = 0.5,
):
    """
    创建斜纹背景

    返回斜纹背景与遮罩
    """
    stripes = Group()
    n_stripes = int(20 // gap) + 2
    for i in range(n_stripes):
        stripe = Rect(20, gap)
        stripe.fill.set(color=color_1 if i % 2 == 0 else color_2, alpha=1.0)
        stripe.stroke.set(alpha=0.0)
        stripes.add(stripe)
    stripes.points.arrange(DOWN, buff=0)
    stripes.points.rotate(angle=angle)

    mask = ShapeMask(
        shape=Rect(width, height),
        affected=[stripes],
    ).show()

    stroke_rect = Rect(width, height)
    stroke_rect.fill.set(alpha=0.0)
    stroke_rect.stroke.set(color=FAColor.c_huibai_gray, alpha=1.0)
    stroke_rect.radius.set(0.03)
    stripes.add(stroke_rect)

    return stripes, mask