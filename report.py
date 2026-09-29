"""Exportación local de informes de texto UTF-8."""
from datetime import datetime
from pathlib import Path

PROJECT = 'PROYECTO — CALCULADORA DE IMC Y PESO DE REFERENCIA'
CODE = 'PROY-IMC-001'
WARNING = ('Esta herramienta proporciona estimaciones y no constituye diagnóstico ni '
           'asesoramiento médico. El IMC es una medida de cribado y debe interpretarse '
           'junto con otros factores individuales. Para una evaluación personalizada, '
           'consulte a un profesional de la salud.')


def build_report(data: dict) -> str:
    lines = [PROJECT, f'Código: {CODE}', f'Fecha: {datetime.now():%Y-%m-%d %H:%M}', '', 'Resultados']
    lines += [f'- {key}: {value}' for key, value in data.items()]
    lines += ['', 'Fórmulas', '- IMC = peso (kg) / estatura² (m).', '- Peso de referencia = IMC × estatura².',
              '- Cambio porcentual = ((actual - anterior) / anterior) × 100.',
              '', 'Advertencia', WARNING, '', 'Limitaciones',
              'Resultados orientativos para adultos; no aplica categorías adultas a menores de 20 años.',
              '', 'Fuentes',
              '- CDC, Adult BMI Categories: https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html',
              '- Mifflin et al. (1990), PMID 2305711: https://pubmed.ncbi.nlm.nih.gov/2305711/']
    return '\n'.join(lines) + '\n'


def save_report(path: Path, data: dict) -> Path:
    path = Path(path)
    path.write_text(build_report(data), encoding='utf-8')
    return path
