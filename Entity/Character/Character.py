from ursina import *
from ursina.camera import Camera

import Game
from GameStates import GameStates
from ..GameUnit import GameUnit
from typing import Union, List
from ..EntityOverHead import EntityOverhead
from Overlays.Notification import Notification
from Entity.TextureMapping import TextureMapping
from Entity.AudioMapping import AudioMapping
from Entity.Loot import Loot
from Entity.Artifact.Artifact import Artifact
from Entity.Buff import Buff
from Entity.Affiliation import Affiliation
from Graphics.TextStyles.TitleText import TitleText
from Graphics.FadeScreen import FadeScreen
from Content.Effects.Burn.Burn import Burn


class Character(GameUnit):
    def __init__(self, texture_mapping: TextureMapping = TextureMapping(), audio_mapping: AudioMapping = AudioMapping(), *args, **kwargs):
        super().__init__(
            texture_mapping=texture_mapping,
            audio_mapping=audio_mapping,
            *args,
            **kwargs
        )

        self.affiliation = Affiliation.Player

        self.texture = self.texture_mapping.get_idle_texture()

        self._is_equipped = False
        self.artifacts = [
            None,
            None,
            None,
            None,
            None
        ]

        self.secondary = None
        self.utility = None
        self.ultimate = None

        self.on_level_up += self._on_level_up
        self.on_level_up += self.recover_health
        self.on_death += self.death_transition

    @property
    def star_rating(self) -> int:
        raise NotImplementedError

    @property
    def description(self) -> str:
        return ""

    @property
    def is_equipped(self) -> bool:
        return self._is_equipped

    def equip(self):
        self._is_equipped = True
        self.is_current_player = True

    def unequip(self):
        self._is_equipped = False
        self.is_current_player = False

    def _on_level_up(self):
        notification = Notification(f"{self.name} is now level {self.experience.level}", color.blue)
        Game.notification_manager.add_notification(notification)

    def set_artifact(self, artifact: Artifact, index: int):
        artifact.equipped_entity = self
        self.artifacts[index] = artifact
        self.update_stats()

    def remove_weapon(self):
        self._weapon.on_level_up -= self.update_stats
        self._weapon.de_equip()
        self._weapon = None
        self.update_stats()

    def remove_artifact(self, index: int):
        self.artifacts[index].equipped_entity = None
        self.artifacts[index] = None
        self.update_stats()

    def update_stats(self):
        def calculate(variable, multiplier: Union[int, float] = 1):
            return variable * multiplier

        # experience stats
        self._difficulty = int(1 + (self.experience.level / 20))

        # health stats
        self._stats.health.set_default_value(int((calculate(self._experience.level, 57) + calculate(self._experience.level, calculate(self.star_rating, 2)) + calculate(self._experience.level, calculate(self.check_minimum(self._stats.health.points, 4)))) + calculate(self._difficulty, 1000) + calculate(self._stats.health.points, 10) + calculate(self.star_rating, 5)))

        # attack stats
        self._stats.attack.set_default_value(int((calculate(self._experience.level, 1.25) + calculate(self.star_rating, 1.50) + calculate(self.star_rating, calculate(self.check_minimum(self._stats.attack.points))) + calculate(self.difficulty - 1, 20)) + 45 + calculate(self.check_minimum(self._stats.attack.points, 3)) + calculate(self.star_rating, 3)))

        # defense stats
        self._stats.defense.set_default_value(self.experience.level * 5)

        # crit rate stats
        self._stats.crit_rate.set_default_value(calculate(self.stats.crit_rate.points, 2))

        # crit damage stats
        self._stats.crit_damage.set_default_value(calculate(self.stats.crit_damage.points, 10))

        # speed stats
        self._stats.speed.set_default_value(1 + ((self.difficulty - 1) * 0.2) + calculate(self.stats.speed.points, 0.5) + (self.star_rating * 0.1))

        # attack speed stats
        self._stats.attack_speed.set_default_value(self.stats.speed.points * 0.5)

        # artifacts
        self.stats.reset_additional_stats()

        def manage_attribute(attribute: Buff):
            value = attribute.value
            if attribute.is_percent:
                self.stats.get_stat_by_string(attribute.stat).boost_stat(value)
            else:
                self.stats.get_stat_by_string(attribute.stat).add_value(value)

        families = {}
        star_rating_count = 0
        avg_star_rating = 0
        count = 0

        for artifact in self.artifacts:
            if artifact:
                star_rating_count += artifact.star_rating
                count += 1
                family = artifact.family
                # append family
                if family not in families.keys():
                    families[family] = 1
                else:
                    families[family] += 1

                # main attribute
                manage_attribute(artifact.main_attribute)

                # attributes
                for attribute in artifact.attributes:
                    manage_attribute(attribute)

        try:
            avg_star_rating = star_rating_count / count
        except ZeroDivisionError:
            pass

        print(families)

        for family in families.keys():
            family_reference = Game.content_manager.get_family(family)
            if families[family] >= 2:
                family_reference.two_piece_buff.apply_buff(self)
            if families[family] >= 4:
                family_reference.four_piece_buff.apply_buff(self)
            if families[family] == 5:
                self._stats.boost_all_stats(avg_star_rating)

        # weapon buff
        if self.weapon:
            manage_attribute(self.weapon.buff)

        # event
        self.on_update_stats()

    def update(self):
        self.direction = Vec3(
            self.up * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        if not self.is_effected_by("Stun") and not self.hits(self.direction):
            self.position += self.direction * self._stats.speed.get_value() * time.dt
            self.on_move()

        if held_keys["left mouse"] and self._weapon and not self.is_effected_by("Stun"):
            if self._weapon.is_ready():
                self.attack()

        if held_keys["right mouse"] and self.secondary.is_ready and not self.is_effected_by("Stun"):
            self.secondary.activate()

        if held_keys["shift"] and self.utility.is_ready and not self.is_effected_by("Stun"):
            self.utility.activate()

        if held_keys["r"] and self.ultimate.is_ready and not self.is_effected_by("Stun"):
            self.ultimate.activate()

        try:
            self.secondary.update_time()
        except:
            pass
        try:
            self.utility.update_time()
        except:
            pass
        try:
            self.ultimate.update_time()
        except:
            pass

        self.handle_buffs()

    def swap_artifact(self, artifact, index: int):
        if 1 <= index <= 5:
            if self.artifacts[index - 1]:
                swapped_artifact = self.artifacts[index - 1]
                self.artifacts[index - 1] = artifact
                self.update_stats()
                return swapped_artifact
            else:
                self.artifacts[index - 1] = artifact

        self.update_stats()

    def manage_loot(self, loot: Loot):
        self.add_xp(loot.xp)
        Game.user.add_money(loot.money)

    def create_texture_copy(self, delay: Union[int, float]):
        copy = Entity(
            model="quad",
            texture=self.texture,
            position=self.position
        )
        destroy(copy, delay)

    def death_transition(self):
        if Game.state != GameStates.testing and Game.state != GameStates.tutorial:
            self.create_texture_copy(4)
            fade_screen = FadeScreen()
            invoke(lambda: camera.animate_position((camera.x, camera.y + 10), 3, curve=curve.linear), delay=0.2)
            fade_screen.fade_in(1, 4, curve=curve.linear)
            death_text = TitleText("You Died...", color=rgb(255, 0, 0, 0))
            death_text.fade_in(1, 2)
            invoke(lambda: fade_screen.fade_out(0, 2), delay=4)
            invoke(lambda: death_text.fade_out(0, 2), delay=4)
            destroy(fade_screen, 20)
            destroy(death_text, 20)
            invoke(lambda: Game.change_state(GameStates.selection), delay=5)

    def jsonify(self):
        artifacts = []
        for artifact in self.artifacts:
            if artifact is not None:
                artifacts.append(artifact.jsonify())
            else:
                artifacts.append(None)

        return {
            "stats": {
                "defense": self._stats.defense.points,
                "attack": self._stats.attack.points,
                "critDamage": self._stats.crit_damage.points,
                "health": self._stats.health.points,
                "critRate": self._stats.crit_rate.points
            },
            "name": self.name,
            "equips": {
                "weapon": self.weapon.jsonify() if self.weapon is not None else None,
                "artifacts": artifacts
            },
            "experience": {
                "level": self.experience.level,
                "xp": self.experience.xp
            },
            'star rating': self.star_rating
        }
