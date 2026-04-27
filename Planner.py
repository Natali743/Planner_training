# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:56:24 2026

@author: student
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# --- Глобальные переменные ---
workouts = []  # Список для хранения всех тренировок
current_file_path = None  # Путь к текущему файлу, если он был загружен/сохранен

# --- Функции валидации ---
def is_valid_date(date_str):
    """Проверяет, соответствует ли строка формату ДД.ММ.ГГГГ"""
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def is_valid_duration(duration_str):
    """Проверяет, является ли строка положительным целым числом"""
    return duration_str.isdigit() and int(duration_str) > 0

# --- Функции для работы с данными ---
def update_table(data_to_display):
    """Очищает и заполняет таблицу данными."""
    # Удаляем все существующие элементы в таблице
    for item in tree.get_children():
        tree.delete(item)
    # Вставляем новые данные
    for i, workout in enumerate(data_to_display):
        tree.insert("", tk.END, values=(workout["date"], workout["type"], workout["duration"]), tags=(i,)) # Добавляем тег для идентификации

def add_workout():
    """Добавляет новую тренировку из полей ввода в список и обновляет таблицу."""
    date_str = date_entry.get().strip()
    workout_type = type_entry.get().strip()
    duration_str = duration_entry.get().strip()

    # Валидация ввода
    if not date_str or not workout_type or not duration_str:
        messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены.")
        return
    if not is_valid_date(date_str):
        messagebox.showwarning("Ошибка ввода", "Некорректный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    if not is_valid_duration(duration_str):
        messagebox.showwarning("Ошибка ввода", "Длительность должна быть положительным числом (минут).")
        return

    duration = int(duration_str)

    # Добавляем тренировку в глобальный список
    workouts.append({"date": date_str, "type": workout_type, "duration": duration})

    # Обновляем таблицу (отображаем все данные, чтобы фильтры не сбрасывались)
    update_table(workouts)

    # Очищаем поля ввода
    date_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

    # Устанавливаем фокус обратно на поле даты
    date_entry.focus_set()

def save_to_json():
    """Сохраняет список тренировок в файл JSON."""
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Сохранить тренировки как..."
    )
    if not file_path:
        return # Пользователь отменил сохранение

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            # Используем ensure_ascii=False для корректной записи кириллицы
            # indent=4 делает файл более читаемым
            import json
            json.dump(workouts, f, ensure_ascii=False, indent=4)
        current_file_path = file_path  # Обновляем путь к файлу
        messagebox.showinfo("Сохранение", f"Тренировки успешно сохранены в файл:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")



def apply_filter():
    """Фильтрует тренировки по дате и типу."""
    filter_date = filter_date_entry.get().strip()
    filter_type = filter_type_entry.get().strip()

    filtered_list = []
    for workout in workouts:
        match_date = True
        match_type = True

        if filter_date:
            if not is_valid_date(filter_date):
                messagebox.showwarning("Ошибка фильтра", "Некорректный формат даты фильтра. Используйте ДД-ММ-ГГГГ.")
                return
            if workout["date"] != filter_date:
                match_date = False

        if filter_type:
            # Поиск без учета регистра
            if filter_type.lower() not in workout["type"].lower():
                match_type = False

        if match_date and match_type:
            filtered_list.append(workout)
    update_table(filtered_list)

def clear_filter():
    """Сбрасывает поля фильтра и отображает все тренировки."""
    filter_date_entry.delete(0, tk.END)
    filter_type_entry.delete(0, tk.END)
    update_table(workouts) # Показываем все тренировки



# --- Настройка главного окна ---
root = tk.Tk()
root.title("Планировщик тренировок")
root.geometry("900x600") # Устанавливаем размер окна

# --- Создание виджетов ---

# Фрейм для ввода данных
input_frame = ttk.LabelFrame(root, text="Добавить тренировку", padding="10")
input_frame.pack(pady=10, padx=10, fill=tk.X)

ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
date_entry = ttk.Entry(input_frame, width=15)
date_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

# Устанавливаем текущую дату при запуске
today = datetime.now().strftime("%d.%m.%Y")
date_entry.insert(0, today)
ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
type_entry = ttk.Entry(input_frame, width=30)
type_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
duration_entry = ttk.Entry(input_frame, width=10)
duration_entry.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)

add_button = ttk.Button(input_frame, text="Добавить тренировку", command=add_workout)
add_button.grid(row=0, column=6, padx=10)

# Фрейм для фильтрации
filter_frame = ttk.LabelFrame(root, text="Фильтр", padding="10")
filter_frame.pack(pady=5, padx=10, fill=tk.X)

ttk.Label(filter_frame, text="По дате (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
filter_date_entry = ttk.Entry(filter_frame, width=15)
filter_date_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

ttk.Label(filter_frame, text="По типу тренировки:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
filter_type_entry = ttk.Entry(filter_frame, width=30)
filter_type_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
filter_button.grid(row=0, column=4, padx=10)

clear_filter_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=clear_filter)
clear_filter_button.grid(row=0, column=5, padx=10)

# Фрейм для кнопок Сохранить/Загрузить
file_buttons_frame = ttk.Frame(root, padding="5")
file_buttons_frame.pack(pady=0, padx=10, fill=tk.X)

save_button = ttk.Button(file_buttons_frame, text="Сохранить в JSON", command=save_to_json)
save_button.pack(side=tk.LEFT, padx=5)


# Фрейм для таблицы
table_frame = ttk.Frame(root, padding="10")
table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Создаем виджет Treeview (таблица)
tree_columns = ("date", "type", "duration")
tree = ttk.Treeview(table_frame, columns=tree_columns, show="headings", height=15)

# Настраиваем заголовки столбцов
tree.heading("date", text="Дата")
tree.heading("type", text="Тип тренировки")
tree.heading("duration", text="Длительность (мин)")

# Настраиваем ширину столбцов
tree.column("date", width=50, anchor=tk.W)
tree.column("type", width=100, anchor=tk.W)
tree.column("duration", width=100, anchor=tk.CENTER)

# Добавляем полосы прокрутки
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
hsb.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.pack(fill=tk.BOTH, expand=True)



# --- Запуск приложения ---
if __name__ == "__main__":
    root.mainloop()