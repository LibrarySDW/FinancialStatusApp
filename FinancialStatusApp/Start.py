import tkinter as tk
from tkinter import messagebox
from joblib import load
import pandas as pd
import pyautogui
import numpy as np
import os
import sys


def resource_path(relative_path):
    """Путь к ресурсам, работает в скрипте и в собранном приложении."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class FinancialStatusApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Финансовый прогноз статуса")
        
        window_width, window_height = 500, 550
        screen_width, screen_height = pyautogui.size()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # # Установка иконки
        # icon_path = resource_path('gui/window_icon.ico')  # .ico
        # self.master.iconphoto(False, tk.PhotoImage(file=icon_path))

        # Поля ввода
        tk.Label(self.master, text="Возраст \n(оптимально 18 ~ 79) ").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.age_entry = tk.Entry(self.master, width=20)
        self.age_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Доход \n(оптимально 0 ~ 83970) ").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.income_entry = tk.Entry(self.master, width=20)
        self.income_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Сумма кредита \n(оптимально 0 ~ 18051) ").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.loan_entry = tk.Entry(self.master, width=20)
        self.loan_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Кредитный рейтинг \n(оптимально -45 ~ 860) ").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.credit_score_entry = tk.Entry(self.master, width=20)
        self.credit_score_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Сбережения \n(оптимально -2806 ~ 29350) ").grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.savings_entry = tk.Entry(self.master, width=20)
        self.savings_entry.grid(row=4, column=1, padx=10, pady=10)

        # Кнопка
        self.predict_button = tk.Button(self.master, text="Предсказать", command=self.predict)
        self.predict_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Метка и поле для вывода результата
        self.result_label = tk.Label(self.master, text="Предсказанный \nфинансовый статус: ")
        self.result_label.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.result_entry = tk.Entry(self.master, state=tk.DISABLED, width=20, bg='white')
        self.result_entry.grid(row=6, column=1, padx=10, pady=10)

        # Загрузка модели
        self.model = load(resource_path('finance_model.joblib'))

    def predict(self):
        # Получаем данные из полей ввода
        try:
            age = int(self.age_entry.get())
            income = float(self.income_entry.get())
            loan_amount = float(self.loan_entry.get())
            credit_score = int(self.credit_score_entry.get())
            savings = float(self.savings_entry.get())

            if age < 18:
                raise ValueError("Младше 18 - кредиты не выдаются!")
            if income < 0:
                raise ValueError("Отрицательные значения дохода не допускаются!")
            if loan_amount <= 0:
                raise ValueError("Сумма кредита должна быть > 0!")

            # Формируем входные данные для модели
            input_data = pd.DataFrame([[age, income, loan_amount, credit_score, savings]], 
                                       columns=['Age', 'Income', 'Loan_Amount', 'Credit_Score', 'Savings'])

            # Предсказание
            prediction = self.model.predict(input_data)

            self.result_entry.config(state=tk.NORMAL)
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(tk.END, prediction[0])  
            self.result_entry.config(state=tk.DISABLED)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", "Неверно введены данные.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialStatusApp(root)
    root.mainloop()
