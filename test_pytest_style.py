import pytest
from pytest import fixture, mark, raises

from task_logic import (
    create_task,
    delete_tasks_by_indices,
    toggle_done,
    format_task_label,
    save_tasks,
)


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 1  —  assert-тести (ті самі, що раніше, тепер через pytest runner)
# ══════════════════════════════════════════════════════════════════════════════

def test_assert_create_task_structure():
    """Крок 1-а: create_task повертає коректну структуру."""
    task = create_task("Купити молоко", "Високий")
    assert task is not None
    assert task["text"] == "Купити молоко"
    assert task["priority"] == "Високий"
    assert task["done"] is False


def test_assert_empty_text_returns_none():
    """Крок 1-б: create_task відхиляє порожній / пробільний рядок."""
    assert create_task("") is None
    assert create_task("   ") is None


def test_assert_delete_removes_correct_items():
    """Крок 1-в: delete_tasks_by_indices видаляє правильні елементи."""
    tasks = [
        {"text": "A", "priority": "Низький",  "done": False},
        {"text": "B", "priority": "Середній", "done": False},
        {"text": "C", "priority": "Високий",  "done": False},
    ]
    result = delete_tasks_by_indices(tasks, [0, 2])
    assert len(result) == 1
    assert result[0]["text"] == "B"


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 2-а  —  @pytest.fixture
# ══════════════════════════════════════════════════════════════════════════════

@fixture
def sample_tasks():
    """Фікстура: повертає список із трьох тестових завдань."""
    return [
        {"text": "Завдання 1", "priority": "Низький",  "done": False},
        {"text": "Завдання 2", "priority": "Середній", "done": True},
        {"text": "Завдання 3", "priority": "Високий",  "done": False},
    ]


@fixture
def single_task():
    """Фікстура: повертає одне завдання."""
    return {"text": "Тестове завдання", "priority": "Середній", "done": False}


def test_fixture_toggle_changes_done(sample_tasks):
    """Крок 2: фікстура sample_tasks — toggle змінює статус."""
    original = sample_tasks[0]["done"]
    toggle_done(sample_tasks, 0)
    assert sample_tasks[0]["done"] != original


def test_fixture_format_includes_status(single_task):
    """Крок 2: фікстура single_task — формат містить символ ○."""
    label = format_task_label(single_task)
    assert "○" in label
    assert "Тестове завдання" in label


def test_fixture_delete_reduces_length(sample_tasks):
    """Крок 2: фікстура sample_tasks — видалення зменшує список."""
    before = len(sample_tasks)
    delete_tasks_by_indices(sample_tasks, [0])
    assert len(sample_tasks) == before - 1


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 2-б  —  @pytest.mark.parametrize
# ══════════════════════════════════════════════════════════════════════════════

@mark.parametrize("text,priority,expected_text", [
    ("Зателефонувати", "Низький",  "Зателефонувати"),
    ("  Написати звіт  ", "Середній", "Написати звіт"),
    ("Зустріч о 15:00", "Високий",  "Зустріч о 15:00"),
])
def test_parametrize_create_task_text(text, priority, expected_text):
    """Крок 2: parametrize — create_task зберігає / обрізає текст правильно."""
    task = create_task(text, priority)
    assert task is not None
    assert task["text"] == expected_text
    assert task["priority"] == priority
    assert task["done"] is False


@mark.parametrize("indices,remaining_texts", [
    ([0],    ["Б", "В"]),
    ([1],    ["А", "В"]),
    ([0, 2], ["Б"]),
])
def test_parametrize_delete_indices(indices, remaining_texts):
    """Крок 2: parametrize — delete_tasks_by_indices залишає правильні елементи."""
    tasks = [
        {"text": "А", "priority": "Низький",  "done": False},
        {"text": "Б", "priority": "Середній", "done": False},
        {"text": "В", "priority": "Високий",  "done": False},
    ]
    result = delete_tasks_by_indices(tasks, indices)
    texts = [t["text"] for t in result]
    assert texts == remaining_texts


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 3  —  pytest.raises
# ══════════════════════════════════════════════════════════════════════════════

def test_raises_index_error_on_invalid_index(sample_tasks):
    """Крок 3: звернення до неіснуючого індексу викидає IndexError."""
    with raises(IndexError):
        toggle_done(sample_tasks, 999)


