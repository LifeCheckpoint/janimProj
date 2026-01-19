from janim.imports import * # type: ignore
from ..effects.chromatic import ChromaticEffect

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
        text_scaling: float = 1.2
    ):
        """
        图灵机纸带方格

        :param center: 纸带格中心位置
        :type center: np.ndarray
        :param square_size: 每个方格的边长
        :type square_size: float
        :param tile_data: 纸带上的字符数据，将生成 TypstMath 类型组件
        :type tile_data: None | str
        :param line_color: 方格边框颜色
        :type line_color: str
        :param text_scaling: 纸带上字符的缩放大小
        :type text_scaling: float
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

    def _set_new_word(self, new_word: TypstMath):
        """
        设置新的字符组件
        """
        self.remove(self.word)
        self.word = new_word
        self.add(self.word)

    def create_set_value_animation(self, value: str, glow_time: float = 0.5, wait_time: float = 0.25, transform_time: float = 1.0) -> Succession:
        """
        获取设置方格字符值的动画
        
        :param value: 字符值
        :type value: str
        :param glow_time: 发光时间，默认值为 0.5
        :type glow_time: float
        :param wait_time: 等待时间，默认值为 0.25
        :type wait_time: float
        :param transform_time: 变换时间，默认值为 1.0
        :type transform_time: float
        :return: Succession 动画序列
        :rtype: Succession
        """
        self.tile_data = value
        new_word = TypstMath(
            text=self.tile_data,
        ).points.scale(self.text_scaling).r
        
        return Succession(
            DataUpdater(
                self.frame,
                lambda item, p: item.glow.set(color=YELLOW, alpha=0.5 * p.alpha, size=0.3 * p.alpha).r,
                duration=glow_time,
            ),
            Wait(wait_time),
            Transform(
                self.word,
                new_word,
                duration=transform_time,
            ),
            Wait(wait_time),
            DataUpdater(
                self.frame,
                lambda item, p: item.glow.set(color=YELLOW, alpha=0.5 * (1 - p.alpha), size=0.3 * (1 - p.alpha)).r,
                duration=glow_time,
            ),
            Do(lambda: self._set_new_word(new_word)),
        )

    def create_clear_value_animation(self, wiggle_time: float = 0.15, wait_time: float = 0.25, transform_time: float = 1.0) -> Succession:
        """
        获取清除方格字符值的动画

        :param wiggle_time: 单次抖动时间，默认值为 0.15
        :type wiggle_time: float
        :param wait_time: 等待时间，默认值为 0.25
        :type wait_time: float
        :param transform_time: 变换时间，默认值为 1.0
        :type transform_time: float
        :return: Succession 动画序列
        :rtype: Succession
        """
        self.tile_data = ""
        new_word = TypstMath(
            text=self.tile_data,
        ).points.scale(self.text_scaling).r

        return Succession(
            Rotate(self, angle=PI / 12, duration=wiggle_time / 2, rate_func=smooth),
            Rotate(self, angle=-PI / 6, duration=wiggle_time, rate_func=smooth),
            Rotate(self, angle=PI / 6, duration=wiggle_time, rate_func=smooth),
            Rotate(self, angle=-PI / 12, duration=wiggle_time / 2, rate_func=smooth),
            Wait(wait_time),
            FadeOut(
                self.word,
                duration=transform_time,
            ),
            Do(lambda: self._set_new_word(new_word)),
        )

    def get_chromatic_effect(self) -> ChromaticEffect:
        """
        获取色差效果组件
        """
        return self.glowing_effect
    
    def create_chromatic_in_updater(self, duration: float = 1.0, max_radius: float = 1, intensity: float = 10) -> DataUpdater:
        """
        创建色差扩大效果的 DataUpdater
        
        :param duration: 效果持续时间，默认值为 1.0
        :type duration: float
        :param max_radius: 最大半径，默认值为 1
        :type max_radius: float
        :param intensity: 效果强度，默认值为 10
        :type intensity: float
        :return: DataUpdater
        :rtype: DataUpdater
        """
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
        """
        创建色差收缩效果的 DataUpdater

        :param duration: 效果持续时间，默认值为 1.0
        :type duration: float
        :param max_radius: 最大半径，默认值为 1
        :type max_radius: float
        :param intensity: 效果强度，默认值为 10
        :type intensity: float
        :return: DataUpdater
        :rtype: DataUpdater
        """
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
