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
        if 19 not in self.armor_classes.keys() and any(x in self.armor_classes.keys() for x in (1, 8, 15, 30,)):
            self.def_upgrades["+1+1"] = Upgrade(0, 0, 0, 1, 1)
            self.def_upgrades["+2+2"] = Upgrade(0, 0, 0, 2, 2)
            self.def_upgrades["+3+4"] = Upgrade(0, 0, 0, 3, 4)

        if 19 not in self.armor_classes.keys() and any(x in self.armor_classes.keys() for x in (8, 30,)):
            self.def_upgrades["+Bl."] = Upgrade(20, 0, 0, 0, 0)
            self.def_upgrades["+Bl.+1+1"] = Upgrade(20, 0, 0, 1, 1)
            self.def_upgrades["+Bl.+2+2"] = Upgrade(20, 0, 0, 2, 2)
            self.def_upgrades["+Bl.+3+4"] = Upgrade(20, 0, 0, 3, 4)

        for key, value in def_upgrades.items():
            self.def_upgrades[key] = value

    def set_atk_upgrades(self, atk_upgrades):
        if 19 not in self.armor_classes.keys() and any(
                x in self.armor_classes.keys() for x in (15,)) and not 23 in self.armor_classes.keys():
            self.atk_upgrades["+1"] = Upgrade(0, 0, 1, 0, 0)
            self.atk_upgrades["+2"] = Upgrade(0, 0, 2, 0, 0)
            self.atk_upgrades["+3"] = Upgrade(0, 0, 3, 0, 0)
            self.atk_upgrades["+4"] = Upgrade(0, 0, 4, 0, 0)

        elif 19 not in self.armor_classes.keys() and any(x in self.armor_classes.keys() for x in (1, 8, 30,)):
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
                               / max(1, ((max(0, unit.melee_attack + unit.melee_attack_upgrade - (
                self.melee_armor + self.melee_armor_upgrade)) if unit.melee_attack > 0 else 0) + max(
            0, unit.pierce_attack + unit.pierce_attack_upgrade - (self.pierce_armor + self.pierce_armor_upgrade)) + sum(
            max(0, value - self.armor_classes[key]) if key in self.armor_classes else 0 for key, value in
            unit.bonus_attack.items())))))
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
        super().__init__(40, 4, 0, 0, 1, armor_classes=(1,),
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+10%HP (Vikings)": Upgrade(hp_upgrade=4),
                                       "+10%HP+1+1 (Vikings)": Upgrade(hp_upgrade=4, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+2+2 (Vikings)": Upgrade(hp_upgrade=4, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+10%HP+3+4 (Vikings)": Upgrade(hp_upgrade=4, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+15%HP (Vikings)": Upgrade(hp_upgrade=6),
                                       "+15%HP+1+1 (Vikings)": Upgrade(hp_upgrade=6, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+15%HP+2+2 (Vikings)": Upgrade(hp_upgrade=6, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+15%HP+3+4 (Vikings)": Upgrade(hp_upgrade=6, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+20%HP (Vikings)": Upgrade(hp_upgrade=8),
                                       "+20%HP+1+1 (Vikings)": Upgrade(hp_upgrade=8, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+20%HP+2+2 (Vikings)": Upgrade(hp_upgrade=8, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+20%HP+3+4 (Vikings)": Upgrade(hp_upgrade=8, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4), })


class Archer(Unit):
    def __init__(self):
        super().__init__(30, 0, 4, 0, 0, armor_classes=(15,), bonus_attack_classes=(27,), bonus_attack_values=(3,))


class Skirmisher(Unit):
    def __init__(self):
        super().__init__(30, 0, 2, 0, 3, armor_classes=(15,), bonus_attack_classes=(15, 27), bonus_attack_values=(3, 3))


class Scout(Unit):
    def __init__(self):
        super().__init__(45, 5, 0, 0, 2, armor_classes=(8,), bonus_attack_classes=(25,), bonus_attack_values=(6,),
                         displayed_name="Scout Cavalry",
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={"+4+5 (SilkArmor)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=5)})


class ManAtArms(Unit):
    def __init__(self):
        super().__init__(45, 6, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(2,),
                         displayed_name="Man-at-Arms",
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+10%HP (Vikings)": Upgrade(hp_upgrade=4.5),
                                       "+10%HP+1+1 (Vikings)": Upgrade(hp_upgrade=4.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+2+2 (Vikings)": Upgrade(hp_upgrade=4.5, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+10%HP+3+4 (Vikings)": Upgrade(hp_upgrade=4.5, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+15%HP (Vikings)": Upgrade(hp_upgrade=6.75),
                                       "+15%HP+1+1 (Vikings)": Upgrade(hp_upgrade=6.75, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+15%HP+2+2 (Vikings)": Upgrade(hp_upgrade=6.75, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+15%HP+3+4 (Vikings)": Upgrade(hp_upgrade=6.75, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+20%HP (Vikings)": Upgrade(hp_upgrade=9),
                                       "+20%HP+1+1 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+20%HP+2+2 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+20%HP+3+4 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4), })


class Spearman(Unit):
    def __init__(self):
        super().__init__(45, 3, 0, 0, 0, armor_classes=(1, 27), bonus_attack_classes=(8, 5, 30, 16, 34, 35, 29,),
                         bonus_attack_values=(15, 15, 12, 9, 9, 4, 1,))


class EagleScout(Unit):
    def __init__(self):
        super().__init__(50, 4, 0, 0, 2, armor_classes=(1, 29), bonus_attack_classes=(25, 20, 8, 30, 16,),
                         bonus_attack_values=(8, 3, 2, 1, 1,), displayed_name="Eagle Scout",
                         atk_upgrades={"+5 (GarlandWars)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+ElDorado": Upgrade(hp_upgrade=40),
                                       "+ElDorado+1+1": Upgrade(hp_upgrade=40, melee_armor_upgrade=1,
                                                                pierce_armor_upgrade=1),
                                       "+ElDorado+2+2": Upgrade(hp_upgrade=40, melee_armor_upgrade=2,
                                                                pierce_armor_upgrade=2),
                                       "+ElDorado+3+4": Upgrade(hp_upgrade=40, melee_armor_upgrade=3,
                                                                pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=6), })


class Villager(Unit):
    def __init__(self):
        super().__init__(25, 3, 0, 0, 0, armor_classes=None, def_upgrades={"+loom": Upgrade(15, 0, 0, 1, 2)})


# castle


class Crossbow(Unit):
    def __init__(self):
        super().__init__(35, 0, 5, 0, 0, armor_classes=(15,), bonus_attack_classes=(27,), bonus_attack_values=(3,),
                         displayed_name="Crossbowman",
                         def_upgrades={"+4+5 (Pavise)": Upgrade(0, 0, 0, 4, 5),
                                       " (Vietnamese)": Upgrade(7, 0, 0, 0, 0),
                                       "+1+1 (Vietnamese)": Upgrade(7, 0, 0, 1, 1),
                                       "+2+2 (Vietnamese)": Upgrade(7, 0, 0, 2, 2),
                                       "+3+4 (Vietnamese)": Upgrade(7, 0, 0, 3, 4), })


class EliteSkirmisher(Unit):
    def __init__(self):
        super().__init__(35, 0, 3, 0, 4, armor_classes=(15,), bonus_attack_classes=(15, 27, 28,),
                         bonus_attack_values=(4, 3, 2,), displayed_name="Elite Skirmisher",
                         def_upgrades={"+3+6 (TowerShields)": Upgrade(0, 0, 0, 3, 6),
                                       " (Vietnamese)": Upgrade(7, 0, 0, 0, 0),
                                       "+1+1 (Vietnamese)": Upgrade(7, 0, 0, 1, 1),
                                       "+2+2 (Vietnamese)": Upgrade(7, 0, 0, 2, 2),
                                       "+3+4 (Vietnamese)": Upgrade(7, 0, 0, 3, 4),
                                       },
                         atk_upgrades={"+5 (Atlatl)": Upgrade(0, 0, 5, 0, 0)})


class Slinger(Unit):
    def __init__(self):
        super().__init__(40, 0, 4, 0, 0, armor_classes=(15, 19,), bonus_attack_classes=(1, 32, 17, 27,),
                         bonus_attack_values=(10, 10, 3, 1,),
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=6)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class CavalryArcher(Unit):
    def __init__(self):
        super().__init__(50, 0, 6, 0, 0, armor_classes=(15, 28, 8,), bonus_attack_classes=(27,),
                         bonus_attack_values=(2,), displayed_name="Cavalry Archer",
                         def_upgrades={"+4+6": Upgrade(0, 0, 0, 4, 6), "+Bl.+4+6": Upgrade(20, 0, 0, 4, 6),
                                       "+5+7 (SilkArmor)": Upgrade(0, 0, 0, 5, 7),
                                       "+Bl.+5+7 (SilkArmor)": Upgrade(20, 0, 0, 5, 7),
                                       " (Vietnamese&Franks)": Upgrade(hp_upgrade=10),
                                       "+1+1 (Vietnamese&Franks)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                           pierce_armor_upgrade=1),
                                       "+2+2 (Vietnamese&Franks)": Upgrade(hp_upgrade=10, melee_armor_upgrade=2,
                                                                           pierce_armor_upgrade=2),
                                       "+3+4 (Vietnamese)": Upgrade(hp_upgrade=10, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=4),
                                       "+Bl. (Vietnamese)": Upgrade(hp_upgrade=30),
                                       "+Bl.+1+1 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=1,
                                                                        pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=2,
                                                                        pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=3,
                                                                        pierce_armor_upgrade=4),
                                       "+Sipahi+Bl.": Upgrade(40, 0, 0, 0, 0),
                                       "+Sipahi+Bl.+1+1": Upgrade(40, 0, 0, 1, 1),
                                       "+Sipahi+Bl.+2+2": Upgrade(40, 0, 0, 2, 2),
                                       "+Sipahi+Bl.+3+4": Upgrade(40, 0, 0, 3, 4),
                                       "+Sipahi+Bl.+4+6": Upgrade(40, 0, 0, 4, 6)},
                         atk_upgrades={"+5 (RecurveBow)": Upgrade(0, 0, 5, 0, 0)})


class Genitour(Unit):
    def __init__(self):
        super().__init__(50, 0, 3, 0, 4, armor_classes=(15, 28, 8, 19,), bonus_attack_classes=(15, 27, 28,),
                         bonus_attack_values=(4, 2, 2,),
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4),
                                       "+5 (Atlatl)": Upgrade(0, 0, 5, 0, 0)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+2+3 (SilkArmor)": Upgrade(0, 0, 0, 2, 3),
                                       "+4+5 (SilkArmor)": Upgrade(0, 0, 0, 4, 5),
                                       "+Bl.+2+3 (SilkArmor)": Upgrade(20, 0, 0, 2, 3),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(20, 0, 0, 4, 5),
                                       " (Vietnamese&Franks)": Upgrade(hp_upgrade=10),
                                       "+1+1 (Vietnamese&Franks)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                           pierce_armor_upgrade=1),
                                       "+2+2 (Vietnamese&Franks)": Upgrade(hp_upgrade=10, melee_armor_upgrade=2,
                                                                           pierce_armor_upgrade=2),
                                       "+3+4 (Vietnamese)": Upgrade(hp_upgrade=10, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=4),
                                       "+Bl. (Vietnamese)": Upgrade(hp_upgrade=30),
                                       "+Bl.+1+1 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=1,
                                                                        pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=2,
                                                                        pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Vietnamese)": Upgrade(hp_upgrade=30, melee_armor_upgrade=3,
                                                                        pierce_armor_upgrade=4),
                                       "+Sipahi+Bl.": Upgrade(40, 0, 0, 0, 0),
                                       "+Sipahi+Bl.+1+1": Upgrade(40, 0, 0, 1, 1),
                                       "+Sipahi+Bl.+2+2": Upgrade(40, 0, 0, 2, 2),
                                       "+Sipahi+Bl.+3+4": Upgrade(40, 0, 0, 3, 4)}
                         )


class LongSword(Unit):
    def __init__(self):
        super().__init__(60, 9, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(6,),
                         displayed_name="Long Swordsman",
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+15%HP (Vikings)": Upgrade(hp_upgrade=9),
                                       "+15%HP+1+1 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+15%HP+2+2 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+15%HP+3+4 (Vikings)": Upgrade(hp_upgrade=9, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+20%HP (Vikings)": Upgrade(hp_upgrade=12),
                                       "+20%HP+1+1 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+20%HP+2+2 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+20%HP+3+4 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4), })


class Pikeman(Unit):
    def __init__(self):
        super().__init__(55, 4, 0, 0, 0, armor_classes=(1, 27,), bonus_attack_classes=(8, 5, 30, 16, 34, 35, 29,),
                         bonus_attack_values=(22, 25, 18, 16, 16, 11, 1),
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+15%HP (Vikings)": Upgrade(hp_upgrade=8.25),
                                       "+15%HP+1+1 (Vikings)": Upgrade(hp_upgrade=8.25, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+15%HP+2+2 (Vikings)": Upgrade(hp_upgrade=8.25, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+15%HP+3+4 (Vikings)": Upgrade(hp_upgrade=8.25, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       "+20%HP (Vikings)": Upgrade(hp_upgrade=11),
                                       "+20%HP+1+1 (Vikings)": Upgrade(hp_upgrade=11, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+20%HP+2+2 (Vikings)": Upgrade(hp_upgrade=11, melee_armor_upgrade=2,
                                                                       pierce_armor_upgrade=2),
                                       "+20%HP+3+4 (Vikings)": Upgrade(hp_upgrade=11, melee_armor_upgrade=3,
                                                                       pierce_armor_upgrade=4),
                                       })


class EagleWarrior(Unit):
    def __init__(self):
        super().__init__(55, 7, 0, 0, 3, armor_classes=(1, 29,), bonus_attack_classes=(25, 20, 8, 30, 16, 34,),
                         bonus_attack_values=(8, 3, 3, 2, 1, 1,), displayed_name="Eagle Warrior",
                         atk_upgrades={"+5 (GarlandWars)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+ElDorado": Upgrade(hp_upgrade=40),
                                       "+ElDorado+1+1": Upgrade(hp_upgrade=40, melee_armor_upgrade=1,
                                                                pierce_armor_upgrade=1),
                                       "+ElDorado+2+2": Upgrade(hp_upgrade=40, melee_armor_upgrade=2,
                                                                pierce_armor_upgrade=2),
                                       "+ElDorado+3+4": Upgrade(hp_upgrade=40, melee_armor_upgrade=3,
                                                                pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=6), })


class LightCavalry(Unit):
    def __init__(self):
        super().__init__(60, 7, 0, 0, 2, armor_classes=(8,), bonus_attack_classes=(25,), bonus_attack_values=(10,),
                         displayed_name="Light Cavalry",
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={"+4+5 (SilkArmor)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=5),
                                       " (Mongols)": Upgrade(hp_upgrade=18),
                                       "+1+1 (Mongols)": Upgrade(hp_upgrade=18, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Mongols)": Upgrade(hp_upgrade=18, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+Bl. (Mongols)": Upgrade(hp_upgrade=38),
                                       "+Bl.+1+1 (Mongols)": Upgrade(hp_upgrade=38, melee_armor_upgrade=1,
                                                                     pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Mongols)": Upgrade(hp_upgrade=38, melee_armor_upgrade=2,
                                                                     pierce_armor_upgrade=2)})


class Knight(Unit):
    def __init__(self):
        super().__init__(100, 10, 0, 2, 2, armor_classes=(8,),
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (Lithuanians)": Upgrade(melee_attack_upgrade=8), },
                         def_upgrades={"+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+Bl.+4+2 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                     pierce_armor_upgrade=2),
                                       "+Bl.+5+4 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=5,
                                                                     pierce_armor_upgrade=4)})


class CamelRider(Unit):
    def __init__(self):
        super().__init__(100, 6, 0, 0, 0, armor_classes=(30,), bonus_attack_classes=(8, 30, 16, 34,),
                         bonus_attack_values=(9, 5, 5, 5,), displayed_name="Camel Rider",
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={" (Saracens)": Upgrade(hp_upgrade=10),
                                       "+1+1 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                  pierce_armor_upgrade=1),
                                       "+2+2 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=2,
                                                                  pierce_armor_upgrade=2),
                                       "+3+4 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=3,
                                                                  pierce_armor_upgrade=4),
                                       "+Bl. (Saracens)": Upgrade(hp_upgrade=30),
                                       "+Bl.+1+1 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=1,
                                                                      pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=2,
                                                                      pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=3,
                                                                      pierce_armor_upgrade=4),
                                       "+Bl. (Zealotry)": Upgrade(hp_upgrade=50),
                                       "+Bl.+1+1 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=1,
                                                                      pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=2,
                                                                      pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=3,
                                                                      pierce_armor_upgrade=4), })


class BattleElephant(Unit):
    def __init__(self):
        super().__init__(250, 12, 0, 1, 2, armor_classes=(8, 5,), displayed_name="Battle Elephant",
                         atk_upgrades={"+3 (TuskSwords)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (TuskSwords)": Upgrade(melee_attack_upgrade=5),
                                       "+7 (TuskSwords)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={"+Chatras": Upgrade(hp_upgrade=50),
                                       "+Chatras+1+1": Upgrade(hp_upgrade=50, melee_armor_upgrade=1,
                                                               pierce_armor_upgrade=1),
                                       "+Chatras+2+2": Upgrade(hp_upgrade=50, melee_armor_upgrade=2,
                                                               pierce_armor_upgrade=2),
                                       "+Chatras+3+4": Upgrade(hp_upgrade=50, melee_armor_upgrade=3,
                                                               pierce_armor_upgrade=4),
                                       "+Chatras+Bl.": Upgrade(hp_upgrade=70),
                                       "+Chatras+Bl.+1+1": Upgrade(hp_upgrade=70, melee_armor_upgrade=1,
                                                                   pierce_armor_upgrade=1),
                                       "+Chatras+Bl.+2+2": Upgrade(hp_upgrade=70, melee_armor_upgrade=2,
                                                                   pierce_armor_upgrade=2),
                                       "+Chatras+Bl.+3+4": Upgrade(hp_upgrade=70, melee_armor_upgrade=3,
                                                                   pierce_armor_upgrade=4),
                                       "+3+3 (Howdah)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=3),
                                       "+4+5 (Howdah)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+3+3 (Howdah)": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=3),
                                       "+Bl.+4+5 (Howdah)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                    pierce_armor_upgrade=5)
                                       })


class SteppeLancer(Unit):
    def __init__(self):
        super().__init__(60, 9, 0, 0, 1, armor_classes=(8,), displayed_name="Steppe Lancer",
                         def_upgrades={"+4+5 (SilkArmor)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=5),
                                       " (Mongols)": Upgrade(hp_upgrade=18),
                                       "+1+1 (Mongols)": Upgrade(hp_upgrade=18, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Mongols)": Upgrade(hp_upgrade=18, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+Bl. (Mongols)": Upgrade(hp_upgrade=38),
                                       "+Bl.+1+1 (Mongols)": Upgrade(hp_upgrade=38, melee_armor_upgrade=1,
                                                                     pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Mongols)": Upgrade(hp_upgrade=38, melee_armor_upgrade=2,
                                                                     pierce_armor_upgrade=2)})


class BatteringRam(Unit):
    def __init__(self):
        super().__init__(175, 2, 0, -3, 180, armor_classes=(20, 17,), bonus_attack_classes=(20,),
                         bonus_attack_values=(40,), displayed_name="Battering Ram",
                         def_upgrades={"+FurorCeltica": Upgrade(hp_upgrade=70),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)})


