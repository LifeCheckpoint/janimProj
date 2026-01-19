from janim.imports import * # type: ignore
from turing_machine.components.tape_cell import TapeCell
from turing_machine.effects.alpha_vignette import AlphaVignetteEffect
from turing_machine.effects.lens import LensEffect
from turing_machine.effects.identity import IdentityEffect
from turing_machine.components.paper_tile import InfinityTapeItem
from turing_machine.logic.tapecore import InfiniteTape
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

class TapeCellTest2(Timeline):
    """
    uv run janim run test_scene.py TapeCellTest2 -i
    """
    def construct(self):
        ch0 = R"#text(fill: white)[0]"
        ch1 = R"#text(fill: red)[1]"
        ch2 = R"#text(fill: blue)[2]"
        ch3 = R"#text(fill: green)[3]"
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
        self.play(
            cell.create_set_value_animation(ch1)
        )
        self.forward(1)
        self.play(
            cell.create_set_value_animation(ch2)
        )
        self.forward(1)
        self.play(
            cell.create_set_value_animation(ch3)
        )
        self.forward(1)
        self.play(
            cell.create_clear_value_animation()
        )
        self.forward(1)

class AlphaVignetteEffectTest(Timeline):
    """
    uv run janim run test_scene.py AlphaVignetteEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2).fill.set(color=BLUE, alpha=1).r
        vignette = AlphaVignetteEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        vignette.show()
        self.forward(2)
        self.play(
            DataUpdater(
                vignette,
                lambda item, p: item.apply_uniforms_set(
                    vignette_radius=0.8 - 0.5 * p.alpha,
                    vignette_softness=0.4,
                    vignette_intensity=1.0 + 2.0 * p.alpha,
                    aspect_ratio=1.77,
                ),
            ),
            duration=4.0,
            rate_func=smooth
        )

class LensEffectTest(Timeline):
    """
    uv run janim run test_scene.py LensEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2)
        lens = LensEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        lens.show()
        self.forward(2)
        self.play(
            DataUpdater(
                lens,
                lambda item, p: item.apply_uniforms_set(
                    lens_radius=0.5 + 0.3 * p.alpha,
                    lens_strength=0.5 + 1.5 * p.alpha,
                    aspect_ratio=1.77,
                ),
            ),
            duration=4.0,
            rate_func=smooth
        )

class ShaderTransformTest(Timeline):
    """
    uv run janim run test_scene.py ShaderTransformTest -i
    """
    def construct(self):
        rect1 = Rect(2, 3).stroke.set(color=RED).r
        rect2 = Rect(3, 2).stroke.set(color=BLUE).r
        LensEffect(rect1).show()
        LensEffect(rect2).show()
        self.play(Create(rect1))
        self.forward(1)
        self.play(Transform(rect1, rect2))
        self.forward(1)

class IdentityEffectTest(Timeline):
    """
    uv run janim run test_scene.py IdentityEffectTest -i
    """
    def construct(self):
        rect2 = Rect(20, 20).fill.set(color=RED, alpha=1).r
        rect = Rect(4, 2)
        identity = IdentityEffect(rect)
        self.play(Create(rect2))
        self.forward()
        self.play(Create(rect))
        self.forward(2)
        identity.show()
        self.forward(4)

class InfinityTapeItemTest(Timeline):
    """
    uv run janim run test_scene.py InfinityTapeItemTest -i
    """
    def construct(self):
        tape = InfiniteTape[str](empty_value="", initial_window_size=11)
        tape.write_batch_absolute(start_abs_index=-2, data=["A", "B", "C_0", "D_1", "E", "F", "G"])
        tape.move_pointer(1)
        tape_item = InfinityTapeItem(
            showcase_radius=5,
            tape_center_at=DOWN * 1,
            init_tape=tape,
            cell_setting=lambda _, value: TapeCell(
                square_size=0.8,
                tile_data=value,
                line_color=WHITE,
                text_scaling=1.0,
            ),
            # vignette_setting=lambda item: AlphaVignetteEffect(
            #     item,
            #     vignette_radius=0.6,
            #     vignette_softness=0.2,
            #     vignette_intensity=2.0,
            #     aspect_ratio=16 / 9,
            # ),
            # lens_setting=lambda item: LensEffect(
            #     item,
            #     lens_radius=1.2,
            #     lens_strength=0.5,
            #     aspect_ratio=16 / 9,
            # ),
        ).points.scale(0.9).r
        self.play(Create(tape_item))
        self.forward(1)
        self.play(
            tape_item.set_value("D_2"),
        )
        self.play(
            tape_item.set_value("D_3"),
        )
        self.play(
            tape_item.set_value("D_4"),
        )
        self.forward(1)

