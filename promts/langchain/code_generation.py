"""
Шаблон: code_generation.py
Назначение: Генерация кода с пояснениями
Использование переменных: {variable}
"""

from langchain.prompts import PromptTemplate

template = """## Instruction
Действуй как senior {language} разработчик.

## Task
{task_description}

## Requirements
{requirements_text}

## Constraints
- Код должен быть production-ready
- Добавь комментарии для сложной логики
- Следуй best practices для {language}

## Input
{input_data}

## Output Format
Верни ответ в формате JSON:
```json
{{
  "code": "",
  "explanation": "",
  "complexity": "",
  "tests": []
}}
```

## Examples
**Input:**
Task: Реализуй функцию для вычисления факториала
Requirements: ["Итеративный подход", "Обработка ошибок"]

**Output:**
```json
{{
  "code": "def factorial(n): ...",
  "explanation": "Итеративная реализация с проверкой типа",
  "complexity": "O(n)",
  "tests": ["factorial(5) == 120", "factorial(0) == 1"]
}}
```
"""

prompt = PromptTemplate.from_template(template)

# Пример использования:
# result = prompt.format(
#     language="Python",
#     task_description="Реализуй функцию для вычисления факториала",
#     requirements_text="- Итеративный подход\\n- Обработка ошибок",
#     input_data=""
# )