class Mangonel(Unit):
    def __init__(self):
        super().__init__(50, 40, 0, 0, 6, armor_classes=(20,), bonus_attack_classes=(20,), bonus_attack_values=(12,),
                         def_upgrades={"FurorCeltica": Upgrade(hp_upgrade=20),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)},
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1)})


class Scorpion(Unit):
    def __init__(self):
        super().__init__(40, 0, 12, 0, 7, armor_classes=(20,), bonus_attack_classes=(5, 17,),
                         bonus_attack_values=(6, 1,),
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+4 (Rocketry)": Upgrade(pierce_attack_upgrade=4),
                                       "+5 (Rocketry)": Upgrade(pierce_attack_upgrade=5)},
                         def_upgrades={"+FurorCeltica": Upgrade(hp_upgrade=16),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)})


class Monk(Unit):
    def __init__(self):
        super().__init__(30, 0, 0, 0, 0, armor_classes=(25,),
                         def_upgrades={"+3+3 (Orthodoxy)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=3),
                                       "+15HP +3+3 (Orthodoxy)": Upgrade(hp_upgrade=15, melee_armor_upgrade=3,
                                                                         pierce_armor_upgrade=3),
                                       "+5HP (Aztecs)": Upgrade(hp_upgrade=5),
                                       "+10HP (Aztecs)": Upgrade(hp_upgrade=10),
                                       "+15HP (Sanctity)": Upgrade(hp_upgrade=15),
                                       "+20HP (Aztecs)": Upgrade(hp_upgrade=20),
                                       "+25HP (Aztecs)": Upgrade(hp_upgrade=25),
                                       "+30HP (Aztecs)": Upgrade(hp_upgrade=30),
                                       "+35HP (Aztecs)": Upgrade(hp_upgrade=35),
                                       "+40HP (Aztecs)": Upgrade(hp_upgrade=40),
                                       "+45HP (Aztecs)": Upgrade(hp_upgrade=45),
                                       "+50HP (Aztecs)": Upgrade(hp_upgrade=50),
                                       "+55HP (Aztecs)": Upgrade(hp_upgrade=55),
                                       "+60HP (Aztecs)": Upgrade(hp_upgrade=60),
                                       "+65HP (Aztecs)": Upgrade(hp_upgrade=65), })


