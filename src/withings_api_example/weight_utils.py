def unit_conversion(unit, value):
    stringified_value = str(value)
    return float(f"{stringified_value[:unit]}.{stringified_value[unit:]}")

def kg_to_ibs(value):
    return value * 2.20462
