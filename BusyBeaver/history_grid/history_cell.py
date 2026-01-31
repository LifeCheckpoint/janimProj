from janim.imports import * # type: ignore

local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]

class HistoryCell(Group):
    def __init__(
        self,
        value: str,
        square_size: float = 0.6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value = value
        self.square_size = square_size
        
        if value == "1":
            fill_color = BLUE_D
        else:
            fill_color = "#1E2130"
            
        self.rect = Rect(
            square_size,
            square_size,
            fill_color=fill_color,
            fill_alpha=1,
            stroke_color=GREY_A,
            stroke_alpha=0.5,
        )
        
        self.text = Text(value, font=local_font)
        self.text.points.move_to(self.rect)
        
        self.add(self.rect, self.text)