# imp
class Arbalest(Unit):
    def __init__(self):
        super().__init__(40, 0, 6, 0, 0, armor_classes=(15,), bonus_attack_classes=(27,), bonus_attack_values=(3,),
                         def_upgrades={"+4+5 (Pavise)": Upgrade(0, 0, 0, 4, 5),
                                       " (Vietnamese)": Upgrade(8, 0, 0, 0, 0),
                                       "+1+1 (Vietnamese)": Upgrade(8, 0, 0, 1, 1),
                                       "+2+2 (Vietnamese)": Upgrade(8, 0, 0, 2, 2),
                                       "+3+4 (Vietnamese)": Upgrade(8, 0, 0, 3, 4), })


class ImperialSkirmisher(Unit):
    def __init__(self):
        super().__init__(35, 0, 4, 0, 5, armor_classes=(15,), bonus_attack_classes=(15, 27, 28,),
                         bonus_attack_values=(5, 3, 3,), displayed_name="Imperial Skirmisher",
                         def_upgrades={"+3+6 (TowerShields)": Upgrade(0, 0, 0, 3, 6),
                                       " (Vietnamese)": Upgrade(7, 0, 0, 0, 0),
                                       "+1+1 (Vietnamese)": Upgrade(7, 0, 0, 1, 1),
                                       "+2+2 (Vietnamese)": Upgrade(7, 0, 0, 2, 2),
                                       "+3+4 (Vietnamese)": Upgrade(7, 0, 0, 3, 4),
                                       },
                         atk_upgrades={"+5 (Atlatl)": Upgrade(0, 0, 5, 0, 0)})


