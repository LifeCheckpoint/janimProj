from pathlib import Path
from janim.imports import * # type: ignore

class LensEffect(SimpleFrameEffect):
    def __init__(
        self, 
        *items, 
        lens_strength=0.2,
        lens_radius=0.5, 
        aspect_ratio=1.77, 
    ):
        """
        透镜效果

        通过 apply_uniforms 动态更新参数

        :param items: 需要应用效果的组件
        :type items: Item
        :param lens_strength: 扭曲强度，正值中心放大，负值中心缩小
        :type lens_strength: float
        :param lens_radius: 透镜作用半径，默认值为 0.5
        :type lens_radius: float
        :param aspect_ratio: 宽高比，默认值为 1.77
        :type aspect_ratio: float
        """
        super().__init__(
            *items,
            shader=(Path(__file__).parent / "lens.glsl").read_text(encoding="utf-8"),
            uniforms=[
                "float lens_strength",
                "float lens_radius",
                "float aspect_ratio",
            ]
        )

        self.lens_strength = lens_strength
        self.lens_radius = lens_radius
        self.aspect_ratio = aspect_ratio

    def apply_uniforms_set(
        self,
        lens_strength: float | None = None,
        lens_radius: float | None = None,
        aspect_ratio: float | None = None,
    ):
        """
        动态设置 uniform 参数

        :param lens_strength: 扭曲强度
        :type lens_strength: float | None
        :param lens_radius: 透镜作用半径
        :type lens_radius: float | None
        :param aspect_ratio: 宽高比
        :type aspect_ratio: float | None
        """
        if lens_strength is not None:
            self.lens_strength = lens_strength
        if lens_radius is not None:
            self.lens_radius = lens_radius
        if aspect_ratio is not None:
            self.aspect_ratio = aspect_ratio

        self.apply_uniforms(
            lens_strength=self.lens_strength,
            lens_radius=self.lens_radius,
            aspect_ratio=self.aspect_ratio,
        )
    