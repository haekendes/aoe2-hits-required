import math


class Unit(object):
    def __init__(self, hp, melee_attack, pierce_attack, melee_armor, pierce_armor, armor_classes,
                 armor_class_values=None, bonus_attack_classes=None, bonus_attack_values=None):
        self.HP = hp
        self.MELEE_ATTACK = melee_attack
        self.PIERCE_ATTACK = pierce_attack
        self.MELEE_ARMOR = melee_armor
        self.PIERCE_ARMOR = pierce_armor
        self.ARMOR_CLASSES = zip_class_values(armor_classes, armor_class_values) if armor_classes else {0: 0}
        self.BONUS_ATTACK = zip_class_values(bonus_attack_classes, bonus_attack_values) if bonus_attack_values else {
            0: 0}

        self.HP_UPGRADE = 0
        self.MELEE_ATTACK_UPGRADE = 0
        self.PIERCE_ATTACK_UPGRADE = 0
        self.MELEE_ARMOR_UPGRADE = 0
        self.PIERCE_ARMOR_UPGRADE = 0

    def upgrade(self, hp_upgrade=0, melee_attack_upgrade=0, pierce_attack_upgrade=0, melee_armor_upgrade=0,
                pierce_armor_upgrade=0):
        self.HP_UPGRADE += hp_upgrade
        self.MELEE_ATTACK_UPGRADE += melee_attack_upgrade
        self.PIERCE_ATTACK_UPGRADE += pierce_attack_upgrade
        self.MELEE_ARMOR_UPGRADE += melee_armor_upgrade
        self.PIERCE_ARMOR_UPGRADE += pierce_armor_upgrade
        return self

    def __sub__(self, unit):
        result = int(math.ceil((self.HP + self.HP_UPGRADE)
                               / max(1, (max(0, unit.MELEE_ATTACK + unit.MELEE_ATTACK_UPGRADE - (
                    self.MELEE_ARMOR + self.MELEE_ARMOR_UPGRADE))
                                         + max(0, unit.PIERCE_ATTACK + unit.PIERCE_ATTACK_UPGRADE - (
                            self.PIERCE_ARMOR + self.PIERCE_ARMOR_UPGRADE))
                                         + sum(max(0, value - self.ARMOR_CLASSES[key])
                                               if key in self.ARMOR_CLASSES else 0
                                               for key, value in unit.BONUS_ATTACK.items())
                                         ))))
        # if unit.MELEE_ATTACK > 0:
        # print(f"{self.__class__.__name__} +{self.MELEE_ARMOR_UPGRADE}+{self.PIERCE_ARMOR_UPGRADE} requires {result} hits from {unit.__class__.__name__} +{unit.MELEE_ATTACK_UPGRADE}")
        # else:
        # print(f"{self.__class__.__name__}+{self.MELEE_ARMOR_UPGRADE}+{self.PIERCE_ARMOR_UPGRADE} requires {result} hits from {unit.__class__.__name__}+{unit.PIERCE_ATTACK_UPGRADE}")
        return result

    def get_name(self):
        return self.__class__.__name__


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


class MenAtArms(Unit):
    def __init__(self):
        super().__init__(45, 6, 0, 0, 1, armor_classes=(1,), bonus_attack_classes=(29,), bonus_attack_values=(2,))


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
        super().__init__(25, 3, 0, 0, 0, armor_classes=None)


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
        super().__init__(40, 0, 4, 0, 0, armor_classes=(1, 19,), bonus_attack_classes=(1, 32, 17, 27,),
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
