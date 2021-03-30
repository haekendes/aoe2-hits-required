from flask import Flask
from flask_bootstrap import Bootstrap

from application.aoe.units import Unit, Villager
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


def zumbla(unit_catcher):
    unit_pitchers = [cls() for cls in Unit.__subclasses__()]
    column_list = []
    for unit_pitcher in unit_pitchers:
        inner_dict = {}
        # columns
        if not 25 in unit_pitcher.ARMOR_CLASSES:
            inner_dict[unit_pitcher.get_name()] = unit_catcher - unit_pitcher  # dict[column_name] = column_values

            # attack upgrades
            if not any(x in unit_pitcher.ARMOR_CLASSES for x in [17, 34]):  # no rams, monks or fishing ships
                inner_dict[unit_pitcher.get_name() + "+1"] = unit_catcher - unit_pitcher.upgrade(melee_attack_upgrade=1) \
                    if unit_pitcher.MELEE_ATTACK > 0 else unit_catcher - unit_pitcher.upgrade(pierce_attack_upgrade=1)

                if not any(x in unit_pitcher.ARMOR_CLASSES for x in [20, ]):  # no siege weapons
                    inner_dict[unit_pitcher.get_name() + "+2"] = unit_catcher - unit_pitcher.upgrade(melee_attack_upgrade=1) \
                        if unit_pitcher.MELEE_ATTACK > 0 else unit_catcher - unit_pitcher.upgrade(pierce_attack_upgrade=1)

                    if unit_pitcher.PIERCE_ATTACK > 0:
                        inner_dict[unit_pitcher.get_name() + "+3"] = unit_catcher - unit_pitcher.upgrade(pierce_attack_upgrade=1)

                    inner_dict[unit_pitcher.get_name() + "+4"] = unit_catcher - unit_pitcher.upgrade(melee_attack_upgrade=2) \
                        if unit_pitcher.MELEE_ATTACK > 0 else unit_catcher - unit_pitcher.upgrade(pierce_attack_upgrade=1)
            column_list.append(inner_dict)
    return column_list


unit_catchers = [cls() for cls in Unit.__subclasses__()]

table_data = []
for unit_catcher in unit_catchers:
    rows_dict = {}

    if isinstance(unit_catcher, Villager):
        rows_dict[unit_catcher.get_name()] = zumbla(unit_catcher)
        rows_dict[unit_catcher.get_name() + " +Loom"] = zumbla(
            unit_catcher.upgrade(hp_upgrade=15, melee_armor_upgrade=1, pierce_armor_upgrade=2))
    else:
        rows_dict[unit_catcher.get_name()] = zumbla(unit_catcher)

    if not any(x in unit_catcher.ARMOR_CLASSES for x in [17, 25, 34]):  # no rams, monks, siege oder fishing ships
        rows_dict[unit_catcher.get_name() + "+1+1"] = zumbla(
            unit_catcher.upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1))
        rows_dict[unit_catcher.get_name() + "+2+2"] = zumbla(
            unit_catcher.upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=1))
        rows_dict[unit_catcher.get_name() + "+3+4"] = zumbla(
            unit_catcher.upgrade(melee_armor_upgrade=1, pierce_armor_upgrade=2))


    super_dict = {unit_catcher.get_name(): rows_dict}
    table_data.append(super_dict)

column_names = [key for key in next(iter(next(iter(table_data[0].values())).values()))]

from application import routes
