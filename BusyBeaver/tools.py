from pathlib import Path

local_font = ["Judou Sans Hans Bold", "Microsoft YaHei"]

# 修复缓冲区问题
from dowhen import goto
from janim.render.renderer_vitem_plane import VItemPlaneRenderer
source_hash = "f746551d"
goto("if self.vbo_points.size != self.vbo_mapped_points.size:").when(
    VItemPlaneRenderer._update_points_normal,
    "if new_attrs.points is not self.attrs.points \\",
    source_hash=source_hash
)

def get_typ_doc(name: str) -> str:
    return Path(f"typ_docs/{name}.typ").read_text(encoding="utf-8")
