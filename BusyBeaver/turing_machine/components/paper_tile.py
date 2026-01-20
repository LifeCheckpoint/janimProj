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
    cells_group: Group[TapeCell]
    pointer: SVGItem
    vignette_effect: AlphaVignetteEffect | IdentityEffect
    lens_effect: LensEffect | IdentityEffect

    tape: InfiniteTape[str]
    
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
        self.cell_setting = cell_setting

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
                    index=self.center_at + i,
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
        
    def set_value(self, value: str, glow_time: float = 0.5, wait_time: float = 0.25, transform_time: float = 1):
        """
        设置当前指针位置的格子数据，并获取动画

        :param value: 要设置的字符数据
        :type value: str
        :param glow_time: 发光时间
        :type glow_time: float
        :param wait_time: 等待时间
        :type wait_time: float
        :param transform_time: 变换时间
        :type transform_time: float
        :return: 返回设置动画
        :rtype: Succession

        """
        self.tape.write_current(value)
        return self.cells_group[self.showcase_radius].create_set_value_animation(
            value=value,
            glow_time=glow_time,
            wait_time=wait_time,
            transform_time=transform_time,
            center_scaling=self.center_scaling,
        )
    
    def tape_shift_right(self, duration: float = 1.0) -> Succession:
        """
        将格子整体向右移动一个位置
        """

        # 更新格子数据
        self.tape.move_tape(1)

        def delete_right():
            """
            删除最右边格子
            """
            self.cells_group[-1].hide()
            self.cells_group.remove(self.cells_group[-1])

        def update_refs():
            """
            更新移动后格子引用
            """
            # 格子组插入最左边新格子
            target_offset = -self.showcase_radius
            new_tape = TapeCell(
                square_size=0.8,
                tile_data=self.tape[target_offset].value,
                line_color=WHITE,
                text_scaling=1.0,
                index=self.tape[target_offset].absolute_index,
            ) if not self.cell_setting \
              else self.cell_setting(self.tape[target_offset].absolute_index, self.tape[target_offset].value)
            new_tape.points.next_to(self.cells_group[0], LEFT, buff=0)
            self.cells_group.add(new_tape, insert=True)

        return Succession(
            Do(delete_right), 
            AnimGroup(
                *[
                    self.cells_group[i].anim.points.move_to(self.cells_group[i + 1].points.box.center)
                    for i in range(0, len(self.cells_group) - 1) # type: ignore
                ],
                self.cells_group[self.showcase_radius].anim.points.scale(1 / self.center_scaling), # type: ignore
                self.cells_group[self.showcase_radius - 1].anim.points.scale(self.center_scaling), # type: ignore
                duration=duration,
                rate_func=ease_out_expo,
            ),
            Do(update_refs),
        )
    
    def tape_shift_left(self, duration: float = 1.0) -> Succession:
        """
        将格子整体向左移动一个位置
        """
        # 更新格子数据
        self.tape.move_tape(-1)

        def delete_left():
            """
            删除最左边格子
            """
            self.cells_group[0].hide()
            self.cells_group.remove(self.cells_group[0])

        def update_refs():
            """
            更新移动后格子引用
            """
            # 格子组插入最右边新格子
            target_offset = self.showcase_radius
            new_tape = TapeCell(
                square_size=0.8,
                tile_data=self.tape[target_offset].value,
                line_color=WHITE,
                text_scaling=1.0,
                index=self.tape[target_offset].absolute_index,
            ) if not self.cell_setting \
              else self.cell_setting(self.tape[target_offset].absolute_index, self.tape[target_offset].value)
            new_tape.points.next_to(self.cells_group[-1], RIGHT, buff=0)
            self.cells_group.add(new_tape, insert=False)
        
        return Succession(
            Do(delete_left),
            AnimGroup(
                *[
                    self.cells_group[i].anim.points.move_to(self.cells_group[i - 1].points.box.center)
                    for i in range(len(self.cells_group) - 1, 0, -1) # type: ignore
                ],
                self.cells_group[self.showcase_radius].anim.points.scale(1 / self.center_scaling), # type: ignore
                self.cells_group[self.showcase_radius + 1].anim.points.scale(self.center_scaling), # type: ignore
                duration=duration,
                rate_func=ease_out_expo,
            ),
            Do(update_refs),
        )
