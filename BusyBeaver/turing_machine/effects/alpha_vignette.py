from pathlib import Path
from janim.imports import * # type: ignore

class AlphaVignetteEffect(SimpleFrameEffect):
    def __init__(
        self, 
        *items, 
        vignette_radius=0.8,
        vignette_softness=0.4, 
        vignette_intensity=1.0, 
        aspect_ratio=1.77,
    ):
        """
        晕影效果

        通过 apply_uniforms 动态更新参数

        :param items: 需要应用效果的组件
        :type items: Item
        :param vignette_radius: 晕影半径，默认值为 0.8
        :type vignette_radius: float
        :param vignette_softness: 晕影柔和度，默认值为 0.4
        :type vignette_softness: float
        :param vignette_intensity: 晕影强度，默认值为 1.0
        :type vignette_intensity: float
        :param aspect_ratio: 宽高比，默认值为 1.77
        :type aspect_ratio: float
        """
        super().__init__(
            *items,
            shader=(Path(__file__).parent / "alpha_vignette.glsl").read_text(encoding="utf-8"),
            uniforms=[
                "float vignette_radius",
                "float vignette_softness",
                "float vignette_intensity",
                "float aspect_ratio",
            ]
        )
        
        self.vignette_radius = vignette_radius
        self.vignette_softness = vignette_softness
        self.vignette_intensity = vignette_intensity
        self.aspect_ratio = aspect_ratio

        self.apply_uniforms_set(
            vignette_radius=self.vignette_radius,
            vignette_softness=self.vignette_softness,
            vignette_intensity=self.vignette_intensity,
            aspect_ratio=self.aspect_ratio,
        )

    def apply_uniforms_set(
        self,
        vignette_radius: float | None = None,
        vignette_softness: float | None = None,
        vignette_intensity: float | None = None,
        aspect_ratio: float | None = None,
    ):
        """
        动态设置 uniform 参数

        :param vignette_radius: 晕影半径
        :type vignette_radius: float | None
        :param vignette_softness: 晕影柔和度
        :type vignette_softness: float | None
        :param vignette_intensity: 晕影强度
        :type vignette_intensity: float | None
        :param aspect_ratio: 宽高比
        :type aspect_ratio: float | None
        """
        if vignette_radius is not None:
            self.vignette_radius = vignette_radius
        if vignette_softness is not None:
            self.vignette_softness = vignette_softness
        if vignette_intensity is not None:
            self.vignette_intensity = vignette_intensity
        if aspect_ratio is not None:
            self.aspect_ratio = aspect_ratio

        self.apply_uniforms(
            vignette_radius=self.vignette_radius,
            vignette_softness=self.vignette_softness,
            vignette_intensity=self.vignette_intensity,
            aspect_ratio=self.aspect_ratio,
        )
    