class HandCannoneer(Unit):
    def __init__(self):
        super().__init__(35, 0, 17, 1, 0, armor_classes=(15, 23,), bonus_attack_classes=(1, 17, 27,),
                         bonus_attack_values=(10, 2, 1,), displayed_name="Hand Cannoneer",
                         def_upgrades={" (Turks)": Upgrade(hp_upgrade=8.75),
                                       "+1+1 (Turks)": Upgrade(hp_upgrade=8.75, melee_armor_upgrade=1,
                                                               pierce_armor_upgrade=1),
                                       "+2+2 (Turks)": Upgrade(hp_upgrade=8.75, melee_armor_upgrade=2,
                                                               pierce_armor_upgrade=2),
                                       "+3+4 (Turks)": Upgrade(hp_upgrade=8.75, melee_armor_upgrade=3,
                                                               pierce_armor_upgrade=4), })


class HeavyCavalryArcher(Unit):
    def __init__(self):
        super().__init__(60, 0, 7, 1, 0, armor_classes=(15, 28, 8,), bonus_attack_classes=(27,),
                         bonus_attack_values=(2,), displayed_name="Heavy Cavalry Archer",
                         def_upgrades={"+4+6": Upgrade(0, 0, 0, 4, 6), "+Bl.+4+6": Upgrade(20, 0, 0, 4, 6),
                                       "+5+7 (SilkArmor)": Upgrade(0, 0, 0, 5, 7),
                                       "+Bl.+5+7 (SilkArmor)": Upgrade(20, 0, 0, 5, 7),
                                       " (Vietnamese&Franks)": Upgrade(hp_upgrade=12),
                                       "+1+1 (Vietnamese&Franks)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                           pierce_armor_upgrade=1),
                                       "+2+2 (Vietnamese&Franks)": Upgrade(hp_upgrade=12, melee_armor_upgrade=2,
                                                                           pierce_armor_upgrade=2),
                                       "+3+4 (Vietnamese)": Upgrade(hp_upgrade=12, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=4),
                                       "+Bl. (Vietnamese)": Upgrade(hp_upgrade=32),
                                       "+Bl.+1+1 (Vietnamese)": Upgrade(hp_upgrade=32, melee_armor_upgrade=1,
                                                                        pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Vietnamese)": Upgrade(hp_upgrade=32, melee_armor_upgrade=2,
                                                                        pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Vietnamese)": Upgrade(hp_upgrade=32, melee_armor_upgrade=3,
                                                                        pierce_armor_upgrade=4),
                                       "+Sipahi+Bl.": Upgrade(40, 0, 0, 0, 0),
                                       "+Sipahi+Bl.+1+1": Upgrade(40, 0, 0, 1, 1),
                                       "+Sipahi+Bl.+2+2": Upgrade(40, 0, 0, 2, 2),
                                       "+Sipahi+Bl.+3+4": Upgrade(40, 0, 0, 3, 4),
                                       "+Sipahi+Bl.+4+6": Upgrade(40, 0, 0, 4, 6)},
                         atk_upgrades={"+5 (RecurveBow)": Upgrade(0, 0, 5, 0, 0)})


class EliteGenitour(Unit):
    def __init__(self):
        super().__init__(55, 0, 4, 0, 4, armor_classes=(15, 28, 8, 19,), armor_class_values=(0, 1, 0, 0,),
                         bonus_attack_classes=(15, 27, 28,), bonus_attack_values=(5, 2, 2,),
                         displayed_name="Elite Genitour",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4),
                                       "+5 (Atlatl)": Upgrade(0, 0, 5, 0, 0)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+2+3 (SilkArmor)": Upgrade(0, 0, 0, 2, 3),
                                       "+4+5 (SilkArmor)": Upgrade(0, 0, 0, 4, 5),
                                       "+Bl.+2+3 (SilkArmor)": Upgrade(20, 0, 0, 2, 3),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(20, 0, 0, 4, 5),
                                       " (Vietnamese&Franks)": Upgrade(hp_upgrade=11),
                                       "+1+1 (Vietnamese&Franks)": Upgrade(hp_upgrade=11, melee_armor_upgrade=1,
                                                                           pierce_armor_upgrade=1),
                                       "+2+2 (Vietnamese&Franks)": Upgrade(hp_upgrade=11, melee_armor_upgrade=2,
                                                                           pierce_armor_upgrade=2),
                                       "+3+4 (Vietnamese)": Upgrade(hp_upgrade=11, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=4),
                                       "+Bl. (Vietnamese)": Upgrade(hp_upgrade=31),
                                       "+Bl.+1+1 (Vietnamese)": Upgrade(hp_upgrade=31, melee_armor_upgrade=1,
                                                                        pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Vietnamese)": Upgrade(hp_upgrade=31, melee_armor_upgrade=2,
                                                                        pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Vietnamese)": Upgrade(hp_upgrade=31, melee_armor_upgrade=3,
                                                                        pierce_armor_upgrade=4),
                                       "+Sipahi+Bl.": Upgrade(40, 0, 0, 0, 0),
                                       "+Sipahi+Bl.+1+1": Upgrade(40, 0, 0, 1, 1),
                                       "+Sipahi+Bl.+2+2": Upgrade(40, 0, 0, 2, 2),
                                       "+Sipahi+Bl.+3+4": Upgrade(40, 0, 0, 3, 4)})


class TwoHandedSwordsman(Unit):
    def __init__(self):
        super().__init__(60, 12, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(8,),
                         displayed_name="Two-Handed Swordsman",
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       " (Vikings)": Upgrade(hp_upgrade=12),
                                       "+1+1 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+3+4 (Vikings)": Upgrade(hp_upgrade=12, melee_armor_upgrade=3,
                                                                 pierce_armor_upgrade=4),
                                       "+8+4 (Bagains)": Upgrade(melee_armor_upgrade=8, pierce_armor_upgrade=4), })


class Champion(Unit):
    def __init__(self):
        super().__init__(70, 13, 0, 1, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(8,),
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       " (Vikings)": Upgrade(hp_upgrade=14),
                                       "+1+1 (Vikings)": Upgrade(hp_upgrade=14, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Vikings)": Upgrade(hp_upgrade=14, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+3+4 (Vikings)": Upgrade(hp_upgrade=14, melee_armor_upgrade=3,
                                                                 pierce_armor_upgrade=4), })


class Halberdier(Unit):
    def __init__(self):
        super().__init__(60, 6, 0, 0, 0, armor_classes=(1, 27,), bonus_attack_classes=(8, 5, 30, 16, 34, 35, 29,),
                         bonus_attack_values=(32, 28, 26, 17, 17, 11, 1,),
                         atk_upgrades={"+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={"+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4)})


