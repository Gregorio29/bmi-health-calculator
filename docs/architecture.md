# BMI & Anthropometric Health Calculator — Architecture

## Overview
A standalone desktop application designed with strict separation of concerns, deterministic mathematical arithmetic, and zero persistent storage of sensitive health telemetry.

```text
┌────────────────────────────────────────────────────────┐
│                   GUI Layer (ui.py)                    │
│      Tkinter / ttk custom styled desktop widgets       │
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼                        ▼
┌──────────────────────────────┐  ┌──────────────────────┐
│ Validation (validation.py)   │  │ History (history.py) │
│ - Decimal boundary checks    │  │ - In-memory only     │
│ - Unit sanitization          │  │ - Zero disk leaks    │
└───────────────┬──────────────┘  └──────────────────────┘
                │
                ▼
┌──────────────────────────────┐  ┌──────────────────────┐
│  Calculator (calculator.py)  │  │  Report (report.py)  │
│  - Decimal arithmetic        │─▶│  - Formatted text    │
│  - WHO / CDC BMI categories  │  │  - UTF-8 export      │
│  - Mifflin-St Jeor (BMR/TDEE)│  │  - Clinical disclaimer│
└──────────────────────────────┘  └──────────────────────┘
```

## Key Architectural Decisions

1. **Exact Precision (`decimal.Decimal`):** Avoids floating-point drift in medical calculations by using exact decimal representation and `ROUND_HALF_UP`.
2. **Privacy by Design:** Session history is maintained solely in memory during the app lifecycle and is never written to disk without explicit user export.
3. **Decoupled Business Logic:** Core algorithms in `calculator.py` and `validation.py` are completely decoupled from UI widgets, allowing 100% automated test coverage with `unittest`.
