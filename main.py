import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

DATA_FILE = 'expenses.json'

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_data()

        # Поля ввода
        frame_input = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=10)
        frame_input.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0)
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=2)
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "ЖКХ", "Прочее"])
        self.combo_category.grid(row=0, column=3)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=0, column=5)

        btn_add = tk.Button(frame_input, text="Добавить", command=self.add_expense, bg="green", fg="white")
        btn_add.grid(row=0, column=6, padx=10)

        # Фильтры
        frame_filter = tk.LabelFrame(root, text="Фильтрация и Итоги", padx=10, pady=10)
        frame_filter.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_filter, text="Категория:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "ЖКХ", "Прочее"])
        self.filter_cat.current(0)
        self.filter_cat.grid(row=0, column=1)

        btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.update_table)
        btn_filter.grid(row=0, column=2, padx=5)

        self.label_total = tk.Label(frame_filter, text="Итого: 0", font=('Arial', 10, 'bold'))
        self.label_total.grid(row=0, column=3, padx=20)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_table()

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combo_category.get()
        date_str = self.entry_date.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте сумму (число > 0) и формат даты (ГГГГ-ММ-ДД)")
            return

        if not category:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return

        new_item = {"amount": amount, "category": category, "date": date_str}
        self.expenses.append(new_item)
        self.save_data()
        self.update_table()
        self.entry_amount.delete(0, tk.END)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def update_table(self):
        # Очистка
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        cat_filter = self.filter_cat.get()
        total = 0

        for exp in self.expenses:
            if cat_filter == "Все" or exp['category'] == cat_filter:
                self.tree.insert("", "end", values=(exp['amount'], exp['category'], exp['date']))
                total += exp['amount']
        
        self.label_total.config(text=f"Итого: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