class EliteEagleWarrior(Unit):
    def __init__(self):
        super().__init__(60, 9, 0, 0, 4, armor_classes=(1, 29,), bonus_attack_classes=(25, 20, 8, 30, 16, 34,),
                         bonus_attack_values=(10, 5, 4, 3, 2, 2,), displayed_name="Elite Eagle Warrior",
                         atk_upgrades={"+5 (GarlandWars)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+ElDorado": Upgrade(hp_upgrade=40),
                                       "+ElDorado+1+1": Upgrade(hp_upgrade=40, melee_armor_upgrade=1,
                                                                pierce_armor_upgrade=1),
                                       "+ElDorado+2+2": Upgrade(hp_upgrade=40, melee_armor_upgrade=2,
                                                                pierce_armor_upgrade=2),
                                       "+ElDorado+3+4": Upgrade(hp_upgrade=40, melee_armor_upgrade=3,
                                                                pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=6), })


class Condottiero(Unit):
    def __init__(self):
        super().__init__(80, 10, 0, 1, 0, armor_classes=(1, 19, 32,), armor_class_values=(10, 0, 0,),
                         bonus_attack_classes=(23,), bonus_attack_values=(10,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4),
                                       "+3 (Burmese)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (Burmese)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Burmese)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+0+3 (Malians)": Upgrade(pierce_armor_upgrade=3),
                                       "+2+5 (Malians)": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=5),
                                       "+3+7 (Malians)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=7),
                                       "+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       " (Vikings)": Upgrade(hp_upgrade=16),
                                       "+1+1 (Vikings)": Upgrade(hp_upgrade=16, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Vikings)": Upgrade(hp_upgrade=16, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+3+4 (Vikings)": Upgrade(hp_upgrade=16, melee_armor_upgrade=3,
                                                                 pierce_armor_upgrade=4), })


class Hussar(Unit):
    def __init__(self):
        super().__init__(75, 7, 0, 0, 2, armor_classes=(8,), bonus_attack_classes=(25,), bonus_attack_values=(12,),
                         def_upgrades={"+4+5 (SilkArmor)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=5),
                                       " (Mongols)": Upgrade(hp_upgrade=22.5),
                                       "+1+1 (Mongols)": Upgrade(hp_upgrade=22.5, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Mongols)": Upgrade(hp_upgrade=22.5, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+Bl. (Mongols)": Upgrade(hp_upgrade=42.5),
                                       "+Bl.+1+1 (Mongols)": Upgrade(hp_upgrade=42.5, melee_armor_upgrade=1,
                                                                     pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Mongols)": Upgrade(hp_upgrade=42.5, melee_armor_upgrade=2,
                                                                     pierce_armor_upgrade=2)})


class Cavalier(Unit):
    def __init__(self):
        super().__init__(120, 12, 0, 2, 2, armor_classes=(8,),
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (Lithuanians)": Upgrade(melee_attack_upgrade=8), },
                         def_upgrades={"+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+Bl.+4+2 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                     pierce_armor_upgrade=2),
                                       "+Bl.+5+4 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=5,
                                                                     pierce_armor_upgrade=4),
                                       " (Franks)": Upgrade(hp_upgrade=24),
                                       "+1+1 (Franks)": Upgrade(hp_upgrade=24, melee_armor_upgrade=1,
                                                                pierce_armor_upgrade=1),
                                       "+2+2 (Franks)": Upgrade(hp_upgrade=24, melee_armor_upgrade=2,
                                                                pierce_armor_upgrade=2),
                                       "+3+4 (Franks)": Upgrade(hp_upgrade=24, melee_armor_upgrade=3,
                                                                pierce_armor_upgrade=4)})


class Paladin(Unit):
    def __init__(self):
        super().__init__(160, 14, 0, 2, 3, armor_classes=(8,),
                         atk_upgrades={"+5 (Lithuanians)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Lithuanians)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Lithuanians)": Upgrade(melee_attack_upgrade=7),
                                       "+8 (Lithuanians)": Upgrade(melee_attack_upgrade=8), },
                         def_upgrades={"+4+2 (Teutons)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=2),
                                       "+5+4 (Teutons)": Upgrade(melee_armor_upgrade=5, pierce_armor_upgrade=4),
                                       "+Bl.+4+2 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                     pierce_armor_upgrade=2),
                                       "+Bl.+5+4 (Teutons)": Upgrade(hp_upgrade=20, melee_armor_upgrade=5,
                                                                     pierce_armor_upgrade=4),
                                       " (Franks)": Upgrade(hp_upgrade=32),
                                       "+1+1 (Franks)": Upgrade(hp_upgrade=32, melee_armor_upgrade=1,
                                                                pierce_armor_upgrade=1),
                                       "+2+2 (Franks)": Upgrade(hp_upgrade=32, melee_armor_upgrade=2,
                                                                pierce_armor_upgrade=2),
                                       "+3+4 (Franks)": Upgrade(hp_upgrade=32, melee_armor_upgrade=3,
                                                                pierce_armor_upgrade=4)})


class HeavyCamel(Unit):
    def __init__(self):
        super().__init__(120, 7, 0, 0, 0, armor_classes=(30,), bonus_attack_classes=(8, 30, 16, 34, 35,),
                         bonus_attack_values=(18, 9, 9, 9, 7), displayed_name="Heavy Camel Rider",
                         atk_upgrades={"+5 (Farimba)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (Farimba)": Upgrade(melee_attack_upgrade=6),
                                       "+7 (Farimba)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={" (Saracens)": Upgrade(hp_upgrade=10),
                                       "+1+1 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                  pierce_armor_upgrade=1),
                                       "+2+2 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=2,
                                                                  pierce_armor_upgrade=2),
                                       "+3+4 (Saracens)": Upgrade(hp_upgrade=10, melee_armor_upgrade=3,
                                                                  pierce_armor_upgrade=4),
                                       "+Bl. (Saracens)": Upgrade(hp_upgrade=30),
                                       "+Bl.+1+1 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=1,
                                                                      pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=2,
                                                                      pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Saracens)": Upgrade(hp_upgrade=30, melee_armor_upgrade=3,
                                                                      pierce_armor_upgrade=4),
                                       "+Bl. (Zealotry)": Upgrade(hp_upgrade=50),
                                       "+Bl.+1+1 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=1,
                                                                      pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=2,
                                                                      pierce_armor_upgrade=2),
                                       "+Bl.+3+4 (Zealotry)": Upgrade(hp_upgrade=50, melee_armor_upgrade=3,
                                                                      pierce_armor_upgrade=4), })


class ImperialCamel(Unit):
    def __init__(self):
        super().__init__(140, 9, 0, 0, 0, armor_classes=(30,), bonus_attack_classes=(8, 30, 16, 34, 35,),
                         bonus_attack_values=(18, 9, 9, 9, 7), displayed_name="Imperial Camel Rider")


class EliteBattleElephant(Unit):
    def __init__(self):
        super().__init__(300, 14, 0, 1, 3, armor_classes=(8, 5,), displayed_name="Elite Battle Elephant",
                         atk_upgrades={"+3 (TuskSwords)": Upgrade(melee_attack_upgrade=3),
                                       "+5 (TuskSwords)": Upgrade(melee_attack_upgrade=5),
                                       "+7 (TuskSwords)": Upgrade(melee_attack_upgrade=7)},
                         def_upgrades={"+Chatras": Upgrade(hp_upgrade=50),
                                       "+Chatras+1+1": Upgrade(hp_upgrade=50, melee_armor_upgrade=1,
                                                               pierce_armor_upgrade=1),
                                       "+Chatras+2+2": Upgrade(hp_upgrade=50, melee_armor_upgrade=2,
                                                               pierce_armor_upgrade=2),
                                       "+Chatras+3+4": Upgrade(hp_upgrade=50, melee_armor_upgrade=3,
                                                               pierce_armor_upgrade=4),
                                       "+Chatras+Bl.": Upgrade(hp_upgrade=70),
                                       "+Chatras+Bl.+1+1": Upgrade(hp_upgrade=70, melee_armor_upgrade=1,
                                                                   pierce_armor_upgrade=1),
                                       "+Chatras+Bl.+2+2": Upgrade(hp_upgrade=70, melee_armor_upgrade=2,
                                                                   pierce_armor_upgrade=2),
                                       "+Chatras+Bl.+3+4": Upgrade(hp_upgrade=70, melee_armor_upgrade=3,
                                                                   pierce_armor_upgrade=4),
                                       "+3+3 (Howdah)": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=3),
                                       "+4+5 (Howdah)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+3+3 (Howdah)": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                                    pierce_armor_upgrade=3),
                                       "+Bl.+4+5 (Howdah)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                    pierce_armor_upgrade=5)
                                       })


