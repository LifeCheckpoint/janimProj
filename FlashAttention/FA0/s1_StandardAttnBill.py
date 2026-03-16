import sys
from pathlib import Path
root = Path(__file__).parent.parent
sys.path.append(str(root))

from janim.imports import * # type: ignore

with reloads():
    from components.utils import *
    from components.colors import FAColor
    from components.grid_matrix import *
    from components.memory_bar import *
if TYPE_CHECKING:
    from components.utils import *
    from components.colors import FAColor
    from components.grid_matrix import *
    from components.memory_bar import *

class s1_1(Timeline):
    CONFIG = Config(
        background_color=Color(FAColor.background),
        typst_shared_preamble=get_typ_doc("preamble"),
    )
    def construct(self) -> None:
        
        self.forward(1)