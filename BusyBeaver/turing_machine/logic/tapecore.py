from typing import Any, Dict, List, Optional, Tuple, TypeVar, Generic
from pydantic import BaseModel, PrivateAttr, Field


class CellValue(BaseModel):
    """
    纸带单元格的值包装类
    """
    absolute_index: int = Field(..., description="单元格的绝对索引")
    value: Any = Field(default=None, description="单元格的实际值")


T = TypeVar("T")

class InfiniteTape(BaseModel, Generic[T]):
    """
    无限长纸带数据结构

    需通过 set_window_size 方法在初始化后设置窗口大小
    """
    
    # 默认空值，用于初始化或清空时填充
    empty_value: Any = Field(default=None, description="纸当中的默认空值")
    
    # 窗口大小，默认为11 (半径为5)
    initial_window_size: int = Field(default=11, ge=1, description="初始化窗口大小")
    
    # 存储稀疏数据的字典：{绝对索引: 数据}
    _tape_data: Dict[int, T] = PrivateAttr(default_factory=dict)
    
    # 当前指针的绝对索引
    _pointer: int = PrivateAttr(default=0)
    
    # 当前可视窗口中心的绝对索引
    _window_center: int = PrivateAttr(default=0)
    
    # 窗口半径
    _window_radius: int = PrivateAttr(default=5)

    def set_window_size(self, size: Optional[int] = None):
        """
        设置窗口大小。
        
        窗口以中心点向左右延伸。如果 size 为 11，则半径为 5 ([-5, 5])。
        如果 size 为偶数，将自动向下取整计算半径。

        :param size: 可视窗口的总长度。
        :type size: int
        :return: Self
        """
        self._window_radius = (size - 1) // 2 if size is not None else (self.initial_window_size - 1) // 2
        return self

    def reset(self) -> None:
        """
        重置纸带。
        
        纸带内容清空，指针归零，窗口回归原点及默认范围。

        :return: None
        """
        self._tape_data.clear()
        self._pointer = 0
        self._window_center = 0
        # 恢复初始配置的窗口大小
        self.set_window_size(self.initial_window_size)

    def _get_value(self, abs_index: int) -> T | None:
        """内部辅助：根据绝对索引获取值，如果不存在返回默认空值"""
        return self._tape_data.get(abs_index, self.empty_value)

    def __getitem__(self, offset: int) -> CellValue:
        """
        单个读取（下标方式读取）。
        
        根据相对于当前指针的偏移量读取数据。

        :param offset: 相对偏移量。0 表示当前指针位置，-1 表示左移一位。
        :type offset: int
        :return: CellValue 包含绝对索引和对应内容
        :rtype: CellValue
        """
        target_abs_index = self._pointer + offset
        return CellValue(absolute_index=target_abs_index, value=self._get_value(target_abs_index))

    def read_current(self):
        """
        快速读取。
        
        读取当前指针指向的数据（相当于下标[0]）。

        :return: CellValue 包含绝对索引和对应内容
        :rtype: CellValue
        """
        return CellValue(absolute_index=self._pointer, value=self._get_value(self._pointer))

    def __setitem__(self, offset: int, value: T) -> None:
        """
        单个写入（下标方式写入）。
        
        根据相对于当前指针的偏移量写入数据。
        如果写入的值是 empty_value，则从存储中删除该key以节省空间。

        :param offset: 相对偏移量。
        :type offset: int
        :param value: 要写入的数据。
        :type value: T
        :return: None
        """
        target_abs_index = self._pointer + offset
        
        if value == self.empty_value:
            if target_abs_index in self._tape_data:
                del self._tape_data[target_abs_index]
        else:
            self._tape_data[target_abs_index] = value

    def write_current(self, value: T) -> None:
        """
        快速写入。
        
        写入当前指针指向的位置。

        :param value: 要写入的数据。
        :type value: T
        :return: None
        """
        self[0] = value

    def read_absolute(self, abs_index: int) -> Optional[T]:
        """
        单个绝对读取。

        :param abs_index: 绝对索引。
        :type abs_index: int
        :return: 对应内容，若无数据返回默认空值。
        :rtype: Optional[T]
        """
        return self._get_value(abs_index)

    def write_absolute(self, abs_index: int, value: T) -> None:
        """
        单个绝对写入。

        :param abs_index: 绝对索引。
        :type abs_index: int
        :param value: 数据内容。
        :type value: T
        :return: None
        """
        if value == self.empty_value:
            if abs_index in self._tape_data:
                del self._tape_data[abs_index]
        else:
            self._tape_data[abs_index] = value

    def read_window(self) -> List[Optional[T]]:
        """
        窗口读取。
        
        返回当前可视窗口范围内的所有数据。

        :return: 窗口大小长度的数据列表，包含空值。
        :rtype: List[Optional[T]]
        """
        start = self._window_center - self._window_radius
        end = self._window_center + self._window_radius
        
        result = []
        for idx in range(start, end + 1):
            result.append(self._get_value(idx))
        return result

    def write_window(self, data: List[T]) -> None:
        """
        窗口写入。
        
        将列表数据一次性写入当前可视窗口。列表长度应与窗口大小一致。
        如果长度不一致，将只写入重叠部分或截断。

        :param data: 要写入的数据列表。
        :type data: List[T]
        :return: None
        """
        start = self._window_center - self._window_radius
        
        # 遍历输入数据，并写入对应的绝对位置
        for i, val in enumerate(data):
            # 防止写入超出窗口定义的范围
            if i > (self._window_radius * 2): 
                break
            abs_idx = start + i
            self.write_absolute(abs_idx, val)

    def read_batch_absolute(self) -> Tuple[List[Optional[T]], int]:
        """
        批量绝对读取。
        
        读取纸带上最左端非空数据到最右端非空数据之间的所有内容。

        :return: (数据列表, 最左端数据的绝对索引)。如果纸带全空，返回 ([], 0)。
        :rtype: Tuple[List[Optional[T]], int]
        """
        if not self._tape_data:
            return [], 0

        # 获取所有非空的 key 并排序
        keys = sorted(self._tape_data.keys())
        start_idx = keys[0]
        end_idx = keys[-1]
        
        result = []
        for idx in range(start_idx, end_idx + 1):
            result.append(self._get_value(idx))
            
        return result, start_idx

    def write_batch_absolute(self, data: List[T], start_abs_index: int) -> None:
        """
        批量绝对写入。

        :param data: 数据列表。
        :type data: List[T]
        :param start_abs_index: 写入的起始绝对索引。
        :type start_abs_index: int
        :return: None
        """
        for i, val in enumerate(data):
            self.write_absolute(start_abs_index + i, val)

    def move_pointer(self, offset: int) -> int:
        """
        指针左右移。
        
        指针尝试在**当前窗口范围**内移动。如果目标位置超出显示窗口，则不移动。

        :param offset: 期望位移 (正数为右，负数为左，通常为 1 或 -1)。
        :type offset: int
        :return: 实际移动位移 (成功返回 offset, 失败返回 0)。
        :rtype: int
        """
        if offset == 0:
            return 0

        target = self._pointer + offset
        
        # 计算当前窗口边界 [min, max]
        win_min = self._window_center - self._window_radius
        win_max = self._window_center + self._window_radius
        
        if win_min <= target <= win_max:
            self._pointer = target
            return 1 if offset > 0 else -1
        
        return 0

    def move_tape(self, direction: int) -> int:
        """
        纸带左右移

        :param direction: 1 (纸带右移) 或 -1 (纸带左移)。
        :type direction: int
        :return: 纸带移动位移 (1/-1)。
        :rtype: int
        """
        window_movement = -1 * direction
        self._window_center += window_movement
        return direction

    def move_window(self, direction: int) -> int:
        """
        窗口左右移。
        
        窗口左移 (-1)：可视范围的索引减小（相当于纸带右移）。
        窗口右移 (+1)：可视范围的索引增加（相当于纸带左移）。

        :param direction: 1 (窗口右移) 或 -1 (窗口左移)。
        :type direction: int
        :return: 窗口移动位移 (1/-1)。
        :rtype: int
        """
        self._window_center += direction
        return direction


    def count_non_empty_length(self) -> int:
        """
        统计非空纸带长度。
        
        从最左端非空数据到最右端非空数据的跨度个数。

        :return: 跨度长度，全空返回 0。
        :rtype: int
        """
        if not self._tape_data:
            return 0
        
        keys = self._tape_data.keys()
        return max(keys) - min(keys) + 1

    def count_content(self, target: T) -> int:
        """
        统计指定内容个数。
        
        遍历非空纸带，统计内容一致的数据个数。

        :param target: 要统计的目标内容。
        :type target: T
        :return: 出现次数。
        :rtype: int
        """
        count = 0
        for val in self._tape_data.values():
            if val == target:
                count += 1
        return count
    
    def __str__(self) -> str:
        win_data = self.read_window()
        ptr_relative = self._pointer - (self._window_center - self._window_radius)
        
        display = []
        for i, val in enumerate(win_data):
            val_str = str(val) if val != self.empty_value else "_"
            if 0 <= ptr_relative < len(win_data) and i == ptr_relative:
                display.append(f"[{val_str}]")
            else:
                display.append(f" {val_str} ")
                
        return f"Tape(Idx={self._pointer}, WinCenter={self._window_center}): {''.join(display)}"