class EliteSteppeLancer(Unit):
    def __init__(self):
        super().__init__(80, 11, 0, 0, 1, armor_classes=(8,), displayed_name="Elite Steppe Lancer",
                         def_upgrades={"+4+5 (SilkArmor)": Upgrade(melee_armor_upgrade=4, pierce_armor_upgrade=5),
                                       "+Bl.+4+5 (SilkArmor)": Upgrade(hp_upgrade=20, melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=5),
                                       " (Mongols)": Upgrade(hp_upgrade=24),
                                       "+1+1 (Mongols)": Upgrade(hp_upgrade=24, melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+2+2 (Mongols)": Upgrade(hp_upgrade=24, melee_armor_upgrade=2,
                                                                 pierce_armor_upgrade=2),
                                       "+Bl. (Mongols)": Upgrade(hp_upgrade=44),
                                       "+Bl.+1+1 (Mongols)": Upgrade(hp_upgrade=44, melee_armor_upgrade=1,
                                                                     pierce_armor_upgrade=1),
                                       "+Bl.+2+2 (Mongols)": Upgrade(hp_upgrade=44, melee_armor_upgrade=2,
                                                                     pierce_armor_upgrade=2)})


class CappedRam(Unit):
    def __init__(self):
        super().__init__(200, 3, 0, -3, 190, armor_classes=(20, 17,), armor_class_values=(0, 1,),
                         bonus_attack_classes=(20,), bonus_attack_values=(50,), displayed_name="Capped Ram",
                         def_upgrades={"+FurorCeltica": Upgrade(hp_upgrade=80),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)})


class SiegeRam(Unit):
    def __init__(self):
        super().__init__(270, 4, 0, -3, 195, armor_classes=(20, 17,), armor_class_values=(0, 2,),
                         bonus_attack_classes=(20,), bonus_attack_values=(65,), displayed_name="Siege Ram",
                         def_upgrades={"+FurorCeltica": Upgrade(hp_upgrade=108)})


class Onager(Unit):
    def __init__(self):
        super().__init__(60, 50, 0, 0, 7, armor_classes=(20,), bonus_attack_classes=(20,), bonus_attack_values=(12,),
                         def_upgrades={"FurorCeltica": Upgrade(hp_upgrade=24),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)},
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1)})


class SiegeOnager(Unit):
    def __init__(self):
        super().__init__(70, 75, 0, 0, 8, armor_classes=(20,), bonus_attack_classes=(20,), bonus_attack_values=(12,),
                         displayed_name="Siege Onager",
                         def_upgrades={"FurorCeltica": Upgrade(hp_upgrade=28),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)},
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1)})


class HeavyScorpion(Unit):
    def __init__(self):
        super().__init__(50, 0, 16, 0, 7, armor_classes=(20,), bonus_attack_classes=(5, 17,),
                         bonus_attack_values=(8, 5,), displayed_name="Heavy Scorpion",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+4 (Rocketry)": Upgrade(pierce_attack_upgrade=4),
                                       "+5 (Rocketry)": Upgrade(pierce_attack_upgrade=5)},
                         def_upgrades={"+FurorCeltica": Upgrade(hp_upgrade=20),
                                       "+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)})


class BombardCannon(Unit):
    def __init__(self):
        super().__init__(80, 40, 0, 2, 5, armor_classes=(20, 23,), bonus_attack_classes=(16, 34, 20,),
                         bonus_attack_values=(40, 40, 20), displayed_name="Bombard Cannon",
                         def_upgrades={"+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4),
                                       " (Turks)": Upgrade(hp_upgrade=20)})


class Petard(Unit):
    def __init__(self):
        super().__init__(50, 25, 0, 0, 2, armor_classes=(), bonus_attack_classes=(20,), bonus_attack_values=(60,))


class TrebuchetPacked(Unit):
    def __init__(self):
        super().__init__(150, 0, 200, 2, 8, armor_classes=(20,), displayed_name="Trebuchet (packed)",
                         def_upgrades={"+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1)})


class TrebuchetUnpacked(Unit):
    def __init__(self):
        super().__init__(150, 0, 200, 1, 150, armor_classes=(20, 17,), displayed_name="Trebuchet (unpacked)",
                         def_upgrades={"+4+0 (Ironclad)": Upgrade(melee_armor_upgrade=4)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1)})


class FishingShip(Unit):
    def __init__(self):
        super().__init__(60, 0, 0, 0, 4, armor_classes=(34,), displayed_name="Fishing Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=6),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=6, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=6, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "2xHP+0+2 (Japanese)": Upgrade(hp_upgrade=60, pierce_armor_upgrade=2),
                                       "2xHP+0+3 (Japanese)": Upgrade(hp_upgrade=60, pierce_armor_upgrade=3), })


class TransportShip(Unit):
    def __init__(self):
        super().__init__(100, 0, 0, 4, 8, armor_classes=(16,), displayed_name="Transport Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=10),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+100%HP (Saracens)": Upgrade(hp_upgrade=100),
                                       "+100%HP+0+1 (Saracens)": Upgrade(hp_upgrade=100, pierce_armor_upgrade=1), })


class FireGalley(Unit):
    def __init__(self):
        super().__init__(100, 0, 1, 0, 4, armor_classes=(16,), armor_class_values=(6,),
                         bonus_attack_classes=(16, 2, 34,), bonus_attack_values=(3, 1, 1,),
                         displayed_name="Fire Galley",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=10),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=10, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2), })


class TradeCog(Unit):
    def __init__(self):
        super().__init__(80, 0, 0, 0, 6, armor_classes=(16,), displayed_name="Trade Cog",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=8),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=8, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=8, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2), })


class DemolitionRaft(Unit):
    def __init__(self):
        super().__init__(45, 90, 0, 0, 2, armor_classes=(16,), armor_class_values=(1,),
                         displayed_name="Demolition Raft",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=4.5),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=4.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=4.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+50%HP (Chinese)": Upgrade(hp_upgrade=22.5),
                                       "+50%HP+0+1 (Chinese)": Upgrade(hp_upgrade=22.5, pierce_armor_upgrade=1)})


class Galley(Unit):
    def __init__(self):
        super().__init__(120, 0, 6, 0, 6, armor_classes=(16,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(8, 8, 3,),
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=12),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2), },
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class FireShip(Unit):
    def __init__(self):
        super().__init__(120, 1, 2, 0, 6, armor_classes=(16,), armor_class_values=(6,),
                         bonus_attack_classes=(16, 34, 2,), bonus_attack_values=(3, 3, 2,),
                         displayed_name="Fire Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=12),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=12, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2), })


class DemolitionShip(Unit):
    def __init__(self):
        super().__init__(60, 110, 0, 0, 3, armor_classes=(16,), armor_class_values=(3,),
                         displayed_name="Demolition Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=6),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=6, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=6, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+50%HP (Chinese)": Upgrade(hp_upgrade=30),
                                       "+50%HP+0+1 (Chinese)": Upgrade(hp_upgrade=30, pierce_armor_upgrade=1)})


