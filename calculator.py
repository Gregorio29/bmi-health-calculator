"""Cálculos antropométricos informativos con Decimal."""
from decimal import Decimal, ROUND_HALF_UP

TWO = Decimal('0.01')
KG_PER_LB = Decimal('0.45359237')
M_PER_INCH = Decimal('0.0254')
ACTIVITY_FACTORS = {
    'Sedentaria': Decimal('1.2'),
    'Ligera': Decimal('1.375'),
    'Moderada': Decimal('1.55'),
    'Alta': Decimal('1.725'),
    'Muy alta': Decimal('1.9'),
}


def rounded(value: Decimal, quantum: Decimal = TWO) -> Decimal:
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def bmi(weight_kg: Decimal, height_m: Decimal) -> Decimal:
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError('El peso y la estatura deben ser mayores que cero.')
    return rounded(weight_kg / (height_m * height_m))


def bmi_category(value: Decimal) -> str:
    if value < Decimal('18.5'):
        return 'Bajo peso'
    if value < Decimal('25'):
        return 'Rango de referencia'
    if value < Decimal('30'):
        return 'Sobrepeso'
    return 'Obesidad'


def reference_weight_range(height_m: Decimal) -> tuple[Decimal, Decimal]:
    if height_m <= 0:
        raise ValueError('La estatura debe ser mayor que cero.')
    square = height_m * height_m
    return rounded(Decimal('18.5') * square), rounded(Decimal('24.999') * square)


def kg_to_lb(kg: Decimal) -> Decimal:
    if kg <= 0: raise ValueError('El peso debe ser mayor que cero.')
    return rounded(kg / KG_PER_LB)


def lb_to_kg(lb: Decimal) -> Decimal:
    if lb <= 0: raise ValueError('El peso debe ser mayor que cero.')
    return rounded(lb * KG_PER_LB)


def height_to_meters(value: Decimal, unit: str) -> Decimal:
    if value <= 0: raise ValueError('La estatura debe ser mayor que cero.')
    if unit == 'm': return value
    if unit == 'cm': return value / Decimal('100')
    raise ValueError('Unidad de estatura no compatible.')


def feet_inches_to_meters(feet: int, inches: Decimal) -> Decimal:
    if feet < 0 or inches < 0 or inches >= 12 or (feet == 0 and inches == 0):
        raise ValueError('Ingrese pies y pulgadas válidos (pulgadas: 0 a <12).')
    return rounded((Decimal(feet) * Decimal('12') + inches) * M_PER_INCH)


def weight_change(previous: Decimal, current: Decimal) -> tuple[Decimal, Decimal, str]:
    if previous <= 0 or current <= 0:
        raise ValueError('Ambos pesos deben ser mayores que cero.')
    absolute = rounded(current - previous)
    percent = rounded((absolute / previous) * Decimal('100'))
    label = 'aumentó' if absolute > 0 else 'disminuyó' if absolute < 0 else 'permaneció igual'
    return absolute, percent, label


def mifflin_st_jeor(weight_kg: Decimal, height_cm: Decimal, age: int, sex: str) -> Decimal:
    if sex not in ('Masculino', 'Femenino'):
        raise ValueError('La TMB requiere seleccionar Masculino o Femenino.')
    base = Decimal('10') * weight_kg + Decimal('6.25') * height_cm - Decimal('5') * Decimal(age)
    return (base + (Decimal('5') if sex == 'Masculino' else Decimal('-161'))).quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def tdee(bmr_kcal: Decimal, activity: str) -> Decimal:
    try: factor = ACTIVITY_FACTORS[activity]
    except KeyError as error: raise ValueError('Seleccione un nivel de actividad válido.') from error
    return (bmr_kcal * factor).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
