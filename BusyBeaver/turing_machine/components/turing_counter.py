from janim.imports import * # type: ignore
from ..utils.text_align import align_text

local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]

class TuringCounter(Group):
    def __init__(
        self,
        num_digits: int = 4,
        max_value: int = 100,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.num_digits = num_digits
        self.max_value = max_value
        self.current_value = 0
        
        # Background
        self.bg = RoundedRect(3, 1.5, corner_radius=0.1, fill_color="#0B1026", fill_alpha=1, stroke_alpha=0.5, stroke_color=BLUE_E)
        
        # Label
        self.label = Text("步数", font_size=20, color=BLUE_B, font=local_font)
        self.label.points.move_to(self.bg.points.box.top + DOWN * 0.25)
        
        # Number
        self.number_text = Text(str(self.current_value).zfill(self.num_digits), font_size=50, color=WHITE, font=local_font)
        self.number_text.points.next_to(self.label, DOWN, buff=0.1)
        
        # Progress Bar Background
        self.progress_bg = Line(LEFT, RIGHT, color=GREY_D)
        self.progress_bg.points.set_width(2.5)
        self.progress_bg.points.next_to(self.number_text, DOWN, buff=0.3)
        
        # Progress Bar Foreground
        self.progress_fg = Line(LEFT, RIGHT, color=TEAL_C)
        self.progress_fg.points.set_width(0.001)
        self.progress_fg.points.align_to(self.progress_bg, LEFT)
        self.progress_fg.points.set_y(self.progress_bg.points.box.get_y())
        
        # Glow
        self.glow = self.progress_fg.copy()
        self.glow.stroke.set(color=TEAL_C, alpha=0.4)
        self.glow.radius.set(0.08)
        
        self.add(self.bg, self.label, self.number_text, self.progress_bg, self.glow, self.progress_fg)
        
    def set_max_value(self, max_value: int):
        self.max_value = max_value
        
    def set_value(self, value: int):
        self.current_value = value
        new_text = Text(str(value).zfill(self.num_digits), font_size=50, color=WHITE, font=local_font)
        align_text(new_text, self.number_text)
        self.number_text.become(new_text)
        
        progress = min(max(value / self.max_value, 0), 1)
        width = self.progress_bg.points.box.width * progress
        if width < 0.001: width = 0.001
        
        self.progress_fg.points.set_width(width, stretch=True)
        self.progress_fg.points.align_to(self.progress_bg, LEFT)
        self.glow.points.set(self.progress_fg.points.get())
        
    def anim_set_value(self, value: int, duration: float=0.5):
        start_val = self.current_value
        end_val = value
        self.current_value = value
        
        def update_number(p: UpdaterParams):
            val = int(start_val + (end_val - start_val) * p.alpha)
            t = Text(str(val).zfill(self.num_digits), font_size=50, color=WHITE, font=local_font)
            align_text(t, self.number_text)
            return t
            
        def update_bar(data: VItem, p: UpdaterParams):
            val = start_val + (end_val - start_val) * p.alpha
            progress = min(max(val / self.max_value, 0), 1)
            width = self.progress_bg.points.box.width * progress
            if width < 0.001: width = 0.001
            data.points.set_width(width, stretch=True)
            data.points.align_to(self.progress_bg, LEFT)
            
        return AnimGroup(
            ItemUpdater(self.number_text, update_number, duration=duration),
            DataUpdater(self.progress_fg, update_bar, duration=duration),
            DataUpdater(self.glow, lambda data, p: data.points.set(self.progress_fg.current().points.get()), duration=duration, rate_func=ease_out_cubic)
        )
