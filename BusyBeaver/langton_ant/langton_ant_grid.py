from janim.imports import *  # type: ignore
from .core import LangtonAntCore

class LangtonAntGrid(Group):
    def __init__(self, cell_size: float = 0.1, pre_alloc: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.cell_size = cell_size
        self.core = LangtonAntCore()
        self.cells: dict[tuple[int, int], Rect] = {}

        self.cells_group = Group()
        self.ant_marker = Triangle(depth=-10).points.scale(cell_size * 0.4).r
        self.ant_marker.stroke.set(color=BLACK, alpha=1)
        self.ant_marker.fill.set(color=WHITE, alpha=1)
        self.ant_marker.points.move_to(self._grid_to_scene(0, 0))

        half = pre_alloc // 2
        for y in range(-half, half):
            for x in range(-half, half):
                rect = Rect(cell_size, cell_size, fill_color=WHITE, fill_alpha=1, stroke_alpha=0)
                rect.points.move_to(self._grid_to_scene(x, y))
                self.cells[(x, y)] = rect
                self.cells_group.add(rect)

        self.add(self.cells_group, self.ant_marker)

    def _grid_to_scene(self, x: float, y: float):
        return RIGHT * x * self.cell_size + UP * y * self.cell_size

    def _ensure_cell(self, x: int, y: int):
        if (x, y) in self.cells:
            return self.cells[(x, y)], False
        rect = Rect(self.cell_size, self.cell_size, fill_color=WHITE, fill_alpha=1, stroke_alpha=0)
        rect.points.move_to(self._grid_to_scene(x, y))
        self.cells[(x, y)] = rect
        self.cells_group.add(rect)
        return rect, True

    def get_step_anim(self, duration: float = 0.3):
        old_x, old_y = self.core.get_position()
        old_color = self.core.grid.get((old_x, old_y), 0)

        self.core.step(1)

        new_x, new_y = self.core.get_position()
        new_color = BLACK if old_color == 0 else WHITE
        rot_delta = -PI / 2 if old_color == 0 else PI / 2
        new_pos = self._grid_to_scene(new_x, new_y)

        old_rect, _ = self._ensure_cell(old_x, old_y)
        new_rect, is_new = self._ensure_cell(new_x, new_y)

        def sync_state():
            old_rect.fill.set(color=new_color, alpha=1)

        anims = []
        if is_new:
            anims.append(FadeIn(new_rect, duration=duration))
        anims.append(old_rect.anim(duration=duration).fill.set(color=new_color))
        anims.append(AnimGroup(
            self.ant_marker.anim(duration=duration).points.rotate(rot_delta),
            self.ant_marker.anim(duration=duration).points.move_to(new_pos),
        ))
        anims.append(Do(sync_state))

        return Succession(*anims)

    def multi_step(self, n: int, duration: float = 1.0):
        """跳步：推进 n 步，返回 AnimGroup 同步所有格子和蚂蚁的视觉状态"""
        old_dir = self.core.get_direction()
        self.core.step(n)

        anims = []
        # 同步所有格子颜色
        for (x, y), v in self.core.get_grid().items():
            if (x, y) in self.cells:
                rect = self.cells[(x, y)]
                new_color = BLACK if v else WHITE
                anims.append(rect.anim(duration=duration).fill.set(color=new_color, alpha=1))

        # 同步蚂蚁位置
        nx, ny = self.core.get_position()
        anims.append(self.ant_marker.anim(duration=duration).points.move_to(self._grid_to_scene(nx, ny)))

        # 同步蚂蚁朝向
        new_dir = self.core.get_direction()
        rot = ((new_dir - old_dir) % 4) * (-PI / 2)
        if rot:
            anims.append(self.ant_marker.anim(duration=duration).points.rotate(rot))

        return AnimGroup(*anims)

    def get_multi_step_anim(self, n: int, duration: float = 0.3):
        return Succession(*(self.get_step_anim(duration) for _ in range(n)))