class WarGalley(Unit):
    def __init__(self):
        super().__init__(135, 0, 7, 0, 6, armor_classes=(16,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(9, 9, 4,), displayed_name="War Galley",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=13.5),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=13.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=13.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2), },
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class TurtleShip(Unit):
    def __init__(self):
        super().__init__(200, 50, 0, 6, 5, armor_classes=(16, 2, 23, 19,), armor_class_values=(8, 0, 0, 0,),
                         displayed_name="Turtle Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1)})


class Longboat(Unit):
    def __init__(self):
        super().__init__(130, 0, 7, 0, 6, armor_classes=(16, 19,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(9, 9, 4),
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class Caravel(Unit):
    def __init__(self):
        super().__init__(143, 0, 6, 0, 8, armor_classes=(16, 19,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(6, 6, 4),
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+1+1 (Carrack)": Upgrade(melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+1+2 (Carrack)": Upgrade(melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=2), },
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class FastFireShip(Unit):
    def __init__(self):
        super().__init__(140, 1, 3, 0, 8, armor_classes=(16,), armor_class_values=(9,),
                         bonus_attack_classes=(16, 34, 2,),
                         bonus_attack_values=(4, 4, 3,), displayed_name="Fast Fire Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1)})


class CannonGalleon(Unit):
    def __init__(self):
        super().__init__(120, 35, 0, 0, 6, armor_classes=(16, 23,), bonus_attack_classes=(20, 1, 15, 8, 35,),
                         bonus_attack_values=(40, 15, 15, 15, 4), displayed_name="Cannon Galleon",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=13.5),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=13.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=13.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+25%HP (Turks)": Upgrade(hp_upgrade=30),
                                       "+25%HP+0+1 (Turks)": Upgrade(hp_upgrade=30, pierce_armor_upgrade=1)})


class HeavyDemo(Unit):
    def __init__(self):
        super().__init__(70, 140, 0, 0, 5, armor_classes=(16,), armor_class_values=(5,),
                         displayed_name="Heavy Demolition Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=7),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=7, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=7, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+50%HP (Chinese)": Upgrade(hp_upgrade=35),
                                       "+50%HP+0+1 (Chinese)": Upgrade(hp_upgrade=35, pierce_armor_upgrade=1)})


class Galleon(Unit):
    def __init__(self):
        super().__init__(165, 0, 8, 0, 8, armor_classes=(16,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(11, 11, 4,),
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=16.5),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=16.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=16.5, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class EliteTurtleShip(Unit):
    def __init__(self):
        super().__init__(300, 50, 0, 8, 6, armor_classes=(16, 2, 23, 19,), armor_class_values=(11, 1, 0, 0,),
                         displayed_name="Elite Turtle Ship",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1)})


class EliteLongboat(Unit):
    def __init__(self):
        super().__init__(160, 0, 8, 0, 8, armor_classes=(16, 19,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(11, 11, 4,), displayed_name="Elite Longboat",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1)},
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class EliteCaravel(Unit):
    def __init__(self):
        super().__init__(165, 0, 8, 0, 8, armor_classes=(16, 19,), bonus_attack_classes=(16, 34, 17,),
                         bonus_attack_values=(7, 7, 4),
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+1+1 (Carrack)": Upgrade(melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=1),
                                       "+1+2 (Carrack)": Upgrade(melee_armor_upgrade=1,
                                                                 pierce_armor_upgrade=2), },
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), })


class EliteCannonGalleon(Unit):
    def __init__(self):
        super().__init__(150, 45, 0, 0, 8, armor_classes=(16, 23,), bonus_attack_classes=(20, 1, 15, 8, 35,),
                         bonus_attack_values=(40, 15, 15, 15, 4), displayed_name="Elite Cannon Galleon",
                         def_upgrades={"+0+1": Upgrade(pierce_armor_upgrade=1),
                                       "+10%HP (Portuguese)": Upgrade(hp_upgrade=15),
                                       "+10%HP+1+1 (Carrack)": Upgrade(hp_upgrade=15, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=1),
                                       "+10%HP+1+2 (Carrack)": Upgrade(hp_upgrade=15, melee_armor_upgrade=1,
                                                                       pierce_armor_upgrade=2),
                                       "+25%HP (Turks)": Upgrade(hp_upgrade=37.5),
                                       "+25%HP+0+1 (Turks)": Upgrade(hp_upgrade=37.5, pierce_armor_upgrade=1)})


class JaguarWarrior(Unit):
    def __init__(self):
        super().__init__(50, 10, 0, 1, 1, armor_classes=(1, 19,), bonus_attack_classes=(1, 32, 29,),
                         bonus_attack_values=(10, 10, 2,),
                         displayed_name="Jaguar Warrior",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4),
                                       "+5 (GarlandWars)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4), })


class EliteJaguarWarrior(Unit):
    def __init__(self):
        super().__init__(75, 12, 0, 2, 1, armor_classes=(1, 19,), bonus_attack_classes=(1, 32, 29,),
                         bonus_attack_values=(11, 10, 2,),
                         displayed_name="Elite Jaguar Warrior",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4),
                                       "+5 (GarlandWars)": Upgrade(melee_attack_upgrade=5),
                                       "+6 (GarlandWars)": Upgrade(melee_attack_upgrade=6),
                                       "+8 (GarlandWars)": Upgrade(melee_attack_upgrade=8)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4), })


class CamelArcher(Unit):
    def __init__(self):
        super().__init__(55, 0, 7, 0, 1, armor_classes=(15, 28, 30, 19,), bonus_attack_classes=(28,),
                         bonus_attack_values=(4,), displayed_name="Camel Archer",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4), })


class EliteCamelArcher(Unit):
    def __init__(self):
        super().__init__(60, 0, 8, 1, 1, armor_classes=(15, 28, 30, 19,), bonus_attack_classes=(28,),
                         bonus_attack_values=(6,), displayed_name="Elite Camel Archer",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4), })


class Longbowman(Unit):
    def __init__(self):
        super().__init__(35, 0, 6, 0, 0, armor_classes=(15, 19,), bonus_attack_classes=(27,),
                         bonus_attack_values=(2,),
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4), })


class EliteLongbowman(Unit):
    def __init__(self):
        super().__init__(40, 0, 7, 0, 1, armor_classes=(15, 19,), bonus_attack_classes=(27,),
                         bonus_attack_values=(2,),
                         displayed_name="Elite Longbowman",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4), })


class Konnik(Unit):
    def __init__(self):
        super().__init__(100, 12, 0, 2, 1, armor_classes=(8, 19,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4), })


class EliteKonnik(Unit):
    def __init__(self):
        super().__init__(120, 14, 0, 2, 2, armor_classes=(8, 19,), displayed_name="Elite Konnik",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4), })


class KonnikDismounted(Unit):
    def __init__(self):
        super().__init__(45, 12, 0, 0, 0, armor_classes=(1, 19,), displayed_name="Konnik (dismounted)",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4), })


