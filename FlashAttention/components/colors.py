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

    # A100 架构图配色
    a100_label_light: str = "#E6EDF3"
    a100_label_dim: str = "#C7D5E0"
    a100_label_mid: str = "#D5DEE6"
    a100_label_memory_ctrl: str = "#D0D9E2"
    a100_label_l2: str = "#EAF2F8"
    a100_label_nvlink: str = "#F0FFF4"
    a100_label_giga_dark: str = "#1C232B"

    a100_tpc_cell_fill: str = "#2A2F36"
    a100_tpc_cell_stroke: str = "#59616A"
    a100_tpc_sm_fill: str = "#356EA3"
    a100_tpc_compute_fill: str = "#4BA11E"
    a100_tpc_bus_fill: str = "#9B6B34"

    a100_gpc_shell_fill: str = "#2E333A"
    a100_gpc_shell_stroke: str = "#7A828C"
    a100_gpc_bar_fill: str = "#1F252D"
    a100_gpc_bar_stroke: str = "#67717C"
    a100_gpc_link_fill: str = "#3D5B75"

    a100_mem_ctrl_fill: str = "#22272E"
    a100_mem_ctrl_stroke: str = "#646C76"

    a100_hbm_fill: str = "#3A3F46"
    a100_hbm_stroke: str = "#5D6670"
    a100_side_link: str = "#D5DEE6"

    a100_l2_fill: str = "#6FA8CF"
    a100_l2_stroke: str = "#9EC5E2"
    a100_l2_split_fill: str = "#1B2027"

    a100_hub_fill: str = "#3A3F46"
    a100_hub_stroke: str = "#6B737D"

    a100_nvlink_fill: str = "#00D43A"
    a100_nvlink_stroke: str = "#43EE67"

    a100_pci_fill: str = "#2F343C"
    a100_pci_stroke: str = "#69727D"

    a100_giga_fill: str = "#E58A2B"
    a100_giga_stroke: str = "#F2B26A"

    a100_center_spine_fill: str = "#1A2027"
    a100_die_bg_fill: str = "#20252B"
    a100_die_bg_stroke: str = "#5D6670"
    a100_chip_border_stroke: str = "#9099A3"

    # A100 SM 架构图配色
    a100_sm_shell_fill: str = a100_gpc_shell_fill
    a100_sm_shell_stroke: str = a100_gpc_shell_stroke
    a100_sm_panel_fill: str = "#24303D"
    a100_sm_panel_stroke: str = "#5A6675"

    a100_sm_l1i_fill: str = a100_l2_fill
    a100_sm_l0i_fill: str = a100_l2_fill
    a100_sm_warp_fill: str = a100_giga_fill
    a100_sm_dispatch_fill: str = a100_tpc_bus_fill
    a100_sm_register_fill: str = "#1E5D78"

    a100_sm_int32_fill: str = "#3F7A2A"
    a100_sm_fp32_fill: str = "#58A82A"
    a100_sm_fp64_fill: str = "#355A22"
    a100_sm_tensor_fill: str = "#4B8A00"

    a100_sm_ldst_fill: str = "#7A3A3A"
    a100_sm_sfu_fill: str = "#8B2D2D"
    a100_sm_tex_fill: str = "#2E5DB0"
    a100_sm_l1d_fill: str = a100_l2_fill