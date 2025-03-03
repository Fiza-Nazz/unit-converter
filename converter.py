def convert_units(category, value, from_unit, to_unit):
    conversions = {
        "Length": {"km": 1000, "m": 1, "cm": 0.01, "mm": 0.001},
        "Weight": {"kg": 1000, "g": 1, "mg": 0.001},
        "Temperature": {
            "C": lambda x: x,
            "F": lambda x: (x * 9/5) + 32,
            "C_to_F": lambda x: (x * 9/5) + 32,
            "F_to_C": lambda x: (x - 32) * 5/9
        }
    }
    
    if category in conversions and from_unit in conversions[category] and to_unit in conversions[category]:
        if category == "Temperature":
            if from_unit == "C" and to_unit == "F":
                return conversions["Temperature"]["C_to_F"](value)
            elif from_unit == "F" and to_unit == "C":
                return conversions["Temperature"]["F_to_C"](value)
            else:
                return "Invalid Temperature Conversion"
        return value * (conversions[category][from_unit] / conversions[category][to_unit])
    
    return "Invalid Conversion"
