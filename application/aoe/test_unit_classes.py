import os
import traceback
from application.aoe.armor_classes import get_armor_class_name
from application.aoe.units import Unit

try:
    for cls in Unit.__subclasses__():

        obj = cls()
        print(f"{obj.__class__.__name__}, HP: {obj.hp}, Attack:{obj.melee_attack}m,{obj.pierce_attack}p, Armor:{obj.melee_armor}m,{obj.pierce_armor}p")

        print(f"{'':<4}Armor classes:\n{'':<8}", end='')
        print(*[f'{get_armor_class_name(key)}: {value}' for key, value in obj.armor_classes.items()], sep=", ")

        print(f"{'':<4}Attack bonuses:\n{'':<8}", end='')
        print(*[f'{get_armor_class_name(key)}: {value}' for key, value in obj.bonus_attack.items()], sep=", ")

        print(f"{'':<4}Upgrades:\n{'':<8}", end='')
        print(f"atk: {obj.atk_upgrades}\n{'':<8}", end='')
        print(f"def: {obj.def_upgrades}")

    print("\nAll unit classes working.")
except:
    os.system('cls')  # on Windows System
    print("Unit test failed.\n")
    traceback.print_exc()