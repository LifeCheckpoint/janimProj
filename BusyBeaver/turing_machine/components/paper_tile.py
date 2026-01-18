from janim.imports import * # type: ignore
from typing import Self, List

class PaperTileInfinity(Group):
    left_tiles: list[Group]
    right_tiles: list[Group]
    center_tile: Group
    
    def __init__(
            self,
            center: np.ndarray = ORIGIN,
            square_size: float = 1.0,
            lr_squares_count: int = 5,
            origin_index: None | int = None,
            tile_data: None | List[str] = None,
            line_color: str = MAROON_A,
            scaling_rate: float = 0.97,
            text_original_scaling: float = 1,
    ):
        """
        图灵机无限长纸带

        Args:
            center (np.ndarray): 纸带中心位置. 默认为 ORIGIN.
            square_size (float): 每个方格的边长. 默认为 1.0.
            lr_squares_count (int): 左右各显示多少个方格. 默认为 5.
            origin_index (None | int): 原点位置的索引. 默认为 None 表示默认为 tile_data 首点.
            tile_data (None | List[str]): 纸带上的字符数据，默认是 TypstMath. 默认为 None 表示空白纸带 [""].
            line_color (str): 方格边框颜色. 默认为 MAROON_A.
            scaling_rate (float): 纸带向左右拓展的缩小比例. 默认为 0.97.
            text_original_scaling (float): 纸带上字符的默认缩放大小. 默认为 1.
        """
        super().__init__()

        self.square_size = square_size
        self.lr_squares_count = lr_squares_count
        self.line_color = line_color
        self.scaling_rate = scaling_rate
        self.text_original_scaling = text_original_scaling
        self.origin_index = origin_index if origin_index is not None else 0
        self.tile_data = tile_data if tile_data else [""]
        self.center = center
        
        self._build_tiles()

    def _build_tiles(self):
        """
        构建纸带方格组件
        """

        self.center_tile = Group(
            Square(
                side_length=self.square_size
            ).stroke.set(color=self.line_color).r \
             .fill.set(alpha=0).r \
             .points.move_to(self.center).r,
            TypstMath(
                text=self.tile_data[self.origin_index],
            ).points.scale(self.text_original_scaling).r \
             .points.move_to(self.center).r
        )
        
        self.right_tiles = [
            self.center_tile.copy() \
                            .points.scale(self.text_original_scaling * self.scaling_rate**i).r \
                            .points.move_to(
                                self.center + RIGHT * self.square_size * sum(
                                    self.scaling_rate**i for i in range(1, i + 1)
                                )
                            ).r
            for i in range(1, self.lr_squares_count + 1)
        ]
        for i, tile in enumerate(self.right_tiles):
            data_index = self.origin_index + i + 1
            char = self.tile_data[data_index] if data_index < len(self.tile_data) and data_index >= 0 else ""
            tile[1].become(
                TypstMath(
                    text=char,
                ).points.scale(self.text_original_scaling * self.scaling_rate**i).r \
                 .points.move_to(tile.points.box.center).r
            )

        self.left_tiles = 

        # 添加所有方格到 Group 中
        self.add(*reversed(self.left_tiles))
        self.add(self.center_tile)
        self.add(*self.right_tiles)