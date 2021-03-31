import math


class Upgrade(object):
    def __init__(self, hp_upgrade=0, melee_attack_upgrade=0, pierce_attack_upgrade=0, melee_armor_upgrade=0,
                 pierce_armor_upgrade=0):
        self.hp_upgrade = hp_upgrade
        self.melee_attack_upgrade = melee_attack_upgrade
        self.pierce_attack_upgrade = pierce_attack_upgrade
        self.melee_armor_upgrade = melee_armor_upgrade
        self.pierce_armor_upgrade = pierce_armor_upgrade

    def __repr__(self):
        return f"{self.hp_upgrade}{self.melee_attack_upgrade}{self.pierce_attack_upgrade}{self.melee_armor_upgrade}{self.pierce_armor_upgrade}"


class Unit(object):
    def __init__(self, hp, melee_attack, pierce_attack, melee_armor, pierce_armor, armor_classes,
                 armor_class_values=None, bonus_attack_classes=None, bonus_attack_values=None, displayed_name=None,
                 atk_upgrades={}, def_upgrades={}):
        self.hp = hp
        self.melee_attack = melee_attack
        self.pierce_attack = pierce_attack
        self.melee_armor = melee_armor
        self.pierce_armor = pierce_armor
        self.armor_classes = zip_class_values(armor_classes, armor_class_values) if armor_classes else {0: 0}
        self.bonus_attack = zip_class_values(bonus_attack_classes, bonus_attack_values) if bonus_attack_values else {
            0: 0}
        self.displayed_name = displayed_name

        self.hp_upgrade = 0
        self.melee_attack_upgrade = 0
        self.pierce_attack_upgrade = 0
        self.melee_armor_upgrade = 0
        self.pierce_armor_upgrade = 0

        self.def_upgrades = {}
        self.atk_upgrades = {}
        self.set_atk_upgrades(atk_upgrades)
        self.set_def_upgrades(def_upgrades)

    def set_def_upgrades(self, def_upgrades):
        if any(x in self.armor_classes.keys() for x in (1, 8, 15, 30,)):
            self.def_upgrades["+1+1"] = Upgrade(0, 0, 0, 1, 1)
            self.def_upgrades["+2+2"] = Upgrade(0, 0, 0, 2, 2)
            self.def_upgrades["+3+4"] = Upgrade(0, 0, 0, 3, 4)

        if 8 in self.armor_classes:
            self.def_upgrades["+Bl.+1+1"] = Upgrade(20, 0, 0, 1, 1)
            self.def_upgrades["+Bl.+2+2"] = Upgrade(20, 0, 0, 2, 2)
            self.def_upgrades["+Bl.+3+4"] = Upgrade(20, 0, 0, 3, 4)

        for key, value in def_upgrades.items():
            self.def_upgrades[key] = value

    def set_atk_upgrades(self, atk_upgrades):
        if any(x in self.armor_classes.keys() for x in (15, 16,)) and not 23 in self.armor_classes.keys():
            self.atk_upgrades["+1"] = Upgrade(0, 0, 1, 0, 0)
            self.atk_upgrades["+2"] = Upgrade(0, 0, 2, 0, 0)
            self.atk_upgrades["+3"] = Upgrade(0, 0, 3, 0, 0)
            self.atk_upgrades["+4"] = Upgrade(0, 0, 4, 0, 0)

        elif any(x in self.armor_classes.keys() for x in (1, 8, 30,)):
            self.atk_upgrades["+1"] = Upgrade(0, 1, 0, 0, 0)
            self.atk_upgrades["+2"] = Upgrade(0, 2, 0, 0, 0)
            self.atk_upgrades["+4"] = Upgrade(0, 4, 0, 0, 0)

        for key, value in atk_upgrades.items():
            self.atk_upgrades[key] = value

    def upgrade(self, upgrade):
        self.hp_upgrade += upgrade.hp_upgrade
        self.melee_attack_upgrade += upgrade.melee_attack_upgrade
        self.pierce_attack_upgrade += upgrade.pierce_attack_upgrade
        self.melee_armor_upgrade += upgrade.melee_armor_upgrade
        self.pierce_armor_upgrade += upgrade.pierce_armor_upgrade
        return self

    def __sub__(self, unit):
        result = int(math.ceil((self.hp + self.hp_upgrade)
                               / max(1, (max(0, unit.melee_attack + unit.melee_attack_upgrade - (
                self.melee_armor + self.melee_armor_upgrade) if unit.melee_attack > 0 else 0)
                                         + max(0, unit.pierce_attack + unit.pierce_attack_upgrade - (
                        self.pierce_armor + self.pierce_armor_upgrade))
                                         + sum(max(0, value - self.armor_classes[key])
                                               if key in self.armor_classes else 0
                                               for key, value in unit.bonus_attack.items())))))

        return result

    def get_name(self):
        return self.displayed_name if self.displayed_name else self.__class__.__name__

    def set_def_upgrades_to_zero(self):
        self.hp_upgrade = 0
        self.melee_armor_upgrade = 0
        self.pierce_armor_upgrade = 0

    def set_atk_upgrades_to_zero(self):
        self.melee_attack_upgrade = 0
        self.pierce_attack_upgrade = 0


def zip_class_values(armor_classes, armor_class_values):
    classes = {}
    for count, value in enumerate(armor_classes):
        classes[value] = armor_class_values[count] if armor_class_values and armor_class_values[count] else 0
    return classes


# feudal

