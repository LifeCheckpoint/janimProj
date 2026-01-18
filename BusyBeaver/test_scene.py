from janim.imports import * # type: ignore
from turing_machine.components.tape_cell import TapeCell

class PaperTileTest(Timeline):
    """
    uv run janim run test_scene.py PaperTileTest -i
    """

class TapeCellTest(Timeline):
    """
    uv run janim run test_scene.py TapeCellTest -i
    """
    CONFIG = Config(
        pixel_height=2160,
        pixel_width=3840,
    )

    def construct(self):
        ch0 = R"#text(fill: white)[0]"
        cell = TapeCell(tile_data=ch0)
        self.forward()
        self.play(Create(cell))
        self.forward()
        cell.get_chromatic_effect().show()
        self.play(
            cell.create_chromatic_in_updater(duration=4.0, intensity=20)
        )
        self.play(
            cell.stop_chromatic_in_updater(intensity=20)
        )
        self.forward(1)

class RotatingTapeCellTest(Timeline):
    """
    uv run janim run test_scene.py RotatingTapeCellTest -i
    """
    def construct(self):
        tl1 = TapeCellTest().build().to_item().show()
        rotate = TransformableFrameClip(tl1, scale=(0.5, 0.5)).show()
        self.play(
            DataUpdater(
                rotate,
                lambda data, p: data.clip.set(rotate=PI * p.alpha)
            ),
            duration=tl1.duration,
            rate_func=smooth
        )
