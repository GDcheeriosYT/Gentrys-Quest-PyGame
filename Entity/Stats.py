from .Stat import Stat


class Stats:
    def __init__(self):
        self._health = Stat("Health", 100)
        self._attack = Stat("Attack", 16)
        self._defense = Stat("Defense", 12)
        self._crit_rate = Stat("CritRate", 5)
        self._crit_damage = Stat("CritDamage", 50)
        self._speed = Stat("Speed")

    @property
    def health(self) -> Stat:
        return self._health

    @property
    def attack(self) -> Stat:
        return self._attack

    @property
    def defense(self) -> Stat:
        return self._defense

    @property
    def crit_rate(self) -> Stat:
        return self._crit_rate

    @property
    def crit_damage(self) -> Stat:
        return self._crit_damage

    @property
    def speed(self) -> Stat:
        return self._speed

    def __repr__(self):
        print(self.health)
        print(self.attack)
        print(self.defense)
        print(self.crit_rate)
        print(self.crit_damage)
        print(self.speed)
        return ""
