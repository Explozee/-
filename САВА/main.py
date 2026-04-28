import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# --- Настройки ---
DATA_FILE = "expenses.json"

# --- Загрузка данных из JSON ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- Сохранение данных в JSON ---
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Валидация и добавление расхода ---
def add_expense():
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    # Проверка суммы
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
        return

    # Проверка даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД!")
        return

    # Добавление в таблицу и список
    expenses.append({"amount": amount, "category": category, "date": date})
    save_data(expenses)
    update_table()

    # Очистка полей
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# --- Обновление таблицы ---
def update_table(filter_category=None, filter_date=None):
    for i in tree.get_children():
        tree.delete(i)

    filtered = expenses
    if filter_category and filter_category != "Все":
        filtered = [e for e in filtered if e["category"] == filter_category]
    if filter_date:
        filtered = [e for e in filtered if e["date"] == filter_date]

    for e in filtered:
        tree.insert("", "end", values=(e["date"], e["category"], f"{e['amount']:.2f} ₽"))

# --- Подсчёт суммы за период ---
def calculate_sum():
    try:
        start_date = datetime.strptime(entry_start.get(), "%Y-%m-%d")
        end_date = datetime.strptime(entry_end.get(), "%Y-%m-%d")
        total = sum(
            e["amount"] for e in expenses
            if start_date <= datetime.strptime(e["date"], "%Y-%m-%d") <= end_date
        )
        label_sum.config(text=f"Итого: {total:.2f} ₽")
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте формат дат (ГГГГ-ММ-ДД)!")

# --- Фильтрация ---
def apply_filter():
    category = combo_filter_category.get()
    date = entry_filter_date.get()
    update_table(filter_category=category, filter_date=date)

# --- Инициализация данных ---
expenses = load_data()

# --- Создание окна ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x500")
root.resizable(False, False)

# --- Вкладка "Добавить расход" ---
tab_control = ttk.Notebook(root)
tab_add = ttk.Frame(tab_control)
tab_stats = ttk.Frame(tab_control)
tab_control.add(tab_add, text="Добавить расход")
tab_control.add(tab_stats, text="Статистика")
tab_control.pack(expand=1, fill="both")

# Форма добавления расхода
tk.Label(tab_add, text="Сумма:").grid(row=0, column=0, padx=10, pady=5)
entry_amount = tk.Entry(tab_add)
entry_amount.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tab_add, text="Категория:").grid(row=1, column=0, padx=10, pady=5)
combo_category = ttk.Combobox(tab_add, values=["Еда", "Транспорт", "Развлечения", "Прочее"])
combo_category.current(0)
combo_category.grid(row=1, column=1, padx=10, pady=5)

tk.Label(tab_add, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=10, pady=5)
entry_date = tk.Entry(tab_add)
entry_date.grid(row=2, column=1, padx=10, pady=5)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

btn_add = tk.Button(tab_add, text="Добавить расход", command=add_expense)
btn_add.grid(row=3, columnspan=2, pady=15)

# Таблица расходов
tree = ttk.Treeview(tab_add, columns=("Дата", "Категория", "Сумма"), show="headings")
tree.heading("Дата", text="Дата")
tree.heading("Категория", text="Категория")
tree.heading("Сумма", text="Сумма")
tree.column("Сумма", anchor="e")
tree.pack(fill="both", expand=True)
update_table()

# Фильтры (на второй вкладке)
tk.Label(tab_stats, text="Фильтр по категории:").pack(pady=5)
combo_filter_category = ttk.Combobox(tab_stats, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Прочее"])
combo_filter_category.current(0)
combo_filter_category.pack(pady=5)

tk.Label(tab_stats, text="Фильтр по дате (ГГГГ-ММ-ДД):").pack(pady=5)
entry_filter_date = tk.Entry(tab_stats)
entry_filter_date.pack(pady=5)
btn_filter = tk.Button(tab_stats, text="Применить фильтр", command=apply_filter)
btn_filter.pack(pady=10)

# Подсчёт суммы за период
tk.Label(tab_stats, text="Период для подсчёта суммы:").pack(pady=5)
frame_dates = tk.Frame(tab_stats)
frame_dates.pack(pady=5)
tk.Label(frame_dates, text="С:").pack(side="left")
entry_start = tk.Entry(frame_dates, width=12)
entry_start.pack(side="left", padx=5)
entry_start.insert(0, "2024-01-01")
tk.Label(frame_dates, text="По:").pack(side="left")
entry_end = tk.Entry(frame_dates, width=12)
entry_end.pack(side="left", padx=5)
entry_end.insert(0, datetime.now().strftime("%Y-%m-%d"))
btn_sum = tk.Button(tab_stats, text="Посчитать сумму", command=calculate_sum)
btn_sum.pack(pady=5)
label_sum = tk.Label(tab_stats, text="Итого: 0.00 ₽", font=("Arial", 12))
label_sum.pack(pady=15)