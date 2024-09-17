from Entity.Weapon.SwingWeapon import SwingWeapon
from Entity.Buff import Buff


class KingsGolfClub(SwingWeapon):
    def __init__(self):
        super().__init__(
            Buff('AttackSpeed', False)
        )
        self.scale_override = 1.5, 1.5

    @property
    def name(self) -> str:
        return "King's Golf Club"

    @property
    def star_rating(self) -> int:
        return 3

    @property
    def base_speed(self) -> float:
        return 1.5

    @property
    def base_attack(self) -> int:
        return 37

    @property
    def range(self) -> float:
        return 2.3

    @property
    def weapon_type(self) -> str:
        return "Golf Club"

    @property
    def texture(self) -> str:
        return "Textures/golfy.png"
