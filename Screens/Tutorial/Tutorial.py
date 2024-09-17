from ursina import *
from ursina.curve import *

import Game

from Graphics.Containers.TextContainer import TextContainer

from ..Screen import Screen
from .Map.TutorialMap import TutorialMap
from .Map.Ramen import Ramen


class Tutorial(Screen):
    def __init__(self):
        super().__init__()
        self.on_show += self._show
        self.phase = 0

    def _show(self):
        self.player = Game.user.get_equipped_character()
        self.player.apply_effect(Game.content_manager.get_effect("Stun"))
        self.map = TutorialMap()
        text_container = TextContainer()
        text_container.set_text("It's 10pm...", 5)
        camera.position = (0, -10, -20)
        camera.animate_position((0, 0, -20), 4, curve=linear)
        invoke(self.player.spawn, delay=5)
        invoke(lambda: self.player.remove_effect("Stun"), delay=10)
        text_container.schedule_text(f"{self.player.name} is at a\nconvenience store buying ramen noodles.", 6, 4)
        text_container.schedule_text(f"He picks up some ramen.", 11, 5)
        invoke(lambda: Ramen(position=(6, 0)), delay=10)
        invoke(self.show_controls, delay=9)

    def show_controls(self):
        movement = Text(
            "Movement\nW A S D",
            position=(-0.8, 1),
            scale=(4, 4),
            parent=camera.ui,
        )
        movement.animate_position((-0.8, 0.5), duration=2, curve=linear)
        invoke(lambda: movement.fade_out(duration=2), delay=4)
        destroy(movement, 8)

    @property
    def name(self) -> str:
        return "Tutorial"

    @property
    def fades(self) -> bool:
        return True

    @property
    def color(self) -> color:
        return rgb(17, 80, 17)
