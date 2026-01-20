from janim.imports import *

CYAN = "#00FFFF"

class GridCell(Group):
    def __init__(
        self,
        state_name: str = "B",
        write_bit: int = 0,
        move_dir: str = "RIGHT",
        is_active: bool = False,
        width: float = 1.8,
        height: float = 2.2,
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
            corner_radius=0.2,
            fill_color="#1E2130",
            fill_alpha=1,
            stroke_alpha=0
        )
        
        # Border
        self.border = RoundedRect(
            self.width,
            self.height,
            corner_radius=0.2,
            fill_alpha=0,
            stroke_color=GREY,
            stroke_alpha=0.3,
        )
        self.border.radius.set(0.02)

        # Content
        self.label = Text("NEXT STATE", font_size=10, color=GREY)
        
        color_map = {
            "A": RED,
            "B": CYAN,
            "C": BLUE,
            "HALT": YELLOW
        }
        state_color = color_map.get(self.state_name, WHITE)
        self.state_text = Text(self.state_name, font_size=40, color=state_color)
        
        self.write_text = Text(f"Write {self.write_bit}", font_size=14, color=GREY_B)
        
        # Direction Button
        dir_map = {
            "RIGHT": "RIGHT →",
            "LEFT": "← LEFT",
            "STOP": "STOP ■"
        }
        dir_str = dir_map.get(self.move_dir, self.move_dir)
        
        self.dir_text = Text(dir_str, font_size=10, color=WHITE)
        
        # Calculate button size based on text
        btn_w = self.dir_text.points.box.width + 0.2
        btn_h = self.dir_text.points.box.height + 0.1
        
        self.dir_bg = RoundedRect(
            btn_w,
            btn_h,
            corner_radius=0.05,
            fill_color="#6A4C93",
            fill_alpha=1,
            stroke_alpha=0
        )
        self.dir_group = Group(self.dir_bg, self.dir_text)
        self.dir_text.points.move_to(self.dir_bg)
        
        # Layout
        center = self.background.points.box.center
        
        # Label at top
        self.label.points.move_to(center + UP * (self.height/2 - 0.3))
        
        # State Name
        self.state_text.points.move_to(center + UP * 0.2)
        
        # Write Text
        self.write_text.points.move_to(center + DOWN * 0.3)
        
        # Button at bottom
        self.dir_group.points.move_to(center + DOWN * (self.height / 2 - 0.4))
        
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
