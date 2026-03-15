import tkinter as tk
from tkinter import messagebox
import json
import os

SAVE_FILE = "tasks.json"

# Функції роботи з даними (Нова гілка)

def load_tasks():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        # ФУНКЦІОНАЛЬНА ПОМИЛКА №1
        # json.dump викликається БЕЗ параметра ensure_ascii=False,
        # тому всі кириличні символи зберігаються як \uXXXX-екранування.
        # При повторному завантаженні текст відображається коректно лише
        # через Python-декодування, але сам файл нечитабельний для людини
        # та сторонніх інструментів.
        json.dump(tasks, f)


# Логіка UI

def add_task():
    text = entry_task.get()
    priority = var_priority.get()

    # ФУНКЦІОНАЛЬНА ПОМИЛКА №2
    # Перевірка виконується через `if text == ""`, яка не відловлює рядки
    # що складаються лише з пробілів (наприклад "   ").
    # Такі «порожні» завдання додаються до списку.
    if text == "":
        messagebox.showwarning("Попередження", "Введіть текст завдання!")
        return

    task = {"text": text, "priority": priority, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    refresh_list()
    entry_task.delete(0, tk.END)


def delete_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Інфо", "Оберіть завдання для видалення.")
        return

    # ФУНКЦІОНАЛЬНА ПОМИЛКА №3
    # При видаленні кількох виділених елементів індекси зсуваються після
    # першого видалення, і наступний елемент видаляється неправильно.
    # Крім того, цикл іде у прямому порядку замість зворотного.
    for i in selected:
        tasks.pop(i)

    save_tasks(tasks)
    refresh_list()


def mark_done():
    selected = listbox.curselection()
    if not selected:
        return
    idx = selected[0]
    tasks[idx]["done"] = not tasks[idx]["done"]
    save_tasks(tasks)
    refresh_list()


def refresh_list():
    listbox.delete(0, tk.END)
    for t in tasks:
        status = "✓" if t["done"] else "○"
        label = f"[{t['priority']}] {status} {t['text']}"
        listbox.insert(tk.END, label)
        if t["done"]:
            listbox.itemconfig(tk.END, fg="gray")


# Побудова вікна

root = tk.Tk()
root.title("Менеджер завдань")

# UI/UX ПОМИЛКА №1 — Фіксований розмір вікна без можливості зміни
# resizable(False, False) забороняє користувачу змінювати розмір вікна.
# Якщо у списку багато завдань або шрифт системи більший —
# контент обрізається і недоступний.
root.geometry("400x300")
root.resizable(False, False)

tasks = load_tasks()

# Фрейм введення
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Завдання:").grid(row=0, column=0, padx=4)
entry_task = tk.Entry(frame_input, width=28)
entry_task.grid(row=0, column=1, padx=4)

tk.Label(frame_input, text="Пріоритет:").grid(row=1, column=0, padx=4, pady=4)
var_priority = tk.StringVar(value="Середній")

# UI/UX ПОМИЛКА №2 — Радіокнопки розташовані вертикально в одній клітинці
# Всі три радіокнопки запаковані в одну клітинку grid без відступів,
# через що вони накладаються або виглядають злипнутими.
for val in ("Низький", "Середній", "Високий"):
    tk.Radiobutton(frame_input, text=val, variable=var_priority,
                   value=val).grid(row=1, column=1)

# Кнопки керування
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=3)

# UI/UX ПОМИЛКА №3 — Кнопка «Видалити» виглядає так само, як інші кнопки
# Деструктивна дія (видалення) не має жодного візуального розрізнення:
# такий самий розмір, колір, шрифт. Це порушує принцип запобігання помилкам —
# користувач може випадково натиснути «Видалити» замість «Виконано».
tk.Button(frame_buttons, text="Додати", width=10, command=add_task).grid(row=0, column=0, padx=4)
tk.Button(frame_buttons, text="Виконано", width=10, command=mark_done).grid(row=0, column=1, padx=4)
tk.Button(frame_buttons, text="Видалити", width=10, command=delete_task).grid(row=0, column=2, padx=4)

# Список завдань
listbox = tk.Listbox(root, width=52, height=10, selectmode=tk.EXTENDED)
listbox.pack(pady=5)

refresh_list()
root.mainloop()
