# Участь у розробці Task Manager

Дякуємо за інтерес до проєкту! 🎉  
Цей документ описує, як долучитись до розробки — чи то як користувач, що повідомляє про помилку, чи як розробник, що надсилає код.

---

## Зміст

- [Кодекс поведінки](#кодекс-поведінки)
- [З чого почати](#з-чого-почати)
- [Налаштування середовища розробки](#налаштування-середовища-розробки)
- [Структура проєкту](#структура-проєкту)
- [Робочий процес Git](#робочий-процес-git)
- [Стиль коду](#стиль-коду)
- [Написання тестів](#написання-тестів)
- [Надсилання Pull Request](#надсилання-pull-request)
- [Повідомлення про помилки](#повідомлення-про-помилки)
- [Запит нової функції](#запит-нової-функції)

---

## Кодекс поведінки

Цей проєкт дотримується принципів відкритого та поважного спілкування. Очікується, що всі учасники будуть:

- **Ввічливими** та конструктивними у коментарях та дискусіях
- **Готовими** враховувати різні точки зору
- **Чіткими** у формулюванні проблем і пропозицій

Будь-яка форма образливої поведінки є неприйнятною.

---

## З чого почати

### Якщо ви хочете виправити баг або додати функцію

1. Перевірте список [відкритих Issues](https://github.com/besssty/PRACTICE_task_manager/issues) — можливо, хтось уже працює над цим
2. Якщо Issue не існує — [створіть нове](#повідомлення-про-помилки)
3. Залиште коментар у Issue, що берете завдання в роботу
4. Виконайте кроки з розділу [Налаштування середовища](#налаштування-середовища-розробки)

### Якщо ви хочете поліпшити документацію

Документаційні правки вітаються без Issue — просто створіть PR з описом змін.

---

## Налаштування середовища розробки

### Крок 1 — Форк та клонування

```bash
# Зробіть форк репозиторію через GitHub UI, потім:
git clone https://github.com/<ваш-логін>/PRACTICE_task_manager.git
cd PRACTICE_task_manager
```

### Крок 2 — Перевірте Python

```bash
python --version
# Потрібно Python 3.8 або вище
```

> **Linux:** якщо tkinter не встановлено — `sudo apt-get install python3-tk`

### Крок 3 — Встановіть pytest (опційно, для тестів)

```bash
pip install pytest
```

### Крок 4 — Перевірте, що все працює

```bash
# Запуск unittest-тестів (без зовнішніх залежностей)
python -m unittest test_task_logic -v

# Запуск pytest-тестів
pytest test_pytest_style.py -v
```

Якщо всі тести зелені — середовище налаштовано правильно. ✅

---

## Структура проєкту

```
PRACTICE_task_manager/
│
├── task_manager.py       # GUI: Tkinter-інтерфейс
│                         # ⚠️  Не містить бізнес-логіки — тільки UI
│
├── task_logic.py         # Бізнес-логіка: чисті функції без UI
│                         # ✅  Саме цей модуль покривається тестами
│
├── test_task_logic.py    # Тести: unittest.TestCase
├── test_pytest_style.py  # Тести: pytest (fixture, parametrize тощо)
│
└── tasks.json            # Файл даних (генерується автоматично, не редагувати вручну)
```

### Архітектурний принцип

> **Логіка відокремлена від UI.**

Будь-яка нова функція повинна бути реалізована як чиста функція у `task_logic.py`, а потім підключена до UI у `task_manager.py`. Це забезпечує можливість тестування без запуску вікна.

```
# Правильно:
task_logic.py  ──►  task_manager.py
(чиста логіка)     (тільки UI-виклики)

# Неправильно:
task_manager.py  (логіка змішана з UI)
```

---

## Робочий процес Git

### Іменування гілок

| Тип змін | Формат | Приклад |
|----------|--------|---------|
| Нова функція | `feature/<назва>` | `feature/task-editing` |
| Виправлення бага | `fix/<назва>` | `fix/empty-task-validation` |
| Документація | `docs/<назва>` | `docs/update-readme` |
| Тести | `tests/<назва>` | `tests/add-parametrize` |

### Типовий цикл роботи

```bash
# 1. Синхронізуйтесь з основним репозиторієм
git remote add upstream https://github.com/besssty/PRACTICE_task_manager.git
git fetch upstream
git checkout main
git merge upstream/main

# 2. Створіть нову гілку
git checkout -b feature/task-editing

# 3. Внесіть зміни та зробіть коміти
git add task_logic.py test_task_logic.py
git commit -m "feat: add edit_task() function with validation"

# 4. Запустіть тести перед пушем
python -m unittest test_task_logic -v

# 5. Надішліть гілку
git push origin feature/task-editing

# 6. Відкрийте Pull Request через GitHub UI
```

### Формат повідомлень комітів

Використовуйте [Conventional Commits](https://www.conventionalcommits.org/):

```
<тип>: <короткий опис>

[необов'язкове тіло]
[необов'язкова підказка: closes #N]
```

| Тип | Коли використовувати |
|-----|---------------------|
| `feat` | Нова функція |
| `fix` | Виправлення помилки |
| `docs` | Зміни у документації |
| `test` | Додавання або зміна тестів |
| `refactor` | Рефакторинг без зміни поведінки |
| `chore` | Налаштування, залежності |

**Приклади:**

```bash
git commit -m "feat: add edit_task() to task_logic.py"
git commit -m "fix: reject whitespace-only task text"
git commit -m "test: add parametrize tests for priority values"
git commit -m "docs: update README installation section"
```

---

## Стиль коду

Проєкт дотримується стандарту **PEP 8**. Основні правила:

### Іменування

```python
# ✅ Правильно
def create_task(text, priority="Середній"):
    ...

SAVE_FILE = "tasks.json"   # константи — UPPER_SNAKE_CASE

# ❌ Неправильно
def CreateTask(Text, Priority):
    ...
```

### Рядки документації

Кожна публічна функція у `task_logic.py` повинна мати docstring:

```python
def toggle_done(tasks, index):
    """
    Перемикає статус виконання завдання за індексом.

    Args:
        tasks (list): Список завдань.
        index (int): Індекс завдання у списку.

    Returns:
        list: Оновлений список завдань.

    Raises:
        IndexError: якщо індекс виходить за межі списку.
    """
    tasks[index]["done"] = not tasks[index]["done"]
    return tasks
```

### Валідація введення

```python
# ✅ Завжди перевіряйте .strip() для рядкового вводу
if not text.strip():
    return None

# ❌ Недостатня перевірка
if text == "":
    return None
```

---

## Написання тестів

### Правило: кожна нова функція = мінімум один тест

Якщо ви додаєте функцію до `task_logic.py`, додайте відповідний тест до `test_task_logic.py`.

### Шаблон unittest-тесту

```python
class TestMyFeature(unittest.TestCase):

    def setUp(self):
        """Підготовка даних перед кожним тестом."""
        self.tasks = [
            {"text": "Тест", "priority": "Середній", "done": False}
        ]

    def test_feature_does_expected_thing(self):
        """Короткий опис того, що перевіряється."""
        result = my_function(self.tasks)
        self.assertEqual(result, expected_value)
```

### Шаблон pytest-тесту з fixture та parametrize

```python
import pytest

@pytest.fixture
def sample_tasks():
    return [
        {"text": "А", "priority": "Низький", "done": False},
        {"text": "Б", "priority": "Високий", "done": True},
    ]

@pytest.mark.parametrize("priority,expected", [
    ("Низький", True),
    ("Середній", True),
    ("Високий", True),
])
def test_create_task_accepts_valid_priority(priority, expected):
    task = create_task("Текст", priority)
    assert (task is not None) == expected
```

### Запуск тестів перед PR

```bash
# Усі unittest-тести мають бути зеленими
python -m unittest test_task_logic -v

# Pytest-тести (крім навмисно зламаних)
pytest test_pytest_style.py -v -k "not broken"
```

> **Важливо:** PR не буде прийнято, якщо тести не проходять.

---

## Надсилання Pull Request

### Чекліст перед відкриттям PR

```
[ ] Гілка відгалужена від актуального main
[ ] Код відповідає стилю PEP 8
[ ] Нові функції мають docstring
[ ] Тести додані або оновлені
[ ] Усі тести проходять локально
[ ] Повідомлення комітів відповідають Conventional Commits
```

### Що вказати в описі PR

```markdown
## Що зроблено
Коротко опишіть зміни.

## Пов'язані Issues
Closes #8

## Тип змін
- [ ] Виправлення помилки (fix)
- [ ] Нова функція (feat)
- [ ] Документація (docs)
- [ ] Тести (test)

## Як перевірити
1. Запустіть `python task_manager.py`
2. Двічі клацніть на завдання — відкриється вікно редагування
3. Змініть текст та натисніть «Зберегти»
```

---

## Повідомлення про помилки

Якщо ви знайшли помилку, [відкрийте Issue](https://github.com/besssty/PRACTICE_task_manager/issues/new) та вкажіть:

1. **Опис проблеми** — що відбувається і що мало б відбуватись
2. **Кроки для відтворення** — послідовність дій
3. **Середовище** — ОС, версія Python
4. **Скриншот або лог помилки** (якщо є)

**Приклад гарного звіту:**

```
**Опис:** При введенні тільки пробілів у поле завдання — порожнє завдання додається до списку.

**Кроки:**
1. Запустити task_manager.py
2. Ввести "   " (три пробіли) у поле "Завдання"
3. Натиснути "Додати"

**Очікувано:** Попередження "Введіть текст завдання!"
**Фактично:** Порожнє завдання з'являється у списку

**Середовище:** Windows 11, Python 3.11.2
```

---

## Запит нової функції

Маєте ідею? Чудово! Відкрийте Issue із заголовком `feat: <назва функції>` та опишіть:

- **Що** ви хочете додати
- **Навіщо** це потрібно (який сценарій вирішується)
- **Як** це могло б виглядати або працювати (опціонально)

Активні запити можна знайти тут:
- [Issue #8 — Редагування завдань](https://github.com/besssty/PRACTICE_task_manager/issues/8)
- [Issue #9 — Дедлайни та сортування](https://github.com/besssty/PRACTICE_task_manager/issues/9)

---

<div align="center">

Повернутись до [README.md](README.md)

</div>
