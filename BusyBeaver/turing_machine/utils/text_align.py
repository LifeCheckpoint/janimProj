from janim.imports import * # type: ignore
import numpy as np

def _get_textline_mat(line) -> np.matrix:
    right = line.mark.get('right') - line.mark.get('orig')
    up = line.mark.get('up') - line.mark.get('orig')
    return np.matrix([right[:2], up[:2]]).T

def align_text(txt: Text, target: Text) -> None:
    """
    Aligns 'txt' to match the transform (rotation/scale) of 'target'.
    """
    if len(txt) == 0 or len(target) == 0:
        return

    rot = _get_textline_mat(target[0]) @ _get_textline_mat(txt[0]).I
    
    txt.points.shift(-txt[0].mark.get()) \
        .apply_matrix(rot) \
        .shift(target[0].mark.get())
