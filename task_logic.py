"""
task_logic.py — чиста бізнес-логіка менеджера завдань (без UI).
Виділена з task_manager.py для можливості юніт-тестування.
"""

import json
import os

SAVE_FILE = "tasks.json"


def load_tasks(filepath=SAVE_FILE):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks, filepath=SAVE_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)


def create_task(text, priority="Середній"):
    """Створює словник завдання. Повертає None, якщо текст порожній."""
    if not text.strip():
        return None
    return {"text": text.strip(), "priority": priority, "done": False}


def delete_tasks_by_indices(tasks, indices):
    """
    Видаляє завдання за списком індексів.
    Індекси обробляються у зворотному порядку, щоб уникнути зсуву.
    """
    for i in sorted(set(indices), reverse=True):
        tasks.pop(i)
    return tasks


def toggle_done(tasks, index):
    """Перемикає статус виконання завдання за індексом."""
    tasks[index]["done"] = not tasks[index]["done"]
    return tasks


def format_task_label(task):
    """Повертає рядок для відображення завдання у списку."""
    status = "✓" if task["done"] else "○"
    return f"[{task['priority']}] {status} {task['text']}"
