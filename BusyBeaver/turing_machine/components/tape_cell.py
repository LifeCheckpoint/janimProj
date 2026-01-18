from janim.imports import * # type: ignore
from ..effects.chromatic import ChromaticEffect
from typing import Self, List

class TapeCell(Group):
    frame: Square
    word: TypstMath
    glowing_effect: ChromaticEffect

    def __init__(
        self,
        center: np.ndarray = ORIGIN,
        square_size: float = 1.0,
        tile_data: None | str = None,
        line_color: str = WHITE,
        text_scaling: float = 1
    ):
        """
        图灵机无限长纸带

        Args:
            center (np.ndarray): 纸带格中心位置. 默认为 ORIGIN.
            square_size (float): 每个方格的边长. 默认为 1.0.
            tile_data (None | str): 纸带上的字符数据，将生成 TypstMath 类型组件.
            line_color (str): 方格边框颜色. 默认为 WHITE.
            text_scaling (float): 纸带上字符的缩放大小. 默认为 1.
        """
        super().__init__()

        self.square_size = square_size
        self.line_color = line_color
        self.text_scaling = text_scaling
        self.tile_data = tile_data
        self.center = center

        self._build_tiles()

        self.glowing_effect = ChromaticEffect(
            self.frame, self.word,
            threshold=1.0,
            radius=0.0,
            intensity=0.0,
        )

    def _build_tiles(self):
        """
        构建纸带方格组件
        """
        self.frame = Square(
            side_length=self.square_size
        ).stroke.set(color=self.line_color).r
        self.frame.points.move_to(self.center)
        self.word = TypstMath(
            text=self.tile_data if self.tile_data else "",
        ).points.scale(self.text_scaling).r
        self.word.points.move_to(self.center)

        self.add(self.frame, self.word)

    def get_chromatic_effect(self) -> ChromaticEffect:
        return self.glowing_effect
    
    def create_chromatic_in_updater(self, duration: float = 1.0, max_radius: float = 1, intensity: float = 10) -> DataUpdater:
        def set_thresholds(data: ChromaticEffect, p):
            data.apply_uniforms_set(
                threshold=0.001,
                radius=max_radius * p.alpha,
                intensity=intensity * p.alpha,
            )
            return data
        
        return DataUpdater(
            self.glowing_effect,
            set_thresholds,
            rate_func=ease_out_expo,
            duration=duration,
        )
    
    def stop_chromatic_in_updater(self, duration: float = 1.0, max_radius: float = 1, intensity: float = 10) -> DataUpdater:
        def reset_thresholds(data: ChromaticEffect, p):
            data.apply_uniforms_set(
                threshold=1.0,
                radius=max_radius * (1 - p.alpha),
                intensity=intensity * (1 - p.alpha),
            )
            return data
        
        return DataUpdater(
            self.glowing_effect,
            reset_thresholds,
            rate_func=ease_in_expo,
            duration=duration,
        )
