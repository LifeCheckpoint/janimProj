from pathlib import Path

def get_typ_doc(name: str) -> str:
    return Path(f"typ_docs/{name}.typ").read_text(encoding="utf-8")
