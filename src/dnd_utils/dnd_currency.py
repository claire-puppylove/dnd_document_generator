import pint
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN

DND_CURRENCY_REGISTRY = pint.UnitRegistry(None)
DND_CURRENCY_REGISTRY.define("copper_piece = 1 = CP = cp")
DND_CURRENCY_REGISTRY.define("silver_piece = 10 * copper_piece = SP = sp")
DND_CURRENCY_REGISTRY.define("electrum_piece = 5 * silver_piece = EP = ep")
DND_CURRENCY_REGISTRY.define("gold_piece = 10 * silver_piece = GP = gp")
DND_CURRENCY_REGISTRY.define("platinum_piece = 10 * gold_piece = PP = pp")

# homebrew aliases
DND_CURRENCY_REGISTRY.define("@alias copper_piece = consumed_soul_piece = creepy_point")
DND_CURRENCY_REGISTRY.define("@alias silver_piece = soul_piece = spooky_point")
DND_CURRENCY_REGISTRY.define("@alias electrum_piece = essence_piece = eerie_point")
DND_CURRENCY_REGISTRY.define("@alias gold_piece = greater_soul_piece = ghost_point")
DND_CURRENCY_REGISTRY.define("@alias platinum_piece = powerful_soul_piece = phantom_point")

# hombrew piece
DND_CURRENCY_REGISTRY.define("life_piece = 10 * powerful_soul_piece = lunar_point = LP = lp")

# Use symbol for string
DND_CURRENCY_REGISTRY.formatter.default_format = "~"

def round(number, ndigits=None):
    """Always round off"""
    exp = Decimal('1.{}'.format(ndigits * '0')) if ndigits else Decimal('1')
    return type(number)(Decimal(number).quantize(exp, ROUND_HALF_DOWN))


def currency_string_to_value(currency_string):
    if "+" in currency_string:
        prefix, cur = currency_string.split("+")
    else:
        prefix = ""
        cur = currency_string
    return prefix, DND_CURRENCY_REGISTRY(cur)

def cost_to_crafting_value(currency_string):
    try:
        prefix, ureg_quantity = currency_string_to_value(currency_string)
        crafting_value = ureg_quantity/2
        if prefix !="":
            prefix = prefix.strip()
            prefix+="/2 + "
    except pint.errors.UndefinedUnitError as e:
        if currency_string == "Priceless":
            prefix = ''
            crafting_value = "Priceless"
        else:
            prefix = ''
            crafting_value = f"Half of {currency_string}"
    return prefix, crafting_value

def currency_value_to_string(prefix, currency_value):
    if isinstance(currency_value, pint.Quantity):
        if currency_value < DND_CURRENCY_REGISTRY("1 SP"):
            currency_value = currency_value.to("CP")
            cv_m = currency_value.magnitude
            cv_m = round(cv_m)
            cv_m_s = f"{cv_m:.0f}"
            cv_u = str(currency_value.units)
            currency_value_str = f"{prefix}{cv_m_s} {cv_u}"
        if currency_value >= DND_CURRENCY_REGISTRY("1 SP") and currency_value < DND_CURRENCY_REGISTRY("1 GP"):
            currency_value = currency_value.to("SP")
            cv_m = currency_value.magnitude
            cv_m_s = f"{cv_m:.1f}".rstrip("0").rstrip(".")
            cv_u = str(currency_value.units)
            currency_value_str = f"{prefix}{cv_m_s} {cv_u}"
        if currency_value >= DND_CURRENCY_REGISTRY("1 GP"):
            currency_value = currency_value.to("GP")
            cv_m = currency_value.magnitude
            cv_m_s = f"{cv_m:,.2f}".rstrip("0").rstrip(".")
            cv_u = str(currency_value.units)
            currency_value_str = f"{prefix}{cv_m_s} {cv_u}"
    else:
        currency_value_str = f"{prefix}{currency_value}"
    return currency_value_str