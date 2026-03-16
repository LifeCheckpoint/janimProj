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
    background: str = "#282C34"

    light_text: str = "#F5EFEB"

    c_bohe_cyan: str = "#56B6C2"
    c_huibai_gray: str = "#ABB2BF"
    c_luori_orange: str = "#F4A261"
    c_maisui_yellow: str = "#E5C07B"
    c_shanhu_red: str = "#E06C75"
    c_shuweicao_green: str = "#8A9A86"
    c_wumai_blue: str = "#7E7FA8"
    c_xiangyu_perple: str = "#C678DD"
    c_yinghua_pink: str = "#E5989B"

    query_fill: str = "#B2D1D6"
    key_fill: str = "#FF917A"
    value_fill: str = "#FCC439"
    mask_fill: str = "#86CDB2"

    highlight_fill: str = c_shanhu_red
    tip_fill: str = c_maisui_yellow
    shade_fill: str = c_yinghua_pink
    comment_fill: str = c_shuweicao_green
    rect_important_stroke: str = c_maisui_yellow

    memory_bar_fill_start: str = GREEN_A
    memory_bar_fill_end: str = c_shanhu_red
    memory_bar_fill_overflow: str = RED
    memory_bar_bg_fill: str = c_wumai_blue