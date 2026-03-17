from dataclasses import dataclass
from janim.imports import * # type: ignore

@dataclass
class FAColor:
    """
    FlashAttention颜色配置类

    一般而言保持 1+3 配置：
    - 1 个主笔色 80%
    - 1 个重点色 10%
    - 1 个结构色 5%
    - 1 个警示色 5%
    """
    background_dark: str = "#282C34"
    background_light: str = "#FDF6E3"

    light_text: str = "#FDF6E3"
    dark_text: str = "#2C2325"

    c_bohe_cyan: str = "#56B6C2"
    c_huibai_gray: str = "#ABB2BF"
    c_luori_orange: str = "#F4A261"
    c_maisui_yellow: str = "#E5C07B"
    c_shanhu_red: str = "#E06C75"
    c_shuweicao_green: str = "#8A9A86"
    c_wumai_blue: str = "#7E7FA8"
    c_xiangyu_perple: str = "#C678DD"
    c_yinghua_pink: str = "#E5989B"

    query_fill: str = c_wumai_blue
    query_fill_highlight: str = "#CEE7EA"
    key_fill: str = c_shanhu_red
    key_fill_highlight: str = "#FFE0D9"
    value_fill: str = c_luori_orange
    value_fill_highlight: str = "#FDF1D0"
    mask_fill: str = "#86CDB2"
    score_fill: str = "#e49bb8"
    probability_fill: str = "#72f399"
    output_fill: str = "#72edf3"

    highlight_fill: str = c_shanhu_red
    tip_fill: str = c_maisui_yellow
    shade_fill: str = c_yinghua_pink
    comment_fill: str = c_shuweicao_green
    rect_important_stroke: str = c_maisui_yellow

    memory_bar_fill_start: str = GREEN_B
    memory_bar_fill_end: str = c_luori_orange
    memory_bar_fill_overflow: str = RED
    memory_bar_bg_fill: str = c_wumai_blue