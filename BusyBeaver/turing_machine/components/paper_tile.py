from janim.imports import * # type: ignore
from typing import Callable, cast
from ..effects.alpha_vignette import AlphaVignetteEffect
from ..effects.identity import IdentityEffect
from ..effects.lens import LensEffect
from ..logic.tapecore import InfiniteTape
from .tape_cell import TapeCell

class InfinityTapeItem(Group):
    """
    无限长纸带 Item

    该类仅用于显示范围半径内的格子组件，并同步 Tape 的部分操作
    """
    cells_group: Group[VItem]
    pointer: SVGItem
    vignette_effect: AlphaVignetteEffect | IdentityEffect
    lens_effect: LensEffect | IdentityEffect
    left_temp_cell: TapeCell
    right_temp_cell: TapeCell
    
    def __init__(
        self,
        showcase_radius: int = 7,
        tape_center_at: np.ndarray = ORIGIN,
        init_tape: InfiniteTape | None = None,
        center_at: None | int = None,
        center_scaling: float = 1.2,
        cell_setting: Callable[[int, str], TapeCell] | None = None,
        vignette_setting: Callable[[Item], AlphaVignetteEffect] | None = None,
        lens_setting: Callable[[Item], LensEffect] | None = None,
    ):
        """
        无限长纸带 Item

        :param showcase_radius: 展示范围半径，表示从中心向左和向右各展示多少个格子
        :type showcase_radius: int
        :param tape_center_at: 纸带组件中心位置
        :type tape_center_at: np.ndarray
        :param init_tape: 初始化的无限纸带数据
        :type init_tape: InfiniteTape | None
        :param center_at: 组件中心所对应的纸带绝对位置索引，默认为 None 表示纸带当前指针位置
        :type center_at: None | int
        :param center_scaling: 中心格子的缩放比例
        :type center_scaling: float
        :param cell_setting: 纸带格子组件设置函数，接收绝对索引和对应字符数据作为参数并返回 TapeCell 实例
        :type cell_setting: Callable[[int, str], TapeCell] | None
        :param vignette_setting: 晕影效果设置函数，接收当前 Item 作为参数并返回 AlphaVignetteEffect 实例
        :type vignette_setting: Callable[[Item], AlphaVignetteEffect] | None
        :param lens_setting: 镜头效果设置函数，接收当前 Item 作为参数并返回 LensEffect 实例
        :type lens_setting: Callable[[Item], LensEffect] | None
        """
        super().__init__()

        self.showcase_radius = showcase_radius
        self.tape = init_tape if init_tape else InfiniteTape[str](empty_value="", initial_window_size=showcase_radius * 2 + 1).set_window_size()
        self.center_at = center_at if center_at is not None else self.tape.read_current().absolute_index
        self.center_scaling = center_scaling

        self.cells_group = Group(depth=10)
        self.pointer = SVGItem(
            file_path=str(Path(__file__).parent.parent / "svgs" / "pointer.svg"),
            scale=1.0,
        )

        for i in range(-self.showcase_radius, self.showcase_radius + 1):
            if not cell_setting:
                cell = TapeCell(
                    square_size=0.8,
                    tile_data=self.tape[i].value,
                    line_color=WHITE,
                    text_scaling=1.0,
                )
            else:
                cell = cell_setting(self.center_at + i, self.tape[i].value)
            
            # 中间 Cell 稍大一些，表示当前正中央位置
            if i == 0:
                cell.points.scale(self.center_scaling)

            self.cells_group.add(cell)

        # 排列格子
        self.cells_group[showcase_radius].points.move_to(tape_center_at)
        Group(*self.cells_group[0:showcase_radius]) \
            .points.arrange_in_grid(
                n_rows=1,
                n_cols=self.showcase_radius,
                buff=0,
            ).r \
            .points.next_to(self.cells_group[showcase_radius], LEFT, buff=0)
        Group(*self.cells_group[showcase_radius + 1:]) \
            .points.arrange_in_grid(
                n_rows=1,
                n_cols=self.showcase_radius,
                buff=0,
            ).r \
            .points.next_to(self.cells_group[showcase_radius], RIGHT, buff=0)

        self.pointer.points.next_to(self.cells_group[showcase_radius], UP, buff=0.5)
        
        self.add(self.cells_group, self.pointer)

        # 应用 shader 序列
        if lens_setting is not None:
            self.lens_effect = lens_setting(self.cells_group).show()
        else:
            self.lens_effect = IdentityEffect(self.cells_group).show()

        if vignette_setting is not None:
            self.vignette_effect = vignette_setting(Group(self.lens_effect, self.pointer)).show()
        else:
            self.vignette_effect = IdentityEffect(Group(self.lens_effect, self.pointer)).show()

        # 将最后一个 shader effect 添加到当前 Group
        self.add(self.vignette_effect.show())
        