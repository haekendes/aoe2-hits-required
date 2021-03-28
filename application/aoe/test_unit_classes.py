import os
import traceback
from application.aoe.armor_classes import get_armor_class_name
from application.aoe.units import Unit

try:
    for cls in Unit.__subclasses__():

        obj = cls()
        print(f"{obj.__class__.__name__}, HP: {obj.HP}, Attack:{obj.MELEE_ATTACK}m,{obj.PIERCE_ATTACK}p, Armor:{obj.MELEE_ARMOR}m,{obj.PIERCE_ARMOR}p")

        print(f"{'':<4}Armor classes:\n{'':<8}", end='')
        print(*[f'{get_armor_class_name(key)}: {value}' for key, value in obj.ARMOR_CLASSES.items()], sep=", ")

        print(f"{'':<4}Attack bonuses:\n{'':<8}", end='')
        print(*[f'{get_armor_class_name(key)}: {value}' for key, value in obj.BONUS_ATTACK.items()], sep=", ")

    print("\nAll unit classes working.")
except:
    os.system('cls')  # on Windows System
    print("Unit test failed.\n")
    traceback.print_exc()