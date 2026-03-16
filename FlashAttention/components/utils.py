from __future__ import annotations
from janim.imports import TypstDoc
from pathlib import Path
from typing import Any
from typing import Callable
import numpy as np

local_font = ["Judou Sans Hans", "Microsoft YaHei"]
CYAN = "#00FFFF"

def get_typ_doc(name: str) -> str:
    return Path(f"typ_docs/{name}.typ").read_text(encoding="utf-8")

def hex_to_rgb(hex_str):
    """将十六进制转换为 [0, 1] 的线性 RGB"""
    hex_str = hex_str.lstrip('#')
    rgb = tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    # sRGB 转 Linear RGB (Gamma 校正逆转)
    return [(c / 12.92) if c <= 0.04045 else ((c + 0.055) / 1.055)**2.4 for c in rgb]

def rgb_to_hex(rgb):
    """将 [0, 1] 的线性 RGB 转换为十六进制"""
    # Linear RGB 转 sRGB (Gamma 校正)
    srgb = [(12.92 * c) if c <= 0.0031308 else (1.055 * (c**(1/2.4)) - 0.055) for c in rgb]
    res = [max(0, min(255, int(c * 255 + 0.5))) for c in srgb]
    return "#{:02x}{:02x}{:02x}".format(*res)

def linear_srgb_to_oklab(r, g, b):
    """将线性 sRGB 转换为 Oklab 空间"""
    l_ = 0.4122214708 * r + 0.5363320963 * g + 0.0514459450 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l, m, s = np.cbrt(l_), np.cbrt(m_), np.cbrt(s_)

    return [
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    ]

def oklab_to_linear_srgb(L, a, b):
    """将 Oklab 空间转换回线性 sRGB"""
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b)**3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b)**3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b)**3

    return [
        +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    ]

def get_perceptual_gradient_function(color_list: list[str]) -> Callable[[float], str]:
    """
    输入十六进制列表，返回一个函数 f(t) -> hex
    t 在 0 到 1 之间
    """
    # 预处理：将所有颜色转到 Oklab 空间
    oklab_colors = []
    for hex_c in color_list:
        lin_rgb = hex_to_rgb(hex_c)
        oklab = linear_srgb_to_oklab(*lin_rgb)
        oklab_colors.append(oklab)
    
    oklab_colors = np.array(oklab_colors)
    n = len(oklab_colors)

    def gradient_func(t):
        t = max(0.0, min(1.0, t))
        if t == 1:
            return color_list[-1]
        
        # 确定处于哪两个颜色之间
        scaled_t = t * (n - 1)
        idx = int(np.floor(scaled_t))
        local_t = scaled_t - idx
        
        # 在 Oklab 空间进行线性插值
        c1 = oklab_colors[idx]
        c2 = oklab_colors[idx + 1]
        
        interp_lab = c1 * (1 - local_t) + c2 * local_t
        
        # 转回十六进制
        lin_rgb = oklab_to_linear_srgb(*interp_lab)
        return rgb_to_hex(lin_rgb)

    return gradient_func

def typst_complement(doc: TypstDoc, *patterns: TypstDoc | Any):
    covered = set()
    for p in patterns:
        pat = doc.typstify(p)
        for i in doc.indices(pat):
            covered.update(range(i, i + len(pat)))
    return doc[[i not in covered for i in range(len(doc))]]
