"""Validación y conversión segura de entradas de interfaz."""
from decimal import Decimal, InvalidOperation


def parse_decimal(raw: str, label: str, max_decimals: int = 2) -> Decimal:
    normalized = raw.strip().replace(',', '.')
    if not normalized:
        raise ValueError(f'{label}: el campo es obligatorio.')
    if normalized.count('.') > 1:
        raise ValueError(f'{label}: ingrese un número válido.')
    try: value = Decimal(normalized)
    except InvalidOperation as error: raise ValueError(f'{label}: ingrese un número válido.') from error
    if not value.is_finite() or value <= 0:
        raise ValueError(f'{label}: ingrese un valor mayor que cero.')
    decimals = -value.as_tuple().exponent if value.as_tuple().exponent < 0 else 0
    if decimals > max_decimals:
        raise ValueError(f'{label}: se permiten como máximo {max_decimals} decimales.')
    return value


def validate_age(raw: str) -> int:
    try: age = int(raw.strip())
    except ValueError as error: raise ValueError('Edad: ingrese un número entero.') from error
    if not 1 <= age <= 150: raise ValueError('Edad: ingrese un valor entre 1 y 150.')
    return age


def validate_weight(raw: str) -> Decimal:
    value = parse_decimal(raw, 'Peso')
    if value > Decimal('500'): raise ValueError('Peso: el valor ingresado parece no ser válido.')
    return value


def validate_height(raw: str) -> Decimal:
    value = parse_decimal(raw, 'Estatura')
    if not Decimal('0.5') <= value <= Decimal('3'): raise ValueError('Estatura: ingrese un valor entre 0,5 y 3 m.')
    return value
