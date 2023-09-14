from ursina import *

import Game

from Graphics.Container import Container
from Graphics.Containers.ScrollableContainer import ScrollableContainer
from Gacha.GachaTypes import GachaTypes
from Overlays.Notification import Notification

from .GachaBanner import GachaBanner


class GachaMenu(Entity):
    def __init__(self, parent):
        super().__init__(
            model="quad",
            color=color.clear,
            parent=parent
        )

        self.gachas = Game.content_manager.gachas

        self.selected_gacha = self.gachas[0]

        self.amount = 1
        self.amount_container = Container(
            position=(-0.25, 0.35),
            scale=(0.1, 0.25),
            parent=self
        )
        self.amount_down = Button(
            "-",
            scale=(0.25, 0.25),
            position=(-0.5, 0),
            parent=self.amount_container
        )
        self.amount_down.on_click = lambda: self.increase_amount(False)
        self.amount_text = Text(
            str(self.amount),
            scale=(7, 7),
            position=(0, 0),
            origin=(0, 0),
            color=color.black,
            parent=self.amount_container
        )
        self.amount_text_text = Text(
            "Amount",
            position=(0, 0.25),
            scale=(5, 5),
            origin=(0, 0),
            color=color.black,
            parent=self.amount_container
        )
        self.amount_up = Button(
            "+",
            scale=(0.25, 0.25),
            position=(0.5, 0),
            parent=self.amount_container
        )
        self.amount_up.on_click = lambda: self.increase_amount(True)

        self.banners = ScrollableContainer(
            is_down=False,
            position=(0.25, 0),
            scale=(0.5, 0.85),
            parent=self
        )
        for gacha in self.gachas:
            banner = GachaBanner(gacha())
            banner.on_click = lambda: self.select_banner(banner)
            self.banners.add_to_container(banner)

        self.select_banner(self.banners.container_children[0])

        self.pull_character_button = Button(
            "Pull character",
            position=(-0.25, 0),
            scale=(0.25, 0.1),
            parent=self
        )

        self.pull_character_button.on_click = lambda: self.pull(True)

        self.pull_weapon_button = Button(
            "Pull weapon",
            position=(-0.25, -0.25),
            scale=(0.25, 0.1),
            parent=self
        )

        self.pull_weapon_button.on_click = lambda: self.pull(False)

    def increase_amount(self, increase: bool):
        self.amount += 1 if increase else -1
        if self.amount < 1:
            self.amount = 1

        self.amount_text.text = str(self.amount)

    def select_banner(self, banner):
        for banner in self.banners.container_children:
            banner.deselect()

        banner.select()
        self.selected_gacha = self.gachas[self.banners.container_children.index(banner)]()

    def pull(self, is_character: bool):
        if Game.user.get_money() > self.selected_gacha.cost * self.amount:
            Game.user.remove_money(self.selected_gacha.cost * self.amount)
            if is_character:
                characters = self.selected_gacha.pull(self.amount, GachaTypes.Character)
                for character in characters:
                    found = False
                    for user_character in Game.user.get_characters():
                        if user_character.name == character.name:
                            found = True
                            user_character.add_xp(user_character.star_rating * 100)

                    if not found:
                        Game.user.add_character(character)

            else:
                [Game.user.add_weapon(weapon) for weapon in self.selected_gacha.pull(self.amount, GachaTypes.Weapon)]
        else:
            Game.notification_manager.add_notification(Notification("Can't afford...", color.red))
