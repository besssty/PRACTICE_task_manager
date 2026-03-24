"""
test_task_logic.py
==================
Тести для модуля task_logic.py.

Крок 1–2: assert-тести та unittest.TestCase-тести.
Крок 4:   секція з навмисно зламаними тестами (клас BrokenTests).
"""

import unittest
import json
import os
import tempfile

from task_logic import (
    create_task,
    delete_tasks_by_indices,
    toggle_done,
    format_task_label,
    save_tasks,
    load_tasks,
)

# ─────────────────────────────────────────────────────────────────────────────
# КРОК 1 — assert-тести (прості функціональні перевірки)
# ─────────────────────────────────────────────────────────────────────────────

def run_assert_tests():
    print("=" * 60)
    print("КРОК 1: assert-тести")
    print("=" * 60)

    # assert-тест 1: create_task повертає правильну структуру
    task = create_task("Купити молоко", "Високий")
    assert task is not None,                          "Завдання не повинно бути None"
    assert task["text"] == "Купити молоко",           "Текст завдання збережено неправильно"
    assert task["priority"] == "Високий",             "Пріоритет збережено неправильно"
    assert task["done"] is False,                     "Нове завдання має бути невиконаним"
    print("  [PASS] assert-тест 1: create_task повертає коректну структуру")

    # assert-тест 2: create_task відхиляє порожній / пробільний рядок
    assert create_task("") is None,                   "Порожній рядок має повертати None"
    assert create_task("   ") is None,                "Рядок з пробілів має повертати None"
    print("  [PASS] assert-тест 2: create_task відхиляє порожній рядок")

    # assert-тест 3: delete_tasks_by_indices видаляє правильні елементи
    tasks = [
        {"text": "A", "priority": "Низький",  "done": False},
        {"text": "B", "priority": "Середній", "done": False},
        {"text": "C", "priority": "Високий",  "done": False},
    ]
    result = delete_tasks_by_indices(tasks, [0, 2])
    assert len(result) == 1,            "Після видалення 2 з 3 має лишитись 1 завдання"
    assert result[0]["text"] == "B",    "Має лишитись завдання 'B'"
    print("  [PASS] assert-тест 3: delete_tasks_by_indices видаляє правильні елементи")

    print()


# ─────────────────────────────────────────────────────────────────────────────
# КРОК 2 — unittest.TestCase-тести
# ─────────────────────────────────────────────────────────────────────────────

class TestCreateTask(unittest.TestCase):
    """Тести функції create_task."""

    def test_valid_task_structure(self):
        """Перевіряє, що create_task повертає словник з усіма полями."""
        task = create_task("Написати звіт", "Середній")
        self.assertIsNotNone(task)
        self.assertIn("text", task)
        self.assertIn("priority", task)
        self.assertIn("done", task)
        self.assertEqual(task["text"], "Написати звіт")
        self.assertFalse(task["done"])

    def test_empty_text_returns_none(self):
        """Порожній і пробільний рядок мають повертати None."""
        self.assertIsNone(create_task(""))
        self.assertIsNone(create_task("   "))
        self.assertIsNone(create_task("\t\n"))

    def test_text_is_stripped(self):
        """Пробіли на початку/кінці тексту мають обрізатися."""
        task = create_task("  Зателефонувати  ")
        self.assertEqual(task["text"], "Зателефонувати")


class TestDeleteTasks(unittest.TestCase):
    """Тести функції delete_tasks_by_indices."""

    def setUp(self):
        self.tasks = [
            {"text": "Завдання 1", "priority": "Низький",  "done": False},
            {"text": "Завдання 2", "priority": "Середній", "done": False},
            {"text": "Завдання 3", "priority": "Високий",  "done": True},
        ]

    def test_delete_single_task(self):
        """Видалення одного завдання зменшує список на 1."""
        result = delete_tasks_by_indices(self.tasks, [1])
        self.assertEqual(len(result), 2)
        texts = [t["text"] for t in result]
        self.assertNotIn("Завдання 2", texts)

    def test_delete_multiple_tasks(self):
        """Видалення кількох завдань (перший і останній індекс)."""
        result = delete_tasks_by_indices(self.tasks, [0, 2])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"], "Завдання 2")


class TestToggleAndFormat(unittest.TestCase):
    """Тести функцій toggle_done та format_task_label."""

    def test_toggle_done_false_to_true(self):
        tasks = [{"text": "X", "priority": "Середній", "done": False}]
        toggle_done(tasks, 0)
        self.assertTrue(tasks[0]["done"])

    def test_toggle_done_true_to_false(self):
        tasks = [{"text": "X", "priority": "Середній", "done": True}]
        toggle_done(tasks, 0)
        self.assertFalse(tasks[0]["done"])

    def test_format_label_done(self):
        task = {"text": "Сходити до лікаря", "priority": "Високий", "done": True}
        label = format_task_label(task)
        self.assertIn("✓", label)
        self.assertIn("Високий", label)
        self.assertIn("Сходити до лікаря", label)

    def test_format_label_not_done(self):
        task = {"text": "Купити хліб", "priority": "Низький", "done": False}
        label = format_task_label(task)
        self.assertIn("○", label)


class TestSaveLoad(unittest.TestCase):
    """Тести функцій save_tasks / load_tasks з тимчасовим файлом."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.close()
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_save_and_load_roundtrip(self):
        """Збережені завдання завантажуються без втрат."""
        tasks = [{"text": "Тест", "priority": "Середній", "done": False}]
        save_tasks(tasks, self.filepath)
        loaded = load_tasks(self.filepath)
        self.assertEqual(tasks, loaded)

    def test_cyrillic_preserved(self):
        """Кирилиця зберігається як читабельний текст, не як \\uXXXX."""
        tasks = [{"text": "Кирилиця", "priority": "Середній", "done": False}]
        save_tasks(tasks, self.filepath)
        with open(self.filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        self.assertIn("Кирилиця", raw)
        self.assertNotIn("\\u041a", raw)  # \u041a = К

    def test_load_nonexistent_file(self):
        """load_tasks повертає порожній список, якщо файл відсутній."""
        result = load_tasks("/tmp/nonexistent_xyz_123.json")
        self.assertEqual(result, [])

# ─────────────────────────────────────────────────────────────────────────────
# Точка входу
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Крок 1: assert-тести
    run_assert_tests()

    # Кроки 2–3 та 5: unittest-тести
    # Щоб запустити тільки «правильні» тести (крок 3):
    #   python test_task_logic.py -- без прапора
    # Щоб запустити ВСІ тести включно з BrokenTests (крок 5):
    #   змінна нижче
    unittest.main(verbosity=2)
