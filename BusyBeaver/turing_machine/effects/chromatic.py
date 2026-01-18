from pathlib import Path
from janim.imports import * # type: ignore

class ChromaticEffect(FrameEffect):
    def __init__(
        self, 
        *items, 
        threshold=0.2, 
        radius=0.01, 
        intensity=1.5, 
        glow_color=Color(WHITE),
        **kwargs
    ):
        shader_code = (Path(__file__).parent / "chromatic.glsl").read_text(encoding="utf-8")
        super().__init__(*items, fragment_shader=shader_code, **kwargs)
        
        self.glow_threshold = threshold
        self.glow_radius = radius
        self.glow_intensity = intensity
        self.glow_color = glow_color

    def dynamic_uniforms(self) -> dict:
        return {
            "threshold": self.glow_threshold,
            "radius": self.glow_radius,
            "intensity": self.glow_intensity,
            "glow_color": [*self.glow_color.rgb, 1.0], # 转换颜色为 vec4
            "fbo": 0
        }
