import math
import builtins
import re 

from functions import fraction_decoder
from constants import UNITS, SPECIAL_UNITS, PREFIXES

## Relevant constants ##
pi = math.pi

## Relevant functions ##
def sqrt(value, n=1): copy = value.copy(); copy.sqrt(n); return copy
def nsqrt(value, n): copy = value.copy(); copy.sqrt(n); return copy
def round(value, digits): copy = value.copy(); copy.round(digits); return copy

## Value Class ##
class v():
    def __init__(self, value):
        value = value.replace("^", "**")
        self.nominators, self.denominators = fraction_decoder(value)
        self._get_value(value)

    def copy(self): return v(self.__str__())
    def round(self, digits): self.value = builtins.round(self.value, digits)
    def sqrt(self, n=1): return self.__pow__(1/n)
    def __str__(self): return str(self.value) + " " + self.unit.get()
    def __eq__(self, other): return str(self) == other
    def __add__(self, other): return v(str(self.value + other.value) + " " + self.unit.get_add(other))
    def __sub__(self, other): return v(str(self.value - other.value) + " " + self.unit.get_sub(other))
    def __rtruediv__(self, other): return self.__truediv__(other)
    def __rmul__(self, other): return self.__mul__(other)
    def __pow__(self, other): return v(str(self.value ** other) + " " + self.unit ** other)

    def __mul__(self, other): 
        if isinstance(other, (int, float)): return v(str(self.value * other) + " " + self.unit.get())
        value = self.value * other.value
        unit = self.unit * other.unit
        return v(str(value) + " " + unit.get())

    def __truediv__(self, other): 
        if isinstance(other, (int, float)): return v(str(self.value / other) + " " + self.unit.get())
        value = self.value / other.value
        unit = self.unit / other.unit
        return v(str(value) + " " + unit.get())

    def _get_value(self, value): 
        if len(self.nominators) and not self.denominators: self._get_single_value(value)
        else: self._get_value_fraction(value)
    
    def _get_value_fraction(self, value):
        self.value = 1
        nom_unit = Unit("")
        for nominator in self.nominators:
            if len(nominator.split()) == 1: 
                nom_unit = self.handle_len_1_value(nominator, "mul", unit_obj = nom_unit)
            else: 
                value_obj = v(nominator)
                self.value *= value_obj.value
                nom_unit *= value_obj.unit

        denom_unit = Unit("")
        if self.denominators:
            for denominator in self.denominators:
                if len(denominator.split()) == 1: 
                    denom_unit = self.handle_len_1_value(denominator, "div", unit_obj = denom_unit)
                else: 
                    value_obj = v(denominator)
                    self.value /= value_obj.value
                    denom_unit *= value_obj.unit
        self.unit = nom_unit / denom_unit

    def handle_len_1_value(self, value, method, unit_obj):
        if self.is_hidden_float(value): 
            if method == "mul": self.value *= value
            else: self.value /= value
        else: 
            if value not in UNITS:
                value_obj = v(f"1 {value}")
                unit_obj *= value_obj.unit
                if method == "mul": self.value *= value_obj.value
                else: self.value /= value_obj.value
            else:
                unit_obj *= Unit(value)
        return unit_obj

    def is_hidden_float(self, value):
        try: float(value); return True
        except: return False

    def _get_single_value(self, value):
        split = value.split()
        if len(split) not in [1, 2]: raise Exception(f"The input should be 1 number and 1 unit: '5 m', '18.23 m/s', etc.\nYou gave this input: {value}")
        if len(split) == 1: self.value, self.unit = float(split[0]), Unit("")
        else: self.value, self.unit = float(split[0]), Unit(split[1])
        self.value *= self.unit.prefix

    def to(self, desired_unit):
        desired_unit_obj = v(f"1 {desired_unit}")
        if self.unit.get(with_power=False) != desired_unit_obj.unit.get(with_power=False): 
            raise Exception(f"{self.unit.get(with_power=False)} does not match with desired unit: {desired_unit} with the SI-unit: {desired_unit_obj.unit.get(with_power=False)}")
        return f"{(self.value / desired_unit_obj.value)} {desired_unit}"

