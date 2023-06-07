from ursina import *
from ursina.camera import Camera

import Game
from ..GameUnit import GameUnit
from typing import Union
from ..EntityOverHead import EntityOverhead
from Overlays.Notification import Notification
from Overlays.NotificationsManager import NotificationManager
from Content.Enemies.TestEnemy import TestEnemy
from Entity.TextureMapping import TextureMapping
from Entity.AudioMapping import AudioMapping
from Entity.Enemy.Enemy import Enemy
from Entity.Loot import Loot
from Entity.Artifact.Artifact import Artifact


class Character(GameUnit):
    def __init__(self, texture_mapping: TextureMapping = TextureMapping(), audio_mapping: AudioMapping = AudioMapping()):
        super().__init__(
            texture_mapping=texture_mapping,
            audio_mapping=audio_mapping
        )

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

    @property
    def star_rating(self) -> int:
        raise NotImplementedError

    @property
    def description(self) -> str:
        return ""

    @property
    def is_equipped(self) -> bool:
        return self._is_equipped

    def _on_level_up(self):
        notification = Notification(f"{self.name} is now level {self.experience.level}", color.blue)
        NotificationManager.add_nofication(notification)

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
        for artifact in self.artifacts:
            if artifact:
                # main attribute
                value = artifact.main_attribute.value
                if artifact.main_attribute.is_percent:
                    self.stats.get_stat_by_string(artifact.main_attribute.stat).boost_stat(value)
                else:
                    self.stats.get_stat_by_string(artifact.main_attribute.stat).add_value(value)

        # event
        self.on_update_stats()

    def update(self):
        if self.spawned:
            camera.position = (self.x, self.y, -20)
        if held_keys["-"]:
            if self.experience.level > 1:
                self.experience.level -= 1
                self.experience.xp = 0
                self.on_level_up()
                self.update_stats()
        if held_keys["="]:
            self.level_up()
            self.experience.xp = 0
        if held_keys["/"]:
            self.damage(50)

        self.direction = Vec3(
            self.up * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()  # get the direction we're trying to walk in.
        if self.direction == 0:
            self.set_idle_texture()
        origin = self.world_position
        hit_info = raycast(origin, self.direction, ignore=[self, Enemy], distance=.1)
        if not hit_info.hit:
            if self.can_move:
                self.position += self.direction * self._stats.speed.get_value() * time.dt
                self.on_move()

        if held_keys["left mouse"] and self._weapon:
            if self._weapon.is_ready():
                self.attack()

        if held_keys["right mouse"] and self.secondary.is_ready and not self.secondary.disabled:
            self.secondary.activate()

        if held_keys["shift"] and self.utility.is_ready and not self.ultimate.disabled:
            self.utility.activate()

        if held_keys["r"] and self.ultimate.is_ready and not self.ultimate.disabled:
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

    def disable_skills(self):
        self.secondary.disable()
        self.utility.disable()
        self.ultimate.disable()

    def input(self, key):
        if key == "p":
            test_enemy = TestEnemy()
            test_enemy.on_death += lambda: self.manage_loot(test_enemy.get_loot())
            test_enemy.position = self.position
            test_enemy.y += random.randint(-7, 7)
            test_enemy.x += random.randint(-7, 7)
            test_enemy.follow_entity(self)
            test_enemy.spawn()
