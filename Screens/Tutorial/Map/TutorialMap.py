from ursina import *

import Game

from .GasStation import GasStation
from .ParkingLot import ParkingLot
from .GentrysHouse import GentrysHouse

from Content.Enemies.AngryPedestrian.AngryPedestrian import AngryPedestrian
from Graphics.TextStyles.InfoText import InfoText
from Graphics.UIs.HUD.SkillsContainer import SkillsContainer
from Graphics.FadeScreen import FadeScreen
from Graphics.TextStyles.TitleText import TitleText
from Graphics.GameText import GameText


class TutorialMap(Entity):
    def __init__(self):
        super().__init__(
            # model='quad',
            # color=color.clear,
            # collider='box',
            # scale=(20, 60),
            # parent=self
        )
        self.angry_pedestrian = AngryPedestrian()
        self.angry_pedestrian.disable()
        self.angry_pedestrian.position = (0, 0, -1)
        self.gentrys_house = GentrysHouse()
        self.gentrys_house.disable()
        self.angry_pedestrian.apply_effect(Game.content_manager.get_effect("Stun"))
        self.angry_pedestrian.follow_entity(Game.user.get_equipped_character())
        self.gas_station = GasStation()
        self.parking_lot = ParkingLot()
        self.enemy_cutscene_intro = False
        self.character_copy = Entity(
            model="quad",
            texture=Game.user.get_equipped_character().texture,
        )
        self.character_copy.disable()
        self.skills_container = SkillsContainer(Game.user.get_equipped_character(), parent=camera.ui)
        self.skills_container.scale = (0.5, 0.5)
        self.skills_container.position = 0.05, -0.35
        self.skills_container.disable()
        self.death_transition = False

    def update(self):
        if not self.enemy_cutscene_intro:
            if self.parking_lot.cutscene_toggler.intersects().entity == Game.user.get_equipped_character():
                self.gas_station.disable()
                self.enemy_cutscene_intro = True
                Game.user.get_equipped_character().apply_effect(Game.content_manager.get_effect("Stun"))
                Game.user.get_equipped_character().disable()
                self.character_copy.position = Game.user.get_equipped_character().position
                self.character_copy.animate_position(self.character_copy.position + (0, -1, 0), 0.2, curve=curve.linear)
                Game.user.get_equipped_character().animate_position(self.character_copy.position + (0, -1, 0), 0.2,
                                                                    curve=curve.linear)
                self.character_copy.enable()
                self.angry_pedestrian.experience.level = 10
                self.angry_pedestrian.update_stats()
                self.angry_pedestrian.stats.boost_all_stats(180)
                self.angry_pedestrian.position = (
                self.character_copy.x + 10, self.character_copy.y - 1, self.character_copy.z)
                invoke(lambda: camera.animate_position((10, camera.position[1] - 5, -20), 2.5, curve=curve.linear),
                       delay=1)
                invoke(self.angry_pedestrian.spawn, delay=4)
                invoke(lambda: self.angry_pedestrian.remove_effect("Stun"), delay=7)
                invoke(self.character_copy.disable, delay=5)
                invoke(Game.user.get_equipped_character().enable, delay=5)
                invoke(lambda: camera.animate_position((0, camera.position[1], -20), 2.5, curve=curve.linear), delay=7)
                invoke(lambda: self.angry_pedestrian.apply_effect(Game.content_manager.get_effect("Stun")), delay=10)
                invoke(lambda: InfoText("Use Skills:\nleft and right mouse buttons\nshift and R keys"), delay=10)
                invoke(self.skills_container.enable, delay=10)
                invoke(lambda: Game.user.get_equipped_character().remove_effect("Stun"), delay=12)
                invoke(lambda: self.angry_pedestrian.remove_effect("Stun"), delay=12)

        if Game.user.get_equipped_character().dead and not self.death_transition:
            fade_screen = FadeScreen()
            death_text = TitleText("You Died", color=color.red)
            or_so_you_thought_text = GameText("or so you thought...", color=color.red)
            or_so_you_thought_text.alpha = 0
            or_so_you_thought_text.always_on_top = True
            death_text.alpha = 0
            death_text.always_on_top = True
            self.skills_container.disable()
            Game.user.get_equipped_character().stats.restore_stats()
            fade_screen.fade_in(1, 2, curve=curve.linear)
            death_text.fade_in(1, 1, curve=curve.linear)
            invoke(lambda: or_so_you_thought_text.fade_in(1, 1, curve=curve.linear), delay=3)
            invoke(lambda: fade_screen.fade_out(0, 2), delay=4)
            invoke(lambda: death_text.fade_out(0, 2), delay=4)
            invoke(lambda: or_so_you_thought_text.fade_out(0, 2, curve=curve.linear), delay=6)
            invoke(lambda: Game.app.setBackgroundColor(color.black), delay=4)
            invoke(self.parking_lot.disable, delay=4)
            invoke(self.angry_pedestrian.disable, delay=4)
            invoke(self.gentrys_house.enable, delay=4)
            camera.animate_position((0, 0), duration=4, curve=curve.linear)
            destroy(fade_screen, 7)
            destroy(death_text, 7)
            destroy(or_so_you_thought_text, 10)
            self.death_transition = True
