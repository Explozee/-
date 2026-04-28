import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

# Используем API, не требующий ключа
API_URL = "https://er-api.com"
HISTORY_FILE = "history.json"

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Super Currency Converter")
        self.root.geometry("500x550")
        self.root.configure(bg="#f0f2f5")

        # Стили
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"))
        
        # Заголовок
        tk.Label(root, text="Конвертер валют", font=("Arial", 18, "bold"), bg="#f0f2f5", fg="#333").pack(pady=10)

        # Контейнер ввода
        input_frame = tk.Frame(root, bg="#f0f2f5")
        input_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(input_frame, text="Сумма:", bg="#f0f2f5").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        self.amount_entry.grid(row=1, column=0, pady=5, padx=5)

        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT"]
        
        self.from_box = ttk.Combobox(input_frame, values=self.currencies, width=8, font=("Arial", 11))
        self.from_box.set("USD")
        self.from_box.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="➔", font=("Arial", 12), bg="#f0f2f5").grid(row=1, column=2)

        self.to_box = ttk.Combobox(input_frame, values=self.currencies, width=8, font=("Arial", 11))
        self.to_box.set("RUB")
        self.to_box.grid(row=1, column=3, padx=5)

        # Кнопка
        self.convert_btn = tk.Button(root, text="КОНВЕРТИРОВАТЬ", command=self.convert, 
                                   bg="#007bff", fg="white", font=("Arial", 11, "bold"), 
                                   padx=20, pady=10, relief="flat", cursor="hand2")
        self.convert_btn.pack(pady=15)

        # Таблица истории
        tk.Label(root, text="История операций:", bg="#f0f2f5", font=("Arial", 10, "italic")).pack()
        
        columns = ("date", "from", "to", "result")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
        self.tree.heading("date", text="Дата")
        self.tree.heading("from", text="Из")
        self.tree.heading("to", text="В")
        self.tree.heading("result", text="Результат")
        
        for col in columns:
            self.tree.column(col, width=100, anchor="center")
            
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        self.history = self.load_history()
        self.update_table()

    def convert(self):
        amount = self.amount_entry.get()
        base = self.from_box.get().upper()
        target = self.to_box.get().upper()

        try:
            val = float(amount)
            if val <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите нормальное число больше 0")
            return

        try:
            response = requests.get(f"{API_URL}{base}")
            data = response.json()
            
            if data["result"] == "success":
                rate = data["rates"][target]
                res = round(val * rate, 2)
                
                # Показываем результат
                final_text = f"{val} {base} = {res} {target}"
                messagebox.showinfo("Готово!", final_text)

                # Сохраняем
                entry = {
                    "date": datetime.now().strftime("%H:%M:%S"),
                    "from": base,
                    "to": target,
                    "res": res
                }
                self.history.append(entry)
                self.save_history()
                self.update_table()
            else:
                messagebox.showerror("Ошибка", "Не удалось получить данные от API")
        except:
            messagebox.showerror("Ошибка", "Проблемы с интернетом")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=4)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in reversed(self.history[-10:]): # Показываем последние 10
            self.tree.insert("", "end", values=(item["date"], item["from"], item["to"], item["res"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
