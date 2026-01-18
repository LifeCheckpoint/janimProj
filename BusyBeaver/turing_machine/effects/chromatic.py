from pathlib import Path
from janim.imports import * # type: ignore

class ChromaticEffect(SimpleFrameEffect):
    def __init__(
        self, 
        *items, 
        threshold=0.2, 
        radius=0.01, 
        intensity=1.5, 
        glow_color=Color(WHITE),
    ):
        """
        色散效果

        通过 apply_uniforms 动态更新参数

        :param items: 需要应用效果的组件
        :param threshold: 色散部分光阈值，低于该值的部分将开始发光
        :param radius: 发散半径，控制发光的扩散范围
        :param intensity: 发散发光强度，控制发光的亮度
        :param glow_color: 发光颜色
        """
        super().__init__(
            *items,
            shader=(Path(__file__).parent / "chromatic.glsl").read_text(encoding="utf-8"),
            uniforms=[
                "float threshold",
                "float radius",
                "float intensity",
                "vec4 glow_color"
            ]
        )
        
        self.threshold = threshold
        self.radius = radius
        self.intensity = intensity
        self.glow_color = glow_color

    def apply_uniforms_set(
        self,
        threshold: float | None = None,
        radius: float | None = None,
        intensity: float | None = None,
        glow_color: Color | None = None,
    ):
        """
        动态设置 uniform 参数

        :param threshold: 色散部分光阈值
        :param radius: 发散半径
        :param intensity: 发散发光强度
        :param glow_color: 发光颜色
        """
        if threshold is not None:
            self.threshold = threshold
        if radius is not None:
            self.radius = radius
        if intensity is not None:
            self.intensity = intensity
        if glow_color is not None:
            self.glow_color = glow_color

        self.apply_uniforms(
            threshold=self.threshold,
            radius=self.radius,
            intensity=self.intensity,
            glow_color=[*self.glow_color.rgb, 1.0],
        )
    