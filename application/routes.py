from flask import render_template

from application.aoe.armor_classes import get_armor_class_name
from application.aoe.units import Unit
from application.app import app, table_data, column_names


@app.get('/')
def home():
    return render_template('home.html')


@app.get('/get_table')
def get_table():
    return {"table": table_data, "columns": column_names}


@app.get('/get_units')
def get_units():
    dict = {}
    for cls in Unit.__subclasses__():
        obj = cls()
        dict[obj.__class__.__name__] = {"hp": obj.hp,
                                        "attack": {"melee": obj.melee_attack, "pierce": obj.pierce_attack}, "armor": {
                "melee": obj.melee_armor, "pierce": obj.pierce_armor},
                                        "armor classes": [{f"{get_armor_class_name(key)}": value} for key, value in
                                                          obj.armor_classes.items()
                                                          ],
                                        "attack bonuses": [{f"{get_armor_class_name(key)}": value} for key, value in
                                                           obj.bonus_attack.items()
                                                           ],
                                        "Upgrades_atk": f"{obj.atk_upgrades}",
                                        "Upgrades_def": f"{obj.def_upgrades}"
                                        }
    return {'units': dict}
