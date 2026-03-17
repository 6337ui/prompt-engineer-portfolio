"""
Шаблон: evaluation_prompt.py
Назначение: Оценка качества ответов экспертом
Использование переменных: {variable}
"""

from langchain.prompts import PromptTemplate

template = """## Instruction
Действуй как эксперт в области {field}.
Оцени предоставленный ответ по критериям точности, полноты и ясности.

## Context
Пользователь: {user_name}
Дата: {evaluation_date}
Уровень пользователя: {user_level}

## Input Data
Вопрос: {user_question}
Ответ для оценки: {response_text}

## Constraints
- Будь объективен и конкретен
- Указывай на фактические ошибки, если они есть
- Предлагай улучшения

## Output Format
Верни ответ в формате JSON:
```json
{{
  "field": "",
  "user": "",
  "evaluation": {{
    "accuracy": 0,
    "completeness": 0,
    "clarity": 0
  }},
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "overall_score": 0
}}
```

## Examples
**Input:**
Expertise: Physics
Response: "Acceleration is the rate of change of velocity with respect to time."

**Output:**
```json
{{
  "field": "Physics",
  "user": "Ivan Petrov",
  "evaluation": {{
    "accuracy": 5,
    "completeness": 4,
    "clarity": 5
  }},
  "strengths": ["Точное определение", "Корректная терминология"],
  "weaknesses": [],
  "recommendations": ["Можно добавить формулу a = Δv/Δt"]
}}
```
"""

prompt = PromptTemplate.from_template(template)

# Пример использования:
# result = prompt.format(
#     field="Physics",
#     user_name="Ivan Petrov",
#     user_level="beginner",
#     user_question="Что такое ускорение?",
#     response_text="Ускорение — это изменение скорости со временем.",
#     evaluation_date="2025-07-18"
# )
