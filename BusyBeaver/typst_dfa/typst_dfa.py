import json
from pydantic import BaseModel, ConfigDict
from pathlib import Path
from janim.imports import * # type: ignore

class DFAInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dfa_main_item: TypstText
    circle_item: dict[str, list[int]]
    text_item: dict[str, list[int]]

def load_dfa_typst(name: str):
    typ = (Path(__file__).parent / "dfa_source" / f"{name}.typ").read_text(encoding="utf-8")
    json_path = Path(__file__).parent / "dfa_source" / f"{name}.json"

    typ_item = TypstText(typ)
    map_item = json.loads(json_path.read_text(encoding="utf-8")) if json_path.exists() else {}

    return DFAInfo(
        dfa_main_item=typ_item,
        circle_item=map_item.get("circle", {}),
        text_item=map_item.get("text", {}),
    )
