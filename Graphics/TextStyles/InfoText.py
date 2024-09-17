from ursina import *
from ursina import curve

import GameConfiguration
from Graphics.GameText import GameText


class InfoText(GameText):
    def __init__(self, text: str):
        super().__init__(
            text,
            origin=(-0.5, 0.5),
            position=(-0.5, 1),
            scale=(3, 3),
            parent=camera.ui
        )

        self.animate_position((-0.5, 0.45), duration=GameConfiguration.fade_time, curve=curve.linear)
        invoke(lambda: self.fade_out(0, duration=GameConfiguration.fade_time), delay=4)
        destroy(self, 5)
