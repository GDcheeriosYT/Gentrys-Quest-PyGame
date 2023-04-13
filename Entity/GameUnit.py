from .GameEntityBase import GameEntityBase
from .Stats import Stats
from .TextureMapping import TextureMapping
from .AudioMapping import AudioMapping
from utils.Event import Event
from .EntityOverHead import EntityOverhead
from ursina import *


class GameUnit(GameEntityBase):
    def __init__(self):
        super().__init__()
        self._stats = Stats()
        self._overhead = EntityOverhead(self)
        self._difficulty = 1

        # event initialization
        self.on_heal = Event("OnHeal", 0)
        self.on_damage = Event("OnDamage", 0)
        self.on_attack = Event("OnAttack", 0)
        self.on_death = Event("OnDeath", 0)
        self.on_move = Event("OnMove", 0)
        self.on_spawn = Event("OnSpawn", 0)

        self.on_level_up += self.print_data
        self.on_level_up += self.update_stats
        self.on_spawn += self.update_stats

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @property
    def overhead(self) -> EntityOverhead:
        return self._overhead

    @property
    def stats(self) -> Stats:
        """
        The stats of the Entity
        """
        return self._stats

    @property
    def texture_mapping(self) -> TextureMapping:
        return TextureMapping()

    @property
    def audio_mapping(self) -> AudioMapping:
        return AudioMapping()

    def set_idle_texture(self):
        self.texture = self.texture_mapping.get_idle_texture()

    def set_damage_texture(self):
        self.texture = self.texture_mapping.get_damage_texture()

    def damage(self, amount):
        self.stats.health.current_value -= amount
        self.on_damage()
        if self.stats.health.current_value <= 0:
            self.die()

    def heal(self, amount):
        self.stats.health.current_value += amount
        self.on_heal()

    def die(self):
        self.on_death()

    def move_left(self):
        self.x -= self.stats.speed.current_value * time.dt
        self.on_move()

    def move_right(self):
        self.x += self.stats.speed.current_value * time.dt
        self.on_move()

    def move_up(self):
        self.y += self.stats.speed.current_value * time.dt
        self.on_move()

    def move_down(self):
        self.y -= self.stats.speed.current_value * time.dt
        self.on_move()

    def spawn(self) -> None:
        self.enable()
        self.on_spawn()
        self.spawn_sequence()

    def spawn_sequence(self) -> None:
        Audio(self.audio_mapping.get_spawn_sound())

    def print_data(self, *_) -> None:
        print(self.name, self._difficulty)
        print(self._experience)
        print(self._stats)
