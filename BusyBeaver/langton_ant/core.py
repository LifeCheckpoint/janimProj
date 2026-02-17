class LangtonAntCore:
    DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 上、右、下、左

    def __init__(self, grid: dict[tuple[int, int], int] | None = None, x=0, y=0, direction=0):
        self.grid: dict[tuple[int, int], int] = dict(grid) if grid else {}
        self.x = x
        self.y = y
        self.dir = direction % 4
        self.steps = 0
        self.min_x = min((k[0] for k in self.grid), default=0)
        self.max_x = max((k[0] for k in self.grid), default=0)
        self.min_y = min((k[1] for k in self.grid), default=0)
        self.max_y = max((k[1] for k in self.grid), default=0)

    def _update_bounds(self, x, y):
        if x < self.min_x: self.min_x = x
        elif x > self.max_x: self.max_x = x
        if y < self.min_y: self.min_y = y
        elif y > self.max_y: self.max_y = y

    def step(self, n=1):
        for _ in range(n):
            pos = (self.x, self.y)
            color = self.grid.get(pos, 0)
            self.dir = (self.dir + (1 if color == 0 else -1)) % 4
            self.grid[pos] = 1 - color
            self.x += self.DIRS[self.dir][0]
            self.y += self.DIRS[self.dir][1]
            self._update_bounds(self.x, self.y)
            self.steps += 1

    def get_map(self) -> tuple[list[list[int]], tuple[int, int]]:
        """返回 (二维网格, 原点在网格中的坐标(row, col))。
        网格 row 0 对应 max_y（上方），col 0 对应 min_x（左侧）。"""
        rows = self.max_y - self.min_y + 1
        cols = self.max_x - self.min_x + 1
        grid = [[0] * cols for _ in range(rows)]
        for (x, y), v in self.grid.items():
            grid[self.max_y - y][x - self.min_x] = v
        origin = (self.max_y, -self.min_x)
        return grid, origin

    def get_grid(self) -> dict[tuple[int, int], int]:
        return dict(self.grid)

    def get_position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_direction(self) -> int:
        return self.dir

    def get_steps(self) -> int:
        return self.steps