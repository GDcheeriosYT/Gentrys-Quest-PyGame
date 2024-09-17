from ursina import *

import Game
from GameStates import GameStates
from User.User import User
from Content.Characters.StarterCharacter.StarterCharacter import StarterCharacter
from Graphics.GameButton import GameButton
from Graphics.GameText import GameText


class GuestConfirmBox(Entity):
    def __init__(self, user: User, menu, *args, **kwargs):
        super().__init__(
            model=Quad(0.15),
            origin=(0, 0),
            scale=(0.6, 0.6),
            position=(0, -0.1),
            color=color.clear,
            parent=camera.ui,
            *args,
            **kwargs
        )

        self._user = user
        self._menu = menu
        menu.disable()

        self._confirm_text = GameText(Game.language.get_localized_text(Game.language.confirm_guest, self._user.username), position=(0, 0.3), origin=(0, 0),
                                  scale=(2.5, 2.5), parent=self)
        self._confirm_box = GameButton(Game.language.confirm, position=(0, -0.2), scale=(0.2, 0.1), parent=self)
        self._confirm_box.on_click = self.confirm_on_click
        self._back_box = GameButton("X", position=(0.5, 0.5), scale=(0.05, 0.05), origin=(0.5, 0.5), parent=self)
        self._back_box.on_click = self.back_on_click

    def confirm_on_click(self):
        Game.user = self._user
        Game.user.load()
        if Game.user.user_data.startup_amount == 0:
            starter_character = StarterCharacter(Game.user.username)
            starter_character.swap_weapon(Game.content_manager.get_weapon("No Weapon"))
            Game.user.user_data.increment_startup_amount()
            Game.user.equip_character(starter_character)
            Game.user.add_character(starter_character)
            Game.change_state(GameStates.tutorial)
        else:
            Game.user.user_data.increment_startup_amount()
            Game.change_state(GameStates.selection)

        self._menu.enable()
        destroy(self)

    def back_on_click(self):
        self._menu.enable()
        destroy(self)
