"""
Шаблон: universal_prompt.py
Назначение: Универсальный шаблон для различных задач
Использование переменных: {variable}
"""

from langchain.prompts import PromptTemplate

template = """## Role
{role}

## Task Description
{task_description}

{% if context %}
## Context
{context}
{% endif %}

{% if input_data %}
## Input Data
{input_data}
{% endif %}

## Requirements
{requirements_text}

{% if constraints %}
## Constraints
{constraints_text}
{% endif %}

{% if examples %}
## Examples
{examples_text}
{% endif %}

## Output Format
{output_format}
"""

# Примечание: Условные блоки {% if %} требуют предварительной обработки в Python
# Для полной функциональности используйте Jinja2 или обрабатывайте условия в коде

prompt = PromptTemplate.from_template(template)

# Пример использования:
# result = prompt.format(
#     role="Действуй как эксперт в области физики",
#     task_description="Объясни понятие ускорения",
#     context="Пользователь — начинающий студент",
#     input_data="",
#     requirements_text="- Будь точен\\n- Дай развёрнутый ответ",
#     constraints_text="- Избегай сложных формул",
#     examples_text="Пример 1: ...",
#     output_format="Дай ответ в формате JSON"
# )
