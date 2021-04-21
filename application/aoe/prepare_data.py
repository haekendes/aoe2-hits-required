from application.aoe.units import Unit

unit_catchers = [cls() for cls in Unit.__subclasses__()]
unit_pitchers = unit_catchers.copy()


def get_column_names():
    column_names = []
    for unit in unit_catchers:
        column_names.append(unit.get_name())
        for key in unit.atk_upgrades.keys():
            column_names.append(unit.get_name() + key)
    return column_names


def get_table_data():
    table_data = []
    for unit_catcher in unit_catchers:
        rows_list = [{unit_catcher.get_name(): fill_columns(unit_catcher)}]
        for key, value in unit_catcher.def_upgrades.items():
            rows_list.append({key: fill_columns(unit_catcher.upgrade(value))})
            unit_catcher.set_def_upgrades_to_zero()

        super_dict = {unit_catcher.get_name(): rows_list}
        table_data.append(super_dict)
    return table_data


def fill_columns(unit_catcher):
    column_list = []
    for unit_pitcher in unit_pitchers:
        inner_column_list = [unit_catcher - unit_pitcher]
        # columns
        for key, value in unit_pitcher.atk_upgrades.items():
            inner_column_list.append(unit_catcher - unit_pitcher.upgrade(value))
            unit_pitcher.set_atk_upgrades_to_zero()

        column_list.append(inner_column_list)
    return column_list