class Militia(Unit):
    def __init__(self):
        super().__init__(40, 4, 0, 0, 1, armor_classes=(1,))


class Archer(Unit):
    def __init__(self):
        super().__init__(30, 0, 4, 0, 0, armor_classes=(15,), bonus_attack_classes=(27,), bonus_attack_values=(3,))


class Skirmisher(Unit):
    def __init__(self):
        super().__init__(30, 0, 2, 0, 3, armor_classes=(15,), bonus_attack_classes=(15, 27), bonus_attack_values=(3, 3))


class Scout(Unit):
    def __init__(self):
        super().__init__(45, 5, 0, 0, 2, armor_classes=(8,), bonus_attack_classes=(25,), bonus_attack_values=(6,))


class ManAtArms(Unit):
    def __init__(self):
        super().__init__(45, 6, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(2,),
                         displayed_name="Man-at-Arms")


class Spearman(Unit):
    def __init__(self):
        super().__init__(45, 3, 0, 0, 0, armor_classes=(1, 27), bonus_attack_classes=(8, 5, 30, 16, 34, 35, 29,),
                         bonus_attack_values=(15, 15, 12, 9, 9, 4, 1,))


class EagleScout(Unit):
    def __init__(self):
        super().__init__(50, 4, 0, 0, 2, armor_classes=(1, 29), bonus_attack_classes=(25, 20, 8, 30, 16,),
                         bonus_attack_values=(8, 3, 2, 1, 1,))


class Villager(Unit):
    def __init__(self):
        super().__init__(25, 3, 0, 0, 0, armor_classes=None, def_upgrades={"+loom": Upgrade(15,0,0,1,2)})


# castle


class Crossbow(Unit):
    def __init__(self):
        super().__init__(35, 0, 5, 0, 0, armor_classes=(15,), bonus_attack_classes=(27,), bonus_attack_values=(3,))


class EliteSkirmisher(Unit):
    def __init__(self):
        super().__init__(35, 0, 3, 0, 4, armor_classes=(15,), bonus_attack_classes=(15, 27, 28,),
                         bonus_attack_values=(4, 3, 2,))


class Slinger(Unit):
    def __init__(self):
        super().__init__(40, 0, 4, 0, 0, armor_classes=(15, 19,), bonus_attack_classes=(1, 32, 17, 27,),
                         bonus_attack_values=(10, 10, 3, 1,))


class CavalryArcher(Unit):
    def __init__(self):
        super().__init__(50, 0, 6, 0, 0, armor_classes=(15, 28, 8,), bonus_attack_classes=(27,),
                         bonus_attack_values=(2,))


class Genitour(Unit):
    def __init__(self):
        super().__init__(50, 0, 3, 0, 4, armor_classes=(15, 28, 8, 19,), bonus_attack_classes=(15, 27, 28,),
                         bonus_attack_values=(4, 2, 2,))


class LongSword(Unit):
    def __init__(self):
        super().__init__(60, 9, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(6,))


class Pikeman(Unit):
    def __init__(self):
        super().__init__(55, 4, 0, 0, 0, armor_classes=(1, 27,), bonus_attack_classes=(8, 5, 30, 16, 34, 35, 29,),
                         bonus_attack_values=(22, 25, 18, 16, 16, 11, 1))


class EagleWarrior(Unit):
    def __init__(self):
        super().__init__(55, 7, 0, 0, 3, armor_classes=(1, 29,), bonus_attack_classes=(25, 20, 8, 30, 16, 34,),
                         bonus_attack_values=(8, 3, 3, 2, 1, 1,))


class LightCavalry(Unit):
    def __init__(self):
        super().__init__(60, 7, 0, 0, 2, armor_classes=(8,), bonus_attack_classes=(25,), bonus_attack_values=(10,))


class Knight(Unit):
    def __init__(self):
        super().__init__(100, 10, 0, 2, 2, armor_classes=(8,))


class CamelRider(Unit):
    def __init__(self):
        super().__init__(100, 6, 0, 0, 0, armor_classes=(30,), bonus_attack_classes=(8, 30, 16, 34,),
                         bonus_attack_values=(9, 5, 5, 5,))


class BattleElephant(Unit):
    def __init__(self):
        super().__init__(250, 12, 0, 1, 2, armor_classes=(8, 5,))


class SteppeLancer(Unit):
    def __init__(self):
        super().__init__(60, 9, 0, 0, 1, armor_classes=(8,))


class BatteringRam(Unit):
    def __init__(self):
        super().__init__(175, 2, 0, -3, 180, armor_classes=(20, 17,), bonus_attack_classes=(20,),
                         bonus_attack_values=(40,))


class Mangonel(Unit):
    def __init__(self):
        super().__init__(50, 40, 0, 0, 6, armor_classes=(20,), bonus_attack_classes=(20,), bonus_attack_values=(12,))


class Scorpion(Unit):
    def __init__(self):
        super().__init__(40, 0, 12, 0, 7, armor_classes=(20,), bonus_attack_classes=(5, 17,),
                         bonus_attack_values=(6, 1,))


class Monk(Unit):
    def __init__(self):
        super().__init__(30, 0, 0, 0, 0, armor_classes=(25,))


# imp


class EliteGenitour(Unit):
    def __init__(self):
        super().__init__(55, 0, 4, 0, 4, armor_classes=(15, 28, 8, 19,), armor_class_values=(0, 1, 0, 0,),
                         bonus_attack_classes=(15, 27, 28,), bonus_attack_values=(5, 2, 2,))