class EliteKonnikDismounted(Unit):
    def __init__(self):
        super().__init__(50, 13, 0, 0, 1, armor_classes=(1, 19,), displayed_name="Elite Konnik (dismounted)",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class CoustillierNoCharge(Unit):
    def __init__(self):
        super().__init__(115, 8, 0, 2, 2, armor_classes=(8, 19,), displayed_name="Coustillier (no charge)",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class EliteCoustillierNoCharge(Unit):
    def __init__(self):
        super().__init__(145, 11, 0, 2, 2, armor_classes=(8, 19,), displayed_name="Elite Coustillier (no charge)",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class FlemishMilitia(Unit):
    def __init__(self):
        super().__init__(75, 12, 0, 1, 1, armor_classes=(1, 19,), bonus_attack_classes=(8, 30, 5, 16, 29,),
                         bonus_attack_values=(8, 6, 8, 6, 2,), displayed_name="Flemish Militia",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class Arambai(Unit):
    def __init__(self):
        super().__init__(60, 0, 12, 0, 1, armor_classes=(15, 28, 8, 19,), bonus_attack_classes=(17,),
                         bonus_attack_values=(2,),
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1)})


class EliteArambai(Unit):
    def __init__(self):
        super().__init__(65, 0, 15, 0, 2, armor_classes=(15, 28, 8, 19,), bonus_attack_classes=(17,),
                         bonus_attack_values=(2,),
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1)})


class Cataphract(Unit):
    def __init__(self):
        super().__init__(110, 9, 0, 2, 1, armor_classes=(8, 19,), armor_class_values=(12, 0,),
                         bonus_attack_classes=(1, 32,), bonus_attack_values=(9, 9,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class EliteCataphract(Unit):
    def __init__(self):
        super().__init__(150, 12, 0, 2, 1, armor_classes=(8, 19,), armor_class_values=(16, 0,),
                         bonus_attack_classes=(1, 32,), bonus_attack_values=(12, 10,),
                         displayed_name="Elite Cataphract",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class WoadRaider(Unit):
    def __init__(self):
        super().__init__(65, 8, 0, 0, 1, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(2,),
                         displayed_name="Woad Raider",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class EliteWoadRaider(Unit):
    def __init__(self):
        super().__init__(80, 13, 0, 0, 1, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(3,),
                         displayed_name="Elite Woad Raider",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


# class ChuKoNu(Unit):

# class Kipchak(Unit):

class ShotelWarrior(Unit):
    def __init__(self):
        super().__init__(40, 16, 0, 0, 0, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(2,),
                         displayed_name="Shotel Warrior",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class EliteShotelWarrior(Unit):
    def __init__(self):
        super().__init__(50, 18, 0, 0, 1, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(2,),
                         displayed_name="Shotel Warrior",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class ThrowingAxeman(Unit):
    def __init__(self):
        super().__init__(60, 7, 0, 0, 0, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(1,),
                         displayed_name="Throwing Axeman",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class EliteThrowingAxeman(Unit):
    def __init__(self):
        super().__init__(70, 8, 0, 1, 0, armor_classes=(1, 19,), bonus_attack_classes=(29,),
                         bonus_attack_values=(2,),
                         displayed_name="Elite Throwing Axeman",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4)})


class Huskarl(Unit):
    def __init__(self):
        super().__init__(60, 10, 0, 0, 6, armor_classes=(1, 19,), bonus_attack_classes=(15, 29,),
                         bonus_attack_values=(6, 2,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2), })


class EliteHuskarl(Unit):
    def __init__(self):
        super().__init__(70, 12, 0, 0, 8, armor_classes=(1, 19,), bonus_attack_classes=(15, 29,),
                         bonus_attack_values=(10, 3,),
                         displayed_name="Elite Huskarl",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2), })


class Tarkan(Unit):
    def __init__(self):
        super().__init__(100, 8, 0, 1, 3, armor_classes=(8, 19,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4)})


class EliteTarkan(Unit):
    def __init__(self):
        super().__init__(150, 11, 0, 1, 4, armor_classes=(8, 19,), displayed_name="Elite Tarkan",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4)})


class Kamayuk(Unit):
    def __init__(self):
        super().__init__(60, 7, 0, 0, 0, armor_classes=(1, 19,), bonus_attack_classes=(5, 8, 30, 25,),
                         bonus_attack_values=(20, 8, 6, 1),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=6)})


class EliteKamayuk(Unit):
    def __init__(self):
        super().__init__(80, 8, 0, 1, 0, armor_classes=(1, 19,), bonus_attack_classes=(5, 8, 30, 25,),
                         bonus_attack_values=(20, 12, 10, 1), displayed_name="Elite Kamayuk",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+6 (FabricShields)": Upgrade(melee_armor_upgrade=4,
                                                                       pierce_armor_upgrade=6)})


class ElephantArcher(Unit):
    def __init__(self):
        super().__init__(280, 0, 6, 0, 3, armor_classes=(28, 15, 8, 5, 19,), armor_class_values=(-2, 0, 0, 0, 0,),
                         displayed_name="Elephant Archer",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+6": Upgrade(0, 0, 0, 4, 6),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4),
                                       "+Bl.+4+6": Upgrade(20, 0, 0, 4, 6), })


class EliteElephantArcher(Unit):
    def __init__(self):
        super().__init__(330, 0, 7, 0, 3, armor_classes=(28, 15, 8, 5, 19,), armor_class_values=(-2, 0, 0, 0, 0,),
                         displayed_name="Elite Elephant Archer",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+6": Upgrade(0, 0, 0, 4, 6),
                                       "+Bl.": Upgrade(hp_upgrade=20),
                                       "+Bl.+1+1": Upgrade(hp_upgrade=20, melee_armor_upgrade=1,
                                                           pierce_armor_upgrade=1),
                                       "+Bl.+2+2": Upgrade(hp_upgrade=20, melee_armor_upgrade=2,
                                                           pierce_armor_upgrade=2),
                                       "+Bl.+3+4": Upgrade(hp_upgrade=20, melee_armor_upgrade=3,
                                                           pierce_armor_upgrade=4),
                                       "+Bl.+4+6": Upgrade(20, 0, 0, 4, 6), })


class GenoeseCrossbowman(Unit):
    def __init__(self):
        super().__init__(45, 0, 6, 1, 0, armor_classes=(15, 19,), bonus_attack_classes=(8, 5, 30, 16, 34,),
                         bonus_attack_values=(5, 5, 4, 4, 4,), displayed_name="Genoese Crossbowman",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+5 (Pavise)": Upgrade(0, 0, 0, 4, 5)})


class EliteGenoeseCrossbowman(Unit):
    def __init__(self):
        super().__init__(50, 0, 6, 1, 0, armor_classes=(15, 19,), bonus_attack_classes=(8, 5, 30, 16, 34,),
                         bonus_attack_values=(7, 7, 6, 5, 5,), displayed_name="Elite Genoese Crossbowman",
                         atk_upgrades={"+1": Upgrade(pierce_attack_upgrade=1),
                                       "+2": Upgrade(pierce_attack_upgrade=2),
                                       "+3": Upgrade(pierce_attack_upgrade=3),
                                       "+4": Upgrade(pierce_attack_upgrade=4), },
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),
                                       "+4+5 (Pavise)": Upgrade(0, 0, 0, 4, 5)})


class Samurai(Unit):
    def __init__(self):
        super().__init__(60, 8, 0, 1, 1, armor_classes=(1, 19,), bonus_attack_classes=(19, 29,),
                         bonus_attack_values=(10, 2,),
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),})


class EliteSamurai(Unit):
    def __init__(self):
        super().__init__(80, 12, 0, 1, 1, armor_classes=(1, 19,), bonus_attack_classes=(19, 29,),
                         bonus_attack_values=(12, 3,), displayed_name="Elite Samurai",
                         atk_upgrades={"+1": Upgrade(melee_attack_upgrade=1),
                                       "+2": Upgrade(melee_attack_upgrade=2),
                                       "+4": Upgrade(melee_attack_upgrade=4)},
                         def_upgrades={"+1+1": Upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1),
                                       "+2+2": Upgrade(melee_armor_upgrade=2, pierce_armor_upgrade=2),
                                       "+3+4": Upgrade(melee_armor_upgrade=3, pierce_armor_upgrade=4),})
