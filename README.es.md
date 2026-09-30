# Calculadora de Salud Antropométrica e IMC (App de Escritorio)

[English](README.md) | [Español](README.es.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI: Tkinter](https://img.shields.io/badge/GUI-Tkinter-teal.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Unittest](https://img.shields.io/badge/Tests-16%20Passed-green.svg)](#)

Calculadora de salud de escritorio en Python para cálculos de IMC, Tasa Metabólica Basal (BMR) y Gasto Energético Diario (TDEE) con validación estricta, tests unitarios y privacidad mediante historial en memoria. Desarrollada en Python puro con aritmética exacta `decimal.Decimal`, validación de entradas, gestión de sesiones y exportación de reportes.

> **Aviso Legal / Exención de Responsabilidad:** Este software ha sido diseñado estrictamente con fines informativos y educativos. No constituye un diagnóstico médico ni sustituye la evaluación, diagnóstico o asesoramiento de un profesional sanitario cualificado.

---

## 🌟 Características Principales

- **Aritmética Exacta:** Utiliza `decimal.Decimal` de Python con redondeo estándar para prevenir imprecisiones de coma flotante.
- **Categorías Adultas OMS y CDC:** Clasifica el IMC con precisión desde bajo peso hasta obesidad de Clase III.
- **Motor Metabólico Mifflin-St Jeor:** Calcula la tasa metabólica basal en reposo (BMR) y el gasto calórico diario total (TDEE) según el nivel de actividad física.
- **Soporte de Unidades Doble:** Sistema métrico (kg/cm) e imperial (lbs/pulgadas) con conversión automática.
- **Privacidad por Diseño:** El historial de la sesión se mantiene exclusivamente en memoria; los datos nunca se guardan en disco sin una exportación explícita del usuario.
- **Exportación de Reportes Estructurados:** Genera resúmenes en texto plano formateado UTF-8 con descargos de responsabilidad médica.
- **Empaquetado Standalone:** Listo para compilarse en un ejecutable Windows sin dependencias externas mediante PyInstaller.

---

## 🛠️ Estructura del Proyecto

```text
CALCULADORA_IMC/
├── calculator.py       # Fórmulas antropométricas centrales y cálculos Decimal
├── validation.py       # Sanitización segura de entradas y validación de límites
├── history.py          # Gestor de sesión en memoria enfocado en privacidad
├── report.py           # Generación de reportes formateados con aviso legal
├── sources.py          # Citas CDC / Mifflin y descargos de responsabilidad
├── ui.py               # Implementación de interfaz gráfica con Tkinter
├── main.py             # Punto de entrada de la aplicación
├── build_exe.py        # Script de compilación PyInstaller
├── docs/               # Documentación de arquitectura y ecuaciones clínicas
├── tests/              # 16 pruebas unitarias cubriendo lógica, UI y validación
└── requirements.txt    # Dependencias de compilación
```

---

## 📦 Instalación y Uso Rápido

```bash
git clone https://github.com/Gregorio29/bmi-health-calculator.git
cd bmi-health-calculator
pip install -r requirements.txt
python main.py
```

---

## 🧪 Ejecución de Pruebas Unitarias

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🔨 Compilar Ejecutable Standalone para Windows

```bash
python build_exe.py
```
El archivo compilado `.exe` se generará en `dist/CALCULADORA_IMC/`.

---

## 📄 Licencia

Este proyecto está distribuido bajo la [Licencia MIT](LICENSE).
