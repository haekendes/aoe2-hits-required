from flask import Flask
from flask_bootstrap import Bootstrap

from application.aoe.units import Unit, Villager, Upgrade
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


def set_generic_upgrades(unit):
    if any(x in unit.armor_classes.keys() for x in (1, 8, 15, 30,)):
        unit.def_upgrades["+1+1"] = Upgrade(0, 0, 0, 1, 1)
        unit.def_upgrades["+2+2"] = Upgrade(0, 0, 0, 2, 2)
        unit.def_upgrades["+3+4"] = Upgrade(0, 0, 0, 3, 4)

    if any(x in unit.armor_classes.keys() for x in (15, 16,)):
        unit.atk_upgrades["+1"] = Upgrade(0, 0, 1, 0, 0)
        unit.atk_upgrades["+2"] = Upgrade(0, 0, 2, 0, 0)
        unit.atk_upgrades["+3"] = Upgrade(0, 0, 3, 0, 0)
        unit.atk_upgrades["+4"] = Upgrade(0, 0, 4, 0, 0)

    if any(x in unit.armor_classes.keys() for x in (1, 8, 30,)):
        unit.atk_upgrades["+1"] = Upgrade(0, 1, 0, 0, 0)
        unit.atk_upgrades["+2"] = Upgrade(0, 2, 0, 0, 0)
        unit.atk_upgrades["+4"] = Upgrade(0, 4, 0, 0, 0)


def zumbla(unit_catcher):
    column_list = []
    for unit_pitcher in unit_pitchers:
        inner_dict = {}
        # columns
        inner_dict[unit_pitcher.get_name()] = unit_catcher - unit_pitcher  # dict[column_name] = column_values
        for key, value in unit_pitcher.atk_upgrades.items():
            inner_dict[unit_pitcher.get_name() + key] = unit_catcher - unit_pitcher.upgrade(value)
            unit_pitcher.set_atk_upgrades_to_zero()

        column_list.append(inner_dict)
    return column_list


unit_catchers = [cls() for cls in Unit.__subclasses__()]
unit_pitchers = unit_catchers.copy()

table_data = []
for unit_catcher in unit_catchers:
    rows_dict = {}

    rows_dict[unit_catcher.get_name()] = zumbla(unit_catcher)
    for key, value in unit_catcher.def_upgrades.items():
        rows_dict[unit_catcher.get_name() + key] = zumbla(unit_catcher.upgrade(value))
        unit_catcher.set_def_upgrades_to_zero()

    super_dict = {unit_catcher.get_name(): rows_dict}
    table_data.append(super_dict)

column_names = [key for key in next(iter(next(iter(table_data[0].values())).values()))]

from application import routes
