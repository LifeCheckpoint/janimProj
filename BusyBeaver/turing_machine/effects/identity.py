from pathlib import Path
from janim.imports import * # type: ignore

class IdentityEffect(SimpleFrameEffect):
    def __init__(
        self, 
        *items,
    ):
        """
        空效果

        :param items: 需要应用效果的组件
        :type items: Item
        """
        super().__init__(
            *items,
            shader=(Path(__file__).parent / "identity.glsl").read_text(encoding="utf-8"),
            uniforms=[]
        )
        
        self.apply_uniforms()
