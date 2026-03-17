# Руководство по Prompt Engineering: Шаблоны и Ручное Составление

Комплексное руководство по созданию эффективных промптов для больших языковых моделей (LLM). Охватывает как ручное написание инструкций, так и использование шаблонизаторов для автоматизации.

---

## Часть 1. Ручное составление промптов

### 1.1. Структура промпта

Хороший промпт состоит из логических блоков, которые помогают модели понять задачу:

```markdown
## Instruction
Краткое описание роли и задачи модели

## Context
Контекст или предыстория задачи

## Input Data
Входные данные для обработки

## Constraints
Ограничения и требования

## Output Format
Требуемый формат ответа

## Examples
Примеры входных данных и ожидаемых ответов (few-shot)
```

### 1.2. Элементы ручного промпта

| Элемент | Синтаксис | Назначение | Пример |
|---------|-----------|------------|--------|
| Заголовок раздела | `## ...` или `### ...` | Разделение логических блоков | `## Instruction` |
| Плейсхолдер для ручной подстановки | `[NAME]` | Место для вставки значения | `[Field]`, `[UserName]` |
| Подсказка в плейсхолдере | `[Field, e.g., "Physics"]` | Пример ожидаемого значения | `[Date, e.g., "2025-07-18"]` |
| Список требований | `-` или `1.` | Перечисление шагов или условий | `- Проанализируй текст` |
| Кодовый блок | ` ``` ` | Сохранение форматирования (JSON, YAML, код) | ` ```json {...} ``` ` |
| Формат вывода | Явная JSON-маска | Структура ожидаемого ответа | `{ "answer": "" }` |

### 1.3. Примеры значений для плейсхолдеров

| Плейсхолдер | Тип данных | Примеры значений |
|-------------|------------|------------------|
| `[Field]` | строка-категория | `Physics`, `Prompt Engineering`, `UX Design` |
| `[Response]` | произвольный текст | `"The acceleration of…"`, `"Этот промпт показывает…"` |
| `[UserName]` | строка (имя) | `Ivan Petrov`, `@vibe-coder` |
| `[Date]` | дата | `2025-07-18`, `18 июля 2025` |
| `[Action]` | глагол (повелительное) | `Сделай X`, `Напиши обзор` |

### 1.4. Пример ручного промпта

```markdown
## Instruction
Действуй как эксперт в указанной области. Проанализируй предоставленный ответ и дай оценку.

## Context
Пользователь получил ответ на свой вопрос и хочет понять его качество.

## Input Data
Expertise: [Field, e.g., "Physics"]
Response to evaluate: [Response text for evaluation]
User: [UserName]
Date: [Date]

## Constraints
- Будь объективен и конкретен
- Указывай на фактические ошибки, если они есть
- Предлагай улучшения

## Output Format
```json
{
  "field": "",
  "strengths": [],
  "weaknesses": [],
  "score": 0,
  "recommendations": []
}
```

## Examples
**Input:**
Expertise: Physics
Response: "Acceleration is the rate of change of velocity with respect to time."

**Output:**
```json
{
  "field": "Physics",
  "strengths": ["Точное определение", "Корректная терминология"],
  "weaknesses": [],
  "score": 5,
  "recommendations": ["Можно добавить формулу a = Δv/Δt"]
}
```
```

---

## Часть 2. Шаблоны с автоматической подстановкой

### 2.1. Нотации переменных

В шаблонах используются разные синтаксисы для переменных-плейсхолдеров:

| Нотация | Синтаксис | Где используется | Пример |
|---------|-----------|------------------|--------|
| Одинарные скобки | `{variable}` | LangChain, Python `str.format()` | `Tell me about {topic}` |
| Двойные скобки | `{{variable}}` | Jinja2, Handlebars, PromptFlow | `Hello, {{ name }}!` |
| Квадратные скобки | `[VARIABLE]` | Ручные шаблоны, документация | `[Field]` |
| ERB/Razor-стиль | `<%= variable %>` | Редко, в некоторых JS-фреймворках | `<%= user_name %>` |

### 2.2. Движки шаблонов

#### LangChain (Python) — одинарные скобки `{}`

```python
from langchain.prompts import PromptTemplate

