from flask import Flask
from flask_bootstrap import Bootstrap

from application.aoe.units import Unit, Villager, Upgrade
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


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

column_names = []
for unit in unit_catchers:
    column_names.append(unit.get_name())
    for key in unit.atk_upgrades.keys():
        column_names.append(unit.get_name() + key)

table_data = []
for unit_catcher in unit_catchers:
    rows_dict = {}

    rows_dict[unit_catcher.get_name()] = zumbla(unit_catcher)
    for key, value in unit_catcher.def_upgrades.items():
        rows_dict[unit_catcher.get_name() + key] = zumbla(unit_catcher.upgrade(value))
        unit_catcher.set_def_upgrades_to_zero()

    super_dict = {unit_catcher.get_name(): rows_dict}
    table_data.append(super_dict)

from application import routes
