from Entity.Buff import Buff
from Entity.Weapon.Weapon import Weapon


class NoWeapon(Weapon):
    def __init__(self):
        super().__init__(
            buff=Buff()  # set the weapon buff
        )

    @property
    def name(self) -> str:
        return "No Weapon"

    @property
    def base_attack(self) -> int:
        return 0

    @property
    def base_speed(self):
        return 0

    @property
    def range(self):
        return 0

    @property
    def weapon_type(self) -> str:
        return "Nothing"

    @property
    def texture(self) -> str:
        return "Textures/Red_X.png"

    @property
    def star_rating(self) -> int:
        return 1

    def attack_process(self, direction):
        pass
