from ursina import *
import Game
import GameConfiguration
from Graphics.Containers.TextContainer import TextContainer
from utils.Event import Event


class Register(Entity):
    def __init__(self, gas_station):
        super().__init__(
            model='quad',
            color=color.white,
            collider='box',
            position=(-0.3, -0.2, -1),
            scale=(0.06, 0.5),
            parent=gas_station
        )

        self.bought = False
        self.text_container = TextContainer()
        self.buy_event = Event("BuyEvent", 0)

    def buy_sequence(self, entity):
        if entity == Game.user.get_equipped_character():
            if "Ramen" in Game.user.user_data.items:
                Game.user.user_data.items.remove("Ramen")
                self.text_container.set_text("Thanks for coming by have a good night!", 3)
                Game.audio_system.play_sound(Audio("Audio/buy.mp3"))
                self.buy_finish()

            else:
                self.text_container.set_text("Do you need something sir?", 3)

    def buy_finish(self):
        self.buy_event()
        self.bought = True

    def update(self):
        if self.intersects().hit and not self.bought:
            entity = self.intersects().entity
            self.buy_sequence(entity)
