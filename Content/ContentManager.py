# Artifact Families
from Content.ArtifactFamilies.BraydenMesserschmidt.BraydenMesserschmidtFamily import BraydenMesserschmidtFamily
from Content.ArtifactFamilies.TestFamily.TestFamily import TestFamily
from Content.ArtifactFamilies.HyVee.HyVee import HyVee

# Characters
from Content.Characters.StarterCharacter.StarterCharacter import StarterCharacter
from Content.Characters.BraydenMesserschmidt.BraydenMesserschmidt import BraydenMesserschmidt
from Content.Characters.PeteMarks.PeteMarks import PeteMarks
from Content.Characters.PhilipMcClure.PhilipMcClure import PhilipMcClure
from Content.Characters.MasonJames.MasonJames import MasonJames

# Effects
from Content.Effects.Burn.Burn import Burn
from Content.Effects.Stun.Stun import Stun

# Enemies
from Content.Enemies.TestEnemy import TestEnemy
from Content.Enemies.AngryPedestrian.AngryPedestrian import AngryPedestrian
from Content.Enemies.AngryChineseMan.AngryChineseMan import AngryChineseMan

# Locations
from Content.Locations.TestLocation.TestLocation import TestLocation

# Weapons
from Content.Weapons.Knife.Knife import Knife
from Content.Weapons.BraydensOsuPen.BraydensOsuPen import BraydensOsuPen
from Content.Weapons.KingsGolfClub.KingsGolfClub import KingsGolfClub
from Content.Weapons.NoWeapon.NoWeapon import NoWeapon

# Gachas
from Content.Gachas.TestGacha import TestGacha
from Content.Gachas.ValleyHighSchool import ValleyHighSchool

# Languages
from Content.Languages.English import English
from Content.Languages.Japanese import Japanese


class ContentManager:
    def __init__(self):
        self.artifact_families = [
            BraydenMesserschmidtFamily,
            TestFamily,
            HyVee
        ]

        self.characters = [
            StarterCharacter,
            BraydenMesserschmidt,
            PeteMarks,
            PhilipMcClure,
            MasonJames
        ]
        
        self.effects = [
            Burn,
            Stun
        ]
        
        self.enemies = [
            TestEnemy,
            AngryPedestrian,
            AngryChineseMan
        ]

        self.locations = [
            TestLocation
        ]

        self.weapons = [
            Knife,
            BraydensOsuPen,
            KingsGolfClub,
            NoWeapon
        ]

        self.gachas = [
            TestGacha,
            ValleyHighSchool
        ]

        self.languages = [
            English,
            Japanese
        ]

    def get_family(self, name: str):
        for family in self.artifact_families:
            if name == family().name:
                return family()

    def get_artifact(self, name: str, star_rating: int):
        for family in self.artifact_families:
            for artifact in family().artifacts:
                try:
                    if artifact(star_rating).name == name:
                        return artifact(star_rating)
                except TypeError:
                    if artifact().name == name:
                        return artifact()

    def get_character(self, name):
        for character in self.characters:
            try:
                if name == character().name:
                    return character()
            except TypeError:
                pass

        return StarterCharacter(name)

    def get_enemy(self, name):
        for enemy in self.enemies:
            if name == enemy().name:
                return enemy()

    def get_location(self, name):
        for location in self.locations:
            if name == location().name:
                return location()

    def get_effect(self, name):
        for effect in self.effects:
            effect = effect()
            if effect.name == name:
                return effect

    def get_weapon(self, name):
        for weapon in self.weapons:
            if name == weapon().name:
                return weapon()

    def get_language(self, name: str):
        for language in self.languages:
            language = language()
            print(name, language.name)
            if language.name == name:
                return language

        return English()
