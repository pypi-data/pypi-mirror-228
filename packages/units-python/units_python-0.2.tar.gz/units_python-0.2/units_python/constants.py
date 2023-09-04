
UNITS = {
    "m": "meter", "s": "second", "g": "gram", "l": "liter", "A": "ampere", "K": "kelvin", "mol": "mole", "cd": "candela"
}

SPECIAL_UNITS = {
    "ton": [10**6, "g"], "tons": [10**6, "g"], 
    "min": [60, "s"], 
    "hours": [60*60, "s"], "hour": [60*60, "s"], "h": [60*60, "s"]
}

PREFIXES = {
    "d": 10**-1, "c": 10**-2, "m": 10**-3, "µ": 10**-6, "n": 10**-9, "p": 10**-12, "f": 10**-15,
    "da": 10**1, "h": 10**2, "k": 10**3, "M": 10**6, "G": 10**9, "T": 10**12, "P": 10**15
}

PREFIXES_SINGLE_LETTER = {
    "d": "deci", "c": "centi", "m": "milli", "µ": "micro", "n": "nano", "p": "pico", "f": "femto",
    "da": "deca", "h": "hecto", "k": "kilo", "M": "mega", "G": "giga", "T": "tera", "P": "peta"
}
PREFIXES_SINGLE_LETTER_REVERSE = {value: key for key, value in PREFIXES_SINGLE_LETTER.items()}