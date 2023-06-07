from ursina import *

import GameConfiguration
from Graphics.Container import Container
import Game


class DebugOverlay(Container):
    def __init__(self):
        super().__init__(
            model=Quad(0.06),
            position=(0.5, -0.5),
            origin=(0.5, -0.5),
            scale=(0.24, 0.3),
            color=rgb(0, 0, 0, 200),
            parent=camera.ui
        )
        self.content = Text(
            "",
            origin=(0.5, 0.5),
            position=(-0.04, 0.96),
            scale=(2.3, 2.3),
            parent=self
        )
        self.always_on_top = True

    def update(self):
        self.content.text = f"version: {Game.version}\n" \
                            f"{Game.state}\n" \
                            f"{Game.state_affected}\n" \
                            f"notifications: {len(Game.notification_manager.notifications)}\n" \
                            f"volume: {round(GameConfiguration.volume, 2)}\n" \
                            f"fullscreen: {GameConfiguration.fullscreen}\n" \
                            f"extra ui: {GameConfiguration.extra_ui_info}\n" \
                            f"pitch range: {GameConfiguration.random_pitch_range}"