template = """You are an assistant. Answer the question: {question}"""
prompt = PromptTemplate.from_template(template)
print(prompt.format(question="What is the capital of France?"))
# Вывод: "You are an assistant. Answer the question: What is the capital of France?"
```

**Особенности:**
- Простая подстановка по имени переменной
- Несколько переменных: `"User {name} from {city} asks: {query}"`
- Нет встроенной поддержки условий/циклов (требуется код Python)
- Экранирование: `{{` выводит `{`, `}}` выводит `}`

#### Jinja2 — двойные скобки `{{}}` + теги `{%%}`

```jinja2
Hello {{ user_name }}, welcome to {{ service_name }}.

{% if user_type == 'premium' %}
Hello, premium user!
{% else %}
Hello, valued user!
{% endif %}

{% for item in todo_list %}
- {{ item }}
{% endfor %}
```

**Особенности:**
- Поддержка условий: `{% if ... %}...{% else %}...{% endif %}`
- Поддержка циклов: `{% for item in collection %}...{% endfor %}`
- Фильтры: `{{ name|title }}`, `{{ list|join(', ') }}`, `{{ value|round(2) }}`
- Комментарии: `{# это комментарий #}`
- Raw-блоки: `{% raw %}{{ не интерполируется }}{% endraw %}`

#### Handlebars / Microsoft Guidance — `{{}}` + блочные теги

```handlebars
{{#system~}}
You are a concise assistant.
{{~/system}}

{{! Это комментарий — не попадёт в промпт }}
{{#user~}}
Question: {{query}}
Context: {{ get_context_from_db query }}
{{~/user}}

{{#assistant~}}
{{gen 'answer' max_tokens=200}}
{{~/assistant}}
```

**Особенности:**
- Условия: `{{#if condition}}...{{else}}...{{/if}}`
- Циклы: `{{#each list}}- {{this}}{{/each}}`
- Роли чата: `{{#system}}...{{/system}}`, `{{#user}}...{{/user}}`
- Генерация: `{{gen 'variable'}}`, выбор: `{{select 'var' options=[...]}}`
- Комментарии: `{{! комментарий }}` или `{{!-- многострочный --}}`

### 2.3. Управляющие конструкции

#### Условия

**Jinja2:**
```jinja2
{% if user_level == 'beginner' %}
Объясняй просто, с примерами.
{% elif user_level == 'advanced' %}
Используй техническую терминологию.
{% else %}
Дай сбалансированный ответ.
{% endif %}
```

**Handlebars/Guidance:**
```handlebars
{{#if is_premium}}
Hello, premium user!
{{else}}
Hello, valued user!
{{/if}}
```

#### Циклы

**Jinja2:**
```jinja2
{% for product in purchases %}
- {{ product|upper }}
{% endfor %}
```

**Handlebars/Guidance:**
```handlebars
{{#each policy_list}}
- {{this}}
{{/each}}
```

#### Фильтры и форматирование

| Фильтр | Описание | Пример |
|--------|----------|--------|
| `|title` | Заглавные буквы | `{{ name|title }}` → `John Doe` |
| `|upper` / `|lower` | Верхний/нижний регистр | `{{ text|upper }}` |
| `|join(', ')` | Объединение списка | `{{ items|join(', ') }}` |
| `|round(n)` | Округление | `{{ value|round(2) }}` |
| `|length` | Длина | `{{ list|length }}` |

**Python-форматирование (LangChain):**
```python
template = "Price: ${price:.2f}"  # Форматирование числа
template = "Items: {items}"       # Простая подстановка
```

### 2.4. Экранирование спецсимволов

| Символ | Jinja2 | LangChain/Python | Handlebars |
|--------|--------|------------------|------------|
| `{` | `{{ '{{' }}` | `{{` | `{{ '{{' }}` |
| `}` | `{{ '}}' }}` | `}}` | `{{ '}}' }}` |
| Блок кода | `{% raw %}...{% endraw %}` | `{{` и `}}` удваиваются | `{{! }}` или raw-хелпер |

**Пример (Jinja2):**
```jinja2
{# Выводим фигурные скобки буквально #}
Используй синтаксис: {{ '{{' }}variable{{ '}}' }}

{# Или целый блок кода #}
{% raw %}
{{ this_will_not_be_interpolated }}
{% endraw %}
```

### 2.5. Комментарии и аннотации

| Тип | Jinja2 | Handlebars/Guidance | LangChain |
|-----|--------|---------------------|-----------|
| Комментарий | `{# текст #}` | `{{! текст }}` | Нет (только в коде) |
| Многострочный | `{# ... #}` | `{{!-- ... --}}` | Нет |
| Аннотация роли | Нет | `{{#system}}...{{/system}}` | Нет |

**Пример с комментариями (Jinja2):**
```jinja2
{# Основная инструкция #}
Действуй как эксперт в {{ field }}.

{% for step in steps %}
- {{ step }}  {# Вывод каждого шага #}
{% endfor %}
```

**Пример с аннотациями ролей (Guidance):**
```handlebars
{{#system~}}
You are a helpful coding assistant.
{{~/system}}

{{#user~}}
{{query}}
{{~/user}}

{{#assistant~}}
{{gen 'response' max_tokens=500}}
{{~/assistant}}
```

---

## Часть 3. Соглашения об именовании

### 3.1. Стили именования переменных

| Стиль | Пример | Где рекомендуется |
|-------|--------|-------------------|
| `snake_case` | `customer_query`, `user_name` | **Рекомендуется** (Jinja2, LangChain, PromptFlow) |
| `camelCase` | `customerQuery`, `userName` | JavaScript/TypeScript интеграции |
| `PascalCase` | `CustomerQuery` | Не рекомендуется для переменных |

### 3.2. Правила именования

✅ **Делайте:**
- Используйте говорящие имена: `customer_location` вместо `loc`
- Пишите на английском языке
- Используйте `snake_case` для консистентности
- Начинайте с маленькой буквы

❌ **Избегайте:**
- Пробелов в именах: `user name` → `user_name`
- Спецсимволов: `user-name`, `user.name` → `user_name`
- Смешения стилей: `userName` и `user_address` в одном шаблоне
- Опечаток — шаблон чувствителен к регистру и написанию

### 3.3. Примеры хороших имён

```jinja2
{# ✅ Хорошо #}
{{ customer_name }}
{{ shipping_method }}
{{ order_total }}
{{ user_query }}

{# ❌ Плохо #}
{{ cn }}           {# Непонятно #}
{{ CustomerName }} {# PascalCase #}
{{ user-name }}    {# Дефис #}
```

---

## Часть 4. Комплексные примеры

### 4.1. Шаблон для оценки ответов (Jinja2)

```jinja2
{# Шаблон: evaluation_prompt.jinja2 #}
## Instruction
Действуй как эксперт в области {{ field|title }}.
Оцени предоставленный ответ по критериям точности, полноты и ясности.

## Context
Пользователь: {{ user_name }}
Дата: {{ evaluation_date }}
{% if user_level == 'beginner' %}
Уровень пользователя: начинающий. Объясняй просто.
{% elif user_level == 'advanced' %}
Уровень пользователя: продвинутый. Используй терминологию.
{% endif %}

## Input Data
Вопрос: {{ user_question }}
Ответ для оценки: {{ response_text }}

## Constraints
- Будь объективен и конкретен
{%- for constraint in additional_constraints %}
- {{ constraint }}
{%- endfor %}

## Output Format
```json
{
  "field": "{{ field }}",
  "user": "{{ user_name }}",
  "evaluation": {
    "accuracy": 0,
    "completeness": 0,
    "clarity": 0
  },
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "overall_score": 0
}
```

{# Пример использования в Python:
from jinja2 import Template
template = Template(prompt_template)
result = template.render(
    field="Physics",
    user_name="Ivan Petrov",
    user_level="beginner",
    user_question="Что такое ускорение?",
    response_text="Ускорение — это изменение скорости со временем.",
    evaluation_date="2025-07-18",
    additional_constraints=["Избегай сложных формул", "Приведи пример"]
)
#}
```

### 4.2. Шаблон для чат-бота (Handlebars/Guidance)

```handlebars
{{#system~}}
Ты — полезный ассистент компании {{ company_name }}.
Твоя задача: помогать клиентам с вопросами о {{ service_type }}.

{% if has_premium_support %}
Для премиум-клиентов предоставляй расширенную поддержку.
{% endif %}
{{~/system}}

{{! Получаем контекст из базы знаний }}
{{#user~}}
{{customer_query}}

История обращений:
{{#each previous_tickets}}
- {{this.date}}: {{this.summary}} (статус: {{this.status}})
{{/each}}
{{~/user}}

{{#assistant~}}
{{gen 'response' max_tokens=300 temperature=0.7}}

{# Сохраняем ответ для аналитики #}
{{set 'ticket_response' response}}
{{~/assistant}}
```

### 4.3. Шаблон для генерации кода (LangChain)

```python
from langchain.prompts import PromptTemplate

template = """## Instruction
Действуй как senior {{ language }} разработчик.

## Task
{task_description}

## Requirements
{%- for requirement in requirements %}
- {requirement}
{%- endfor %}

## Constraints
- Код должен быть production-ready
- Добавь комментарии для сложной логики
- Следуй best practices для {language}

## Input
{input_data}

## Output Format
Верни ответ в формате JSON:
```json
{{{{
  "code": "",
  "explanation": "",
  "complexity": "",
  "tests": []
}}}}
```

## Examples
**Input:**
Task: Реализуй функцию для вычисления факториала
Requirements: ["Итеративный подход", "Обработка ошибок"]

**Output:**
```json
{{{{
  "code": "def factorial(n): ...",
  "explanation": "Итеративная реализация с проверкой типа",
  "complexity": "O(n)",
  "tests": ["factorial(5) == 120", "factorial(0) == 1"]
}}}}
```
"""

prompt = PromptTemplate.from_template(template)
# Обратите внимание: {{{{ выводит {{ в итоговом промпте
```

### 4.4. Универсальный шаблон (комбинирует оба подхода)

```jinja2
{# 
  Универсальный шаблон промпта
  Сочетает ручную структуру и автоматическую подстановку
#}

## Role
{% if role_custom %}
{{ role_custom }}
{% else %}
Действуй как эксперт в области {{ expertise_field|default("общие знания", true)|title }}
{% endif %}

## Task Description
{{ task_description }}

{% if context %}
## Context
{{ context }}
{% endif %}

{% if input_data %}
## Input Data
{{ input_data }}
{% endif %}

## Requirements
{%- for requirement in requirements|default(["Будь точен", "Дай развёрнутый ответ"], true) %}
- {{ requirement }}
{%- endfor %}

{% if constraints %}
## Constraints
{%- for constraint in constraints %}
- {{ constraint }}
{%- endfor %}
{% endif %}

{% if examples %}
## Examples
{%- for example in examples %}
### Example {{ loop.index }}
**Input:** {{ example.input }}
**Output:** {{ example.output }}
{% endfor %}
{% endif %}

## Output Format
{% if output_format %}
{{ output_format }}
{% else %}
Дай развёрнутый ответ в свободной форме.
{% endif %}

{# Мета-информация (не попадает в промпт модели) #}
{# 
  Переменные шаблона:
  - role_custom: кастомная роль (опционально)
  - expertise_field: область экспертизы
  - task_description: описание задачи
  - context: контекст (опционально)
  - input_data: входные данные
  - requirements: список требований
  - constraints: ограничения
  - examples: примеры few-shot обучения
  - output_format: формат вывода
#}
```

---

## Часть 5. Best Practices

### 5.1. Для ручных промптов

| Практика | Описание |
|----------|----------|
| **Структурируй** | Разделяй промпт на логические блоки с заголовками |
| **Будь конкретен** | Избегай двусмысленностей в инструкциях |
| **Показывай формат** | Явно указывай ожидаемый формат ответа (JSON, список, текст) |
| **Добавляй примеры** | Few-shot примеры улучшают качество ответов |
| **Тестируй итеративно** | Улучшай промпт на основе результатов |

### 5.2. Для шаблонов

| Практика | Описание |
|----------|----------|
| **Используй snake_case** | Консистентность имён упрощает поддержку |
| **Документируй переменные** | Добавляй комментарии к сложным шаблонам |
| **Экранируй правильно** | `{{ '{{' }}` для вывода фигурных скобок |
| **Валидируй входные данные** | Проверяй наличие всех переменных перед рендерингом |
| **Модульность** | Разбивай сложные шаблоны на части (partials) |

### 5.3. Общие рекомендации

1. **Начинай с простого** — сначала базовый промпт, потом усложняй
2. **Тестируй на краевых случаях** — пустые значения, специальные символы
3. **Версионируй шаблоны** — отслеживай изменения промптов
4. **Логируй вход/выход** — для отладки и анализа качества
5. **A/B тестируй варианты** — сравнивай разные формулировки

---

## Приложение A. Быстрая справка

### Синтаксис переменных

```
{var}           # LangChain, Python format
{{var}}         # Jinja2, Handlebars
[VARIABLE]      # Ручные шаблоны
```

### Условия

```jinja2
{# Jinja2 #}
{% if condition %}...{% else %}...{% endif %}

{# Handlebars #}
{{#if condition}}...{{else}}...{{/if}}
```

### Циклы

```jinja2
{# Jinja2 #}
{% for item in list %}{{ item }}{% endfor %}

{# Handlebars #}
{{#each list}}{{this}}{{/each}}
```

### Комментарии

```jinja2
{# Jinja2 #}
{# комментарий #}

{# Handlebars #}
{{! комментарий }}
{{!-- многострочный --}}
```

### Фильтры (Jinja2)

```jinja2
{{ name|title }}      # Заглавные буквы
{{ text|upper }}      # Верхний регистр
{{ list|join(', ') }} # Объединение
{{ value|round(2) }}  # Округление
{{ item|default('N/A') }} # Значение по умолчанию
```

---

## Приложение B. Сравнение движков

| Функция | LangChain | Jinja2 | Handlebars/Guidance |
|---------|-----------|--------|---------------------|
| Переменные | `{var}` | `{{var}}` | `{{var}}` |
| Условия | ❌ (только в коде) | ✅ `{% if %}` | ✅ `{{#if}}` |
| Циклы | ❌ (только в коде) | ✅ `{% for %}` | ✅ `{{#each}}` |
| Фильтры | Python format | ✅ богатый набор | ⚠️ ограниченный |
| Комментарии | ❌ | ✅ `{# #}` | ✅ `{{! }}` |
| Роли чата | ⚠️ вручную | ❌ | ✅ `{{#system}}` |
| Генерация LLM | ⚠️ через API | ❌ | ✅ `{{gen}}` |
| Сложность | Низкая | Средняя | Средняя |
| Экосистема | Python | Универсальный | Microsoft |

---

*Документ составлен на основе: promt-1.md, promt-2.md*  
*Версия: 1.0 | Дата: 2025-07-18*
