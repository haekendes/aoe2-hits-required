from application.aoe.units import Unit


unit_catchers = [cls() for cls in Unit.__subclasses__()]
unit_pitchers = unit_catchers.copy()

column_names = [unit.__class__.__name__ for unit in unit_catchers]

table_data = []
for unit_catcher in unit_catchers:
    for unit_pitcher in unit_pitchers:
        dict = {unit_pitcher.__class__.__name__: unit_catcher - unit_pitcher}
        dict["empty"] = unit_catcher.__class__.__name__ # row names
        table_data.append(dict)

print(table_data)