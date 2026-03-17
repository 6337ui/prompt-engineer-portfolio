# Готовые шаблоны промптов

Папка содержит готовые шаблоны для Jinja2 и LangChain на основе примеров из README.

## Структура

```
promts/
├── jinja2/          # Шаблоны Jinja2 с расширенным синтаксисом
│   ├── evaluation_prompt.jinja2    # Оценка качества ответов
│   ├── universal_prompt.jinja2     # Универсальный шаблон
│   ├── code_generation.jinja2      # Генерация кода
│   └── chat_assistant.jinja2       # Чат-бот с контекстом
│
└── langchain/       # Шаблоны LangChain для Python
    ├── evaluation_prompt.py        # Оценка качества ответов
    ├── code_generation.py          # Генерация кода
    ├── universal_prompt.py         # Универсальный шаблон
    └── text_analysis.py            # Анализ текста
```

## Использование

### Jinja2

```python
from jinja2 import Template

# Загрузка шаблона
with open('promts/jinja2/evaluation_prompt.jinja2', 'r') as f:
    template = Template(f.read())

# Рендеринг
result = template.render(
    field="Physics",
    user_name="Ivan Petrov",
    user_level="beginner",
    user_question="Что такое ускорение?",
    response_text="Ускорение — это изменение скорости со временем.",
    evaluation_date="2025-07-18",
    additional_constraints=["Избегай сложных формул", "Приведи пример"]
)
```

### LangChain

```python
from langchain.prompts import PromptTemplate

# Импорт готового шаблона
from promts.langchain.evaluation_prompt import prompt

# Использование
result = prompt.format(
    field="Physics",
    user_name="Ivan Petrov",
    user_level="beginner",
    user_question="Что такое ускорение?",
    response_text="Ускорение — это изменение скорости со временем.",
    evaluation_date="2025-07-18"
)
```

## Описание шаблонов

| Шаблон | Назначение | Ключевые переменные |
|--------|-----------|---------------------|
| `evaluation_prompt` | Оценка качества ответов | `field`, `user_name`, `response_text`, `user_level` |
| `universal_prompt` | Универсальный шаблон | `role`, `task_description`, `requirements`, `constraints` |
| `code_generation` | Генерация кода | `language`, `task_description`, `requirements` |
| `chat_assistant` | Чат-бот с историей | `company_name`, `customer_query`, `previous_tickets` |
| `text_analysis` | Анализ текста | `text`, `language` |

## Особенности

### Jinja2 шаблоны
- Поддержка условий: `{% if %}...{% endif %}`
- Поддержка циклов: `{% for %}...{% endfor %}`
- Фильтры: `{{ variable|title }}`, `{{ variable|default("value") }}`
- Комментарии: `{# комментарий #}`

### LangChain шаблоны
- Простая подстановка: `{variable}`
- Для экранирования `{` и `}` используйте `{{` и `}}`
- Условия и циклы требуют обработки в Python