def test_raises_index_error_on_delete_out_of_range():
    """Крок 3: видалення за індексом поза межами викидає IndexError."""
    tasks = [{"text": "X", "priority": "Середній", "done": False}]
    with raises(IndexError):
        delete_tasks_by_indices(tasks, [5])


def test_raises_type_error_json_non_serializable():
    """Крок 3: save_tasks з не-серіалізованим об'єктом викидає TypeError."""
    import tempfile, os
    bad_tasks = [{"text": object(), "priority": "Низький", "done": False}]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tmp.close()
    try:
        with raises(TypeError):
            save_tasks(bad_tasks, tmp.name)
    finally:
        os.unlink(tmp.name)


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 4  —  @pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════

@mark.skip(reason="UI-функція refresh_list потребує активного tkinter-вікна")
def test_skip_refresh_list_requires_display():
    """Крок 4: цей тест пропускається, бо tkinter недоступний без дисплею."""
    import tkinter as tk
    root = tk.Tk()
    root.mainloop()
    assert False, "Не повинно виконуватись"


@mark.skip(reason="Функція експорту ще не реалізована")
def test_skip_export_to_csv_not_implemented():
    """Крок 4: пропускаємо тест функціоналу, якого ще немає."""
    from task_logic import export_to_csv   # type: ignore  # функція не існує
    export_to_csv([], "/tmp/tasks.csv")


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 5  —  @pytest.mark.xfail
# ══════════════════════════════════════════════════════════════════════════════

@mark.xfail(reason="create_task ще не валідує довжину тексту > 255 символів")
def test_xfail_create_task_rejects_too_long_text():
    """Крок 5: xfail — валідація максимальної довжини ще не реалізована."""
    long_text = "А" * 300
    task = create_task(long_text)
    # Очікуємо None (відмову), але функція цього не перевіряє → провал
    assert task is None, "Занадто довгий текст має відхилятись"


@mark.xfail(reason="Сортування завдань за пріоритетом ще не реалізоване")
def test_xfail_tasks_sorted_by_priority(sample_tasks):
    """Крок 5: xfail — функція сортування ще відсутня."""
    from task_logic import sort_by_priority   # type: ignore  # немає такої функції
    sorted_tasks = sort_by_priority(sample_tasks)
    assert sorted_tasks[0]["priority"] == "Високий"


# ══════════════════════════════════════════════════════════════════════════════
# КРОК 6  —  навмисно зламані тести
# ══════════════════════════════════════════════════════════════════════════════

def test_broken_wrong_text_after_strip():
    """ЗЛАМАНО (крок 6): очікуємо текст з пробілами, але create_task їх обрізає."""
    task = create_task("  Привіт  ")
    # Правильно: task["text"] == "Привіт"
    # Навмисна помилка: порівнюємо з необрізаним рядком
    assert task["text"] == "  Привіт  ", \
        f"Очікувалось '  Привіт  ', отримано '{task['text']}'"


def test_broken_delete_wrong_remaining_count():
    """ЗЛАМАНО (крок 6): після видалення 2 елементів очікуємо 2, але лишається 1."""
    tasks = [
        {"text": "A", "priority": "Низький",  "done": False},
        {"text": "B", "priority": "Середній", "done": False},
        {"text": "C", "priority": "Високий",  "done": False},
    ]
    delete_tasks_by_indices(tasks, [0, 1])
    assert len(tasks) == 2, \
        f"Очікувалось 2 завдання після видалення, залишилось {len(tasks)}"


def test_broken_toggle_expects_unchanged():
    """ЗЛАМАНО (крок 6): після toggle(False) очікуємо False, але стає True."""
    tasks = [{"text": "X", "priority": "Середній", "done": False}]
    toggle_done(tasks, 0)
    assert tasks[0]["done"] is False, \
        "Очікувалось False після toggle, але отримано True"


def test_broken_format_expects_wrong_symbol():
    """ЗЛАМАНО (крок 6): для невиконаного завдання очікуємо ✓ замість ○."""
    task = {"text": "Тест", "priority": "Низький", "done": False}
    label = format_task_label(task)
    assert "✓" in label, \
        f"Очікувався символ ✓ для невиконаного завдання, але label = '{label}'"


# ══════════════════════════════════════════════════════════════════════════════
# Точка входу
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.run()
