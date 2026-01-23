from janim.imports import * # type: ignore

CYAN = "#00FFFF"
local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]

class GridCell(Group):
    def __init__(
        self,
        state_name: str = "B",
        write_bit: int | str = 0,
        move_dir: str = "RIGHT",
        is_active: bool = False,
        width: float = 1.1,
        height: float = 1.1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.state_name = state_name
        self.write_bit = write_bit
        self.move_dir = move_dir
        self.is_active = is_active
        self.width = width
        self.height = height

        self._build_components()
        self.set_active(is_active)

    def _build_components(self):
        # Background
        self.background = RoundedRect(
            self.width,
            self.height,
            corner_radius=0.01,
            fill_color="#1E2130",
            fill_alpha=1,
            stroke_alpha=0,
            depth=100,
        )
        
        # Border
        self.border = RoundedRect(
            self.width,
            self.height,
            corner_radius=0.01,
            fill_alpha=0,
            stroke_color=GREY,
            stroke_alpha=0.3,
            depth=100,
        )

        # Content
        self.label = Text("Next", font_size=9, color=GREY, font=local_font)
        
        self.state_text = Text(self.state_name, font_size=23, font=local_font, format='rich')
        # self.write_text = Text(f"<c #BBBBBB>写入</c> <c #EEEEEE><fs 1.1>{self.write_bit}</fs></c>", format='rich', font_size=14, font=local_font)
        self.write_text = Text(f"<c #EEEEEE><fs 1.1>{self.write_bit}</fs></c>", format='rich', font_size=14, font=local_font)
        
        # Direction Button
        dir_map = {
            "RIGHT": "<c GREEN>→</c>",
            "LEFT": "<c GREEN>←</c>",
            "STOP": "<c RED>■</c>"
        }
        dir_str = dir_map.get(self.move_dir, self.move_dir)
        
        self.dir_text = Text(dir_str, font_size=14, color=WHITE, font=local_font, format='rich')
        
        # Calculate button size based on text
        btn_w = self.dir_text.points.box.width + 0.1
        btn_h = self.dir_text.points.box.height + 0.05
        
        self.dir_bg = RoundedRect(
            btn_w,
            btn_h,
            corner_radius=0.01,
            fill_color="#6A4C93",
            fill_alpha=0,
            stroke_alpha=0,
            depth=10,
        )
        self.dir_group = Group(self.dir_bg, self.dir_text)
        self.dir_text.points.move_to(self.dir_bg)
        
        center = self.background.points.box.center
        self.label.points.move_to(center + UP * (self.height / 2 - 0.15))
        self.state_text.points.move_to(center + UP * 0.15)
        self.write_text.points.move_to(center + DOWN * 0.15)
        self.dir_group.points.move_to(center + DOWN * 0.4)
        
        self.add(self.background, self.border, self.label, self.state_text, self.write_text, self.dir_group)

    def set_active(self, is_active: bool):
        self.is_active = is_active
        if is_active:
            self.border.stroke.set(color=CYAN, alpha=1)
            self.border.radius.set(0.04)
            self.border.glow.set(color=CYAN, alpha=0.6, size=0.2)
        else:
            self.border.stroke.set(color=GREY, alpha=0.3)
            self.border.radius.set(0.02)
            self.border.glow.set(alpha=0)

    def animate_active(self, active: bool, duration: float = 0.5):
        self.is_active = active
        if active:
            return AnimGroup(
                self.border.anim(duration=duration).stroke.set(color=CYAN, alpha=1), # type: ignore
                self.border.anim(duration=duration).radius.set(0.04), # type: ignore
                self.border.anim(duration=duration).glow.set(color=CYAN, alpha=0.6, size=0.2), # type: ignore
            )
        else:
            return AnimGroup(
                self.border.anim(duration=duration).stroke.set(color=GREY, alpha=0.3), # type: ignore
                self.border.anim(duration=duration).radius.set(0.02), # type: ignore
                self.border.anim(duration=duration).glow.set(alpha=0), # type: ignore
            )
