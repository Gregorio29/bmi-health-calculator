"""Interfaz Tkinter para CALCULADORA_IMC."""
from decimal import Decimal
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from calculator import (ACTIVITY_FACTORS, bmi, bmi_category, feet_inches_to_meters,
                        height_to_meters, kg_to_lb, lb_to_kg, mifflin_st_jeor,
                        reference_weight_range, tdee, weight_change)
from history import SessionHistory
from report import save_report
from sources import DISCLAIMER
from validation import parse_decimal, validate_age, validate_height, validate_weight

BG, CARD, ACCENT, TEXT, MUTED = '#f5f7fb', '#ffffff', '#1769aa', '#16212d', '#5c6875'


class BMIApp:
    def __init__(self, root: tk.Tk):
        self.root, self.history = root, SessionHistory()
        root.title('CALCULADORA IMC | PROY-IMC-001')
        root.geometry('1050x720'); root.minsize(860, 600); root.configure(bg=BG)
        style = ttk.Style(); style.theme_use('clam')
        style.configure('TFrame', background=BG); style.configure('Card.TFrame', background=CARD)
        style.configure('TLabel', background=CARD, foreground=TEXT, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=BG, foreground=TEXT, font=('Segoe UI Semibold', 21))
        style.configure('Sub.TLabel', background=BG, foreground=MUTED, font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI Semibold', 10), padding=8)
        style.configure('Accent.TButton', foreground='white', background=ACCENT)
        self._variables(); self._build(); root.bind('<Return>', self._on_enter)

    def _variables(self):
        self.age_var = tk.StringVar(); self.sex_var = tk.StringVar(value='No especificar')
        self.weight_var = tk.StringVar(); self.weight_unit = tk.StringVar(value='kg')
        self.height_var = tk.StringVar(); self.height_unit = tk.StringVar(value='cm')
        self.feet_var = tk.StringVar(); self.inches_var = tk.StringVar()
        self.previous_var = tk.StringVar(); self.activity_var = tk.StringVar(value='No calcular')

    def _build(self):
        header = ttk.Frame(self.root, padding=(24, 18, 24, 8)); header.grid(sticky='ew'); header.columnconfigure(0, weight=1)
        ttk.Label(header, text='Calculadora de IMC y peso de referencia', style='Title.TLabel').grid(row=0, column=0, sticky='w')
        ttk.Label(header, text='PROYECTO — CALCULADORA DE IMC Y PESO DE REFERENCIA · PROY-IMC-001', style='Sub.TLabel').grid(row=1, column=0, sticky='w')
        shell = ttk.Frame(self.root, padding=(24, 8, 24, 18)); shell.grid(sticky='nsew'); self.root.rowconfigure(1, weight=1); shell.columnconfigure((0, 1), weight=1); shell.rowconfigure(0, weight=1)
        left = ttk.Frame(shell, style='Card.TFrame', padding=18); left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        right = ttk.Frame(shell, style='Card.TFrame', padding=18); right.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        self._form(left); self._result_panel(right)

    def _row(self, parent, row, label, variable, choices=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=(7, 2))
        widget = ttk.Combobox(parent, textvariable=variable, values=choices, state='readonly') if choices else ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row + 1, column=0, columnspan=2, sticky='ew', pady=(0, 5)); return widget

    def _form(self, frame):
        frame.columnconfigure((0, 1), weight=1)
        ttk.Label(frame, text='Datos de entrada', font=('Segoe UI Semibold', 14)).grid(row=0, column=0, columnspan=2, sticky='w')
        self._row(frame, 1, 'Edad (años)', self.age_var)
        self._row(frame, 3, 'Sexo (solo requerido para TMB)', self.sex_var, ('Masculino', 'Femenino', 'No especificar'))
        ttk.Label(frame, text='Peso actual').grid(row=5, column=0, sticky='w', pady=(7, 2))
        ttk.Entry(frame, textvariable=self.weight_var).grid(row=6, column=0, sticky='ew', padx=(0, 5))
        ttk.Combobox(frame, textvariable=self.weight_unit, values=('kg', 'lb'), state='readonly', width=8).grid(row=6, column=1, sticky='ew')
        ttk.Label(frame, text='Estatura').grid(row=7, column=0, sticky='w', pady=(7, 2))
        ttk.Entry(frame, textvariable=self.height_var).grid(row=8, column=0, sticky='ew', padx=(0, 5))
        unit_box = ttk.Combobox(frame, textvariable=self.height_unit, values=('cm', 'm', 'pies/pulgadas'), state='readonly', width=12); unit_box.grid(row=8, column=1, sticky='ew'); unit_box.bind('<<ComboboxSelected>>', lambda _e: self._height_hint())
        self.height_hint = ttk.Label(frame, text='Ingrese cm o m.', foreground=MUTED); self.height_hint.grid(row=9, column=0, columnspan=2, sticky='w')
        feet_frame = ttk.Frame(frame, style='Card.TFrame'); feet_frame.grid(row=10, column=0, columnspan=2, sticky='ew', pady=2)
        ttk.Entry(feet_frame, textvariable=self.feet_var, width=8).pack(side='left'); ttk.Label(feet_frame, text=' pies   ').pack(side='left'); ttk.Entry(feet_frame, textvariable=self.inches_var, width=8).pack(side='left'); ttk.Label(feet_frame, text=' pulgadas').pack(side='left')
        self._row(frame, 11, 'Peso anterior (opcional; misma unidad)', self.previous_var)
        self._row(frame, 13, 'Actividad (TDEE opcional)', self.activity_var, ('No calcular', *ACTIVITY_FACTORS.keys()))
        buttons = ttk.Frame(frame, style='Card.TFrame'); buttons.grid(row=15, column=0, columnspan=2, sticky='ew', pady=(12, 0)); buttons.columnconfigure((0, 1), weight=1)
        ttk.Button(buttons, text='CALCULAR', style='Accent.TButton', command=self.calculate).grid(row=0, column=0, sticky='ew', padx=(0, 4))
        ttk.Button(buttons, text='LIMPIAR', command=self.clear).grid(row=0, column=1, sticky='ew', padx=(4, 0))
        ttk.Button(frame, text='GUARDAR INFORME', command=self.save_current_report).grid(row=16, column=0, columnspan=2, sticky='ew', pady=(8, 0))
        ttk.Button(frame, text='VER / LIMPIAR HISTORIAL', command=self.show_history).grid(row=17, column=0, columnspan=2, sticky='ew', pady=(6, 0))

    def _result_panel(self, frame):
        ttk.Label(frame, text='Resultados orientativos', font=('Segoe UI Semibold', 14)).pack(anchor='w')
        self.results = tk.Text(frame, height=22, wrap='word', borderwidth=0, bg=CARD, fg=TEXT, font=('Segoe UI', 10), padx=0, pady=10)
        self.results.pack(fill='both', expand=True); self.results.configure(state='disabled')
        ttk.Label(frame, text='Advertencia', font=('Segoe UI Semibold', 11)).pack(anchor='w', pady=(8, 0))
        ttk.Label(frame, text=DISCLAIMER, wraplength=430, foreground=MUTED).pack(anchor='w', pady=(2, 0))
        ttk.Label(frame, text='Fuentes: CDC (categorías de adultos); Mifflin et al., 1990 (TMB).', wraplength=430, foreground=MUTED).pack(anchor='w', pady=(10, 0))

    def _height_hint(self):
        self.height_hint.configure(text='Use pies y pulgadas abajo (pulgadas: 0 a <12).' if self.height_unit.get() == 'pies/pulgadas' else 'Ingrese cm o m.')

    def _on_enter(self, _event): self.calculate(); return 'break'
    def _show_result(self, text):
        self.results.configure(state='normal'); self.results.delete('1.0', 'end'); self.results.insert('1.0', text); self.results.configure(state='disabled')

    def _collect(self):
        age = validate_age(self.age_var.get())
        raw_weight = validate_weight(self.weight_var.get())
        kg = raw_weight if self.weight_unit.get() == 'kg' else lb_to_kg(raw_weight)
        if self.height_unit.get() == 'pies/pulgadas':
            feet = int(self.feet_var.get().strip()); inches = parse_decimal(self.inches_var.get(), 'Pulgadas'); meters = feet_inches_to_meters(feet, inches)
        else:
            raw_height = parse_decimal(self.height_var.get(), 'Estatura')
            meters = height_to_meters(raw_height, self.height_unit.get()); meters = validate_height(str(meters))
        return age, kg, meters

    def calculate(self):
        try:
            age, kg, meters = self._collect()
            if age < 20:
                self._show_result('Para menores de 20 años se requiere IMC según edad y sexo con tablas de crecimiento apropiadas. No se aplicaron categorías de IMC para adultos.')
                return
            value, category = bmi(kg, meters), bmi_category(bmi(kg, meters)); low, high = reference_weight_range(meters)
            diff = ''
            if kg < low: diff = f'\nDiferencia hasta el límite inferior: {low - kg:.2f} kg.'
            elif kg > high: diff = f'\nDiferencia sobre el límite superior: {kg - high:.2f} kg.'
            else: diff = '\nEl peso actual se encuentra dentro de este rango matemático de referencia.'
            lines = [f'Edad: {age} años', f'Estatura: {meters:.2f} m', f'Peso actual: {kg:.2f} kg ({kg_to_lb(kg):.2f} lb)', '', f'IMC: {value:.2f} kg/m²', f'Categoría CDC: {category}', f'Rango de peso correspondiente al IMC de referencia: {low:.2f}–{high:.2f} kg ({kg_to_lb(low):.2f}–{kg_to_lb(high):.2f} lb).', diff]
            if self.previous_var.get().strip():
                previous = validate_weight(self.previous_var.get()); previous = previous if self.weight_unit.get() == 'kg' else lb_to_kg(previous)
                absolute, percentage, movement = weight_change(previous, kg); lines.append(f'\nCambio de peso: {absolute:+.2f} kg ({percentage:+.2f} %); {movement}.')
            if self.sex_var.get() in ('Masculino', 'Femenino'):
                resting = mifflin_st_jeor(kg, meters * Decimal('100'), age, self.sex_var.get()); lines.append(f'\nTMB estimada (Mifflin–St Jeor): {resting} kcal/día.')
                if self.activity_var.get() != 'No calcular': lines.append(f'TDEE estimado ({self.activity_var.get()}): {tdee(resting, self.activity_var.get())} kcal/día.')
            elif self.activity_var.get() != 'No calcular': lines.append('\nTDEE no calculado: la TMB requiere seleccionar sexo para esta fórmula.')
            text = '\n'.join(lines); self._show_result(text)
            self.current_data = {'Edad': str(age), 'Estatura': f'{meters:.2f} m', 'Peso actual': f'{kg:.2f} kg', 'IMC': f'{value:.2f}', 'Categoría': category, 'Resultados': text}
            self.history.add(self.current_data)
        except (ValueError, ArithmeticError) as error: messagebox.showerror('Revise los datos', str(error))

    def clear(self):
        for variable in (self.age_var, self.weight_var, self.height_var, self.feet_var, self.inches_var, self.previous_var): variable.set('')
        self.sex_var.set('No especificar'); self.weight_unit.set('kg'); self.height_unit.set('cm'); self.activity_var.set('No calcular'); self._height_hint(); self._show_result('')
        self.current_data = None

    def save_current_report(self):
        if not getattr(self, 'current_data', None): messagebox.showinfo('Informe', 'Calcule un resultado antes de guardarlo.'); return
        filename = filedialog.asksaveasfilename(defaultextension='.txt', initialfile='CALCULADORA_IMC_INFORME.txt', filetypes=[('Informe de texto', '*.txt')])
        if filename: save_report(Path(filename), self.current_data); messagebox.showinfo('Informe guardado', 'El informe se guardó localmente.')

    def show_history(self):
        entries = self.history.items()
        if not entries: messagebox.showinfo('Historial', 'No hay cálculos en esta sesión.'); return
        window = tk.Toplevel(self.root); window.title('Historial de sesión'); window.geometry('560x360')
        text = tk.Text(window, wrap='word'); text.pack(fill='both', expand=True, padx=12, pady=12)
        for index, entry in enumerate(entries, 1): text.insert('end', f'{index}. IMC {entry["IMC"]} — {entry["Categoría"]}\n')
        ttk.Button(window, text='Eliminar historial', command=lambda: (self.history.clear(), window.destroy())).pack(pady=(0, 12))
