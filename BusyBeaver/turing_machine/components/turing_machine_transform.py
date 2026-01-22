from janim.imports import * # type: ignore
from ..utils.text_align import align_text

local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]
CYAN = "#00FFFF"
PURPLE_BG = "#2D1B4E"
DARK_BLUE_BG = "#0B1026"

class TuringMachineTransform(Group):
    def __init__(
        self,
        width: float = 5.5,
        height: float = 4,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        
        self._build_ui()
        
    def _build_ui(self):
        # Main Background
        self.bg = RoundedRect(
            self.width, 
            self.height, 
            corner_radius=0.1, 
            fill_color=DARK_BLUE_BG, 
            fill_alpha=1, 
            stroke_alpha=0.5, 
            stroke_color=BLUE_E
        )
        
        # Left accent line
        box = self.bg.points.box
        self.accent_line = Line(
            box.get(UL) + RIGHT * 0.05 + DOWN * 0.1,
            box.get(DL) + RIGHT * 0.05 + UP * 0.1,
            color=CYAN,
        )
        
        # Title
        self.title = Text(
            "状态转换 ^_^", 
            font_size=18, 
            color=BLUE_B, 
            font=local_font
        )
        self.title.points.move_to(box.get(UL) + RIGHT * 0.4 + DOWN * 0.4, aligned_edge=LEFT)
        
        # --- Internal State Shift Section ---
        self.state_label = Text("状态变换", font_size=15, color=WHITE, font=local_font)
        self.state_label.points.next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.state_from = Text("状态 _", font_size=24, color=GREY_B, font=local_font)
        self.state_arrow = Text("→", font_size=24, color=WHITE, font=local_font)
        self.state_to = Text("状态 _", font_size=32, color=CYAN, font=local_font)
        # Add glow to state_to
        self.state_to.glow.set(color=CYAN, alpha=0.4, size=0.15)
        
        self.state_group = Group(self.state_from, self.state_arrow, self.state_to)
        self.state_group.points.arrange(RIGHT, buff=0.3)
        self.state_group.points.next_to(self.state_label, DOWN, buff=0.15, aligned_edge=LEFT)
        
        # --- Tape Symbol Rewrite Section ---
        self.symbol_label = Text("纸带数据变换", font_size=15, color=WHITE, font=local_font)
        self.symbol_label.points.next_to(self.state_group, DOWN, buff=0.25, aligned_edge=LEFT)
        
        self.read_text = Text("读取到 [ _ ]", font_size=24, color=GREY_B, font=local_font)
        self.symbol_arrow = Text("→", font_size=24, color=WHITE, font=local_font)
        self.write_text = Text("将写入 [ _ ]", font_size=32, color=CYAN, font=local_font)
        # Add glow to write_text
        self.write_text.glow.set(color=CYAN, alpha=0.4, size=0.15)
        
        self.symbol_group = Group(self.read_text, self.symbol_arrow, self.write_text)
        self.symbol_group.points.arrange(RIGHT, buff=0.15)
        self.symbol_group.points.next_to(self.symbol_label, DOWN, buff=0.15, aligned_edge=LEFT)
        
        # --- Physical Movement Section ---
        self.move_label = Text("纸带移动方向", font_size=15, color=WHITE, font=local_font)
        self.move_label.points.next_to(self.symbol_group, DOWN, buff=0.25, aligned_edge=LEFT)
        
        self.move_display_text = Text("待定 ■", font_size=16, color="#E0B0FF", font=local_font)
        
        btn_w = self.move_display_text.points.box.width + 0.4
        btn_h = self.move_display_text.points.box.height + 0.2
        self.move_bg = RoundedRect(
            btn_w, btn_h, 
            corner_radius=0.05, 
            fill_color=PURPLE_BG, 
            fill_alpha=0.6, 
            stroke_color="#E0B0FF", 
            stroke_alpha=0.4
        )
        self.move_group = Group(self.move_bg, self.move_display_text)
        self.move_display_text.points.move_to(self.move_bg)
        self.move_group.points.next_to(self.move_label, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.add(
            self.bg, self.accent_line, self.title,
            self.state_label, self.state_group,
            self.symbol_label, self.symbol_group,
            self.move_label, self.move_group
        )

    def update_info(
        self, 
        state_from: str, 
        state_to: str, 
        read_symbol: str, 
        write_symbol: str, 
        direction: str
    ):
        # Update State Shift
        new_state_from = Text(f"状态 {state_from}", font_size=24, color=GREY_B, font=local_font)
        new_state_to = Text(f"状态 {state_to}", font_size=32, color=CYAN, font=local_font)
        new_state_to.glow.set(color=CYAN, alpha=0.4, size=0.15)
        
        align_text(new_state_from, self.state_from)
        align_text(new_state_to, self.state_to)
        
        self.state_from.become(new_state_from)
        self.state_to.become(new_state_to)
        
        # Update Symbol Rewrite
        new_read = Text(f"读取到 [ {read_symbol} ]", font_size=24, color=GREY_B, font=local_font)
        new_write = Text(f"将写入 [ {write_symbol} ]", font_size=32, color=CYAN, font=local_font)
        new_write.glow.set(color=CYAN, alpha=0.4, size=0.15)
        
        align_text(new_read, self.read_text)
        align_text(new_write, self.write_text)
        
        self.read_text.become(new_read)
        self.write_text.become(new_write)
        
        # Update Movement
        dir_map = {
            "R": "右移 →",
            "L": "← 左移",
            "S": "停止 ■"
        }
        dir_text = dir_map.get(direction, direction)
        new_move_text = Text(dir_text, font_size=16, color="#E0B0FF", font=local_font)
        align_text(new_move_text, self.move_display_text)
        self.move_display_text.become(new_move_text)

    def anim_update_info(
        self, 
        state_from: str, 
        state_to: str, 
        read_symbol: str, 
        write_symbol: str, 
        direction: str,
        duration: float = 0.5
    ):
        def update_state_from(p: UpdaterParams):
            t = Text(f"状态 {state_from}", font_size=24, color=GREY_B, font=local_font)
            align_text(t, self.state_from)
            return t
            
        def update_state_to(p: UpdaterParams):
            t = Text(f"状态 {state_to}", font_size=32, color=CYAN, font=local_font)
            t.glow.set(color=CYAN, alpha=0.4, size=0.15)
            align_text(t, self.state_to)
            return t
            
        def update_read(p: UpdaterParams):
            t = Text(f"读取到 [ {read_symbol} ]", font_size=24, color=GREY_B, font=local_font)
            align_text(t, self.read_text)
            return t
            
        def update_write(p: UpdaterParams):
            t = Text(f"将写入 [ {write_symbol} ]", font_size=32, color=CYAN, font=local_font)
            t.glow.set(color=CYAN, alpha=0.4, size=0.15)
            align_text(t, self.write_text)
            return t
            
        def update_move(p: UpdaterParams):
            dir_map = {
                "R": "右移 →",
                "L": "← 左移",
                "S": "停止 ■"
            }
            dir_text = dir_map.get(direction, direction)
            t = Text(dir_text, font_size=16, color="#E0B0FF", font=local_font)
            align_text(t, self.move_display_text)
            return t

        return AnimGroup(
            ItemUpdater(self.state_from, update_state_from, duration=duration),
            ItemUpdater(self.state_to, update_state_to, duration=duration),
            ItemUpdater(self.read_text, update_read, duration=duration),
            ItemUpdater(self.write_text, update_write, duration=duration),
            ItemUpdater(self.move_display_text, update_move, duration=duration),
        )
