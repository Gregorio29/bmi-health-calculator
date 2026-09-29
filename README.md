# BMI & Anthropometric Health Calculator (Desktop App)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI: Tkinter](https://img.shields.io/badge/GUI-Tkinter-teal.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Unittest](https://img.shields.io/badge/Tests-16%20Passed-green.svg)](#)

Desktop health calculator in Python for BMI, BMR and TDEE calculations with validation, testing and privacy-first in-memory history. Built in pure Python with exact `decimal.Decimal` arithmetic, input validation, in-memory session history, and report export.

> **Disclaimer:** This software is designed strictly for informational and educational purposes and does not substitute evaluation, diagnosis, or advice from a qualified healthcare professional.

---

## 🌟 Key Features

- **Exact Arithmetic:** Uses Python's `decimal.Decimal` with standard rounding to prevent floating-point inaccuracies.
- **WHO & CDC Adult Categories:** Classifies BMI accurately from underweight to Class III obesity.
- **Mifflin-St Jeor Metabolic Engine:** Calculates resting metabolic rate (BMR) and daily caloric needs (TDEE) based on activity levels.
- **Dual Unit Support:** Metric (kg/cm) and Imperial (lbs/inches) inputs with conversion.
- **Privacy by Design:** Session history is kept in memory; health entries are never written to disk without explicit user export.
- **Structured Report Export:** Generates formatted UTF-8 text summaries with clinical disclaimers.
- **Standalone Packaging:** Ready to compile into a zero-dependency Windows executable via PyInstaller.

---

## 🛠️ Project Structure

```text
CALCULADORA_IMC/
├── calculator.py       # Core anthropometric formulas & Decimal calculations
├── validation.py       # Safe input sanitization and boundary checks
├── history.py          # In-memory privacy-first session manager
├── report.py           # Formatted report generation with disclaimer
├── sources.py          # CDC & Mifflin citations and clinical disclaimer
├── ui.py               # Tkinter GUI implementation
├── main.py             # Application entrypoint
├── build_exe.py        # PyInstaller build script
├── docs/               # Architecture and clinical equations documentation
├── tests/              # 16 unit tests covering core logic, UI, and validation
└── requirements.txt    # Build dependencies
```

---

## 📦 Installation & Quick Start

```bash
git clone https://github.com/<username>/bmi-health-calculator.git
cd bmi-health-calculator
pip install -r requirements.txt
python main.py
```

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🔨 Building Standalone Windows Executable

```bash
python build_exe.py
```
The compiled `.exe` will be generated in `dist/CALCULADORA_IMC/`.

---

## ⚖️ Clinical Disclaimer

This software provides general nutritional and metabolic estimates and is intended for informational and educational purposes only. It does not constitute medical diagnosis or individual clinical advice.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