## Unit Class ##
class Unit():
    def __init__(self, unit) -> None:
        self.set_unit_and_power(unit)
        self.simplify()

    def _check_compatibility(self, other): 
        if self.unit != other.unit.get(with_power=False): raise Exception(f"Units are not compatible: {self.unit} : {other.unit.get(with_power=False)}")

    def _check_if_unit_class(self, other):
        if not isinstance(other, Unit): raise Exception(f"Other must be Unit, but is {type(other)}")

    def _non_empty_denominators(self): return self.denominators != [''] and self.denominators != []

    def __mul__(self, other): 
        self._check_if_unit_class(other)
        this_nom, this_denom = self.get_fraction_with_powers(self)
        other_nom, other_denom = self.get_fraction_with_powers(other)
        nominators = "*".join([v for v in [this_nom, other_nom] if v != ""])
        denominators = "*".join([v for v in [this_denom, other_denom] if v != ""])
        fraction = nominators
        if denominators != [""]: fraction += "/"; fraction += denominators
        return Unit(fraction)

    def __truediv__(self, other): 
        self._check_if_unit_class(other)
        this_nom, this_denom = self.get_fraction_with_powers(self)
        other_nom, other_denom = self.get_fraction_with_powers(other)
        nominators = "*".join([v for v in [this_nom, other_denom] if v != ""])
        denominators = "*".join([v for v in [this_denom, other_nom] if v != ""])
        fraction = nominators
        if denominators != [""]: fraction += "/"; fraction += denominators
        return Unit(fraction)

    def __pow__(self, other): return self.add_power(other)
    def get(self, with_power = True): return self.add_power() if with_power else self.unit 
    def get_add(self, other): self._check_compatibility(other); return self.add_power()
    def get_sub(self, other): self._check_compatibility(other); return self.add_power()

    def get_fraction_with_powers(self, unit_instance): 
        if "/" not in unit_instance.add_power(): return (unit_instance.add_power(), "")
        return unit_instance.add_power().split("/"); 

    def add_power(self, power=1): 
        nominator_powers = [nom_power * power for nom_power in self.nominators_powers]
        denominator_powers = [denom_power * power for denom_power in self.denominators_powers]
        return self.construct_unit_with_powers(nominator_powers, denominator_powers)

    def set_unit_and_power(self, unit):
        self.set_unit(unit)
        self.set_powers()
        self.prefix = self.get_total_prefix()
        self.unit = self.construct_unit()

    def set_unit(self, unit):
        if len(unit.split("/")) not in [1, 2]: raise ValueError("Input must have exactly one '/' character to separate numerator and denominator.")
        if "/" not in unit: self.nominators, self.denominators = [unit, ""]
        else: self.nominators, self.denominators = unit.split("/")
        pattern = r'(?<=[A-Za-z0-9])\*(?=[A-Za-z0-9])'
        self.nominators = re.split(pattern, self.nominators)
        self.denominators = re.split(pattern, self.denominators)
    
    def construct_unit(self):
        unit_construction = "*".join(self.nominators)
        if self._non_empty_denominators(): unit_construction += "/"; unit_construction += "*".join(self.denominators)
        return unit_construction

    def construct_unit_with_powers(self, nom_powers, denom_powers):
        nominators = [f"{unit}**{str(power)}" if power != 1 else unit for (unit, power) in zip(self.nominators, nom_powers)]
        denominators = [f"{unit}**{str(power)}" if power != 1 else unit for (unit, power) in zip(self.denominators, denom_powers)]
        unit_construction = "*".join(nominators)
        if self._non_empty_denominators(): unit_construction += "/"; unit_construction += "*".join(denominators)
        return unit_construction

    def set_powers(self):
        self.nominators_powers = [self.set_power(unit)[1] for unit in self.nominators]
        self.nominators = [self.set_power(unit)[0] for unit in self.nominators]
        self.denominators_powers = [self.set_power(unit)[1] for unit in self.denominators]
        self.denominators = [self.set_power(unit)[0] for unit in self.denominators]

    def set_power(self, unit):
        if "**" in unit: unit, power = unit.split("**")
        else: power = 1
        return (unit, float(power))
    
    def get_total_prefix(self):
        nominator_prefixes = [self.get_prefix(unit, power) for unit, power in zip(self.nominators, self.nominators_powers)]
        nominator_prefix = math.prod([prefix for (prefix, unit) in nominator_prefixes])
        self.nominators = [unit for (prefix, unit) in nominator_prefixes]
        denominator_prefixes = [self.get_prefix(unit, power) for unit, power in zip(self.denominators, self.denominators_powers)]
        denominator_prefix = math.prod([prefix for (prefix, unit) in denominator_prefixes])
        self.denominators = [unit for (prefix, unit) in denominator_prefixes]
        return nominator_prefix / denominator_prefix

    def get_prefix(self, unit, power):
        if unit[1:] in UNITS: prefix = PREFIXES[unit[0]]; unit = unit[1:]
        elif unit in SPECIAL_UNITS: prefix, unit = SPECIAL_UNITS[unit]
        else: prefix = 1
        prefix **= power
        return prefix, unit

    def simplify(self):
        nominator_dict, denominator_dict = self.get_simplify_dicts()
        simplified_nominator_dict = self.subtract_dicts(nominator_dict, denominator_dict)
        simplified_denominator_dict = self.subtract_dicts(denominator_dict, nominator_dict)
        self.set_fraction_values(simplified_nominator_dict, simplified_denominator_dict)

    def get_simplify_dicts(self): 
        return (self.get_simplify_dict(self.nominators, self.nominators_powers), self.get_simplify_dict(self.denominators, self.denominators_powers))

    def get_simplify_dict(self, units, powers): 
        simplify_dict = {}
        for unit, power in zip(units, powers):
            if unit not in simplify_dict: simplify_dict[unit] = power
            else: simplify_dict[unit] += power
        return simplify_dict

    def subtract_dicts(self, dict1, dict2):
        updated_dict = {}
        for key in dict1.keys():
            if key in dict2: updated_dict[key] = dict1[key] - dict2[key]
            else: updated_dict[key] = dict1[key]
        return {key: value for (key, value) in updated_dict.items() if value > 0}

    def set_fraction_values(self, nominator_dict, denominator_dict):
        self.nominators = list(nominator_dict.keys())
        self.nominators_powers = list(nominator_dict.values())
        self.denominators = list(denominator_dict.keys())
        self.denominators_powers = list(denominator_dict.values())