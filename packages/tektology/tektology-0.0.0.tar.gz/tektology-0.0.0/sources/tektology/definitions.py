# general definitions


# dimensional units
conversion_table = {"inches to meters": 100/2.54}

def unit_conversion(value, from_unit, to_unit):
    get_ratio = value / conversion_table.get(f"{from_unit} to {to_unit}")
    return get_ratio

print(unit_conversion(1, "inches", "meters"))