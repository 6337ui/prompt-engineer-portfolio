"""
Шаблон: text_analysis.py
Назначение: Анализ текста (сентимент, ключевые темы, саммари)
Использование переменных: {variable}
"""

from langchain.prompts import PromptTemplate

template = """## Instruction
Действуй как эксперт по анализу текстовых данных.
Проанализируй предоставленный текст по следующим критериям:

## Input Data
Текст для анализа:
```
{text}
```

Язык текста: {language}

## Analysis Requirements
1. Определи тональность текста (позитивная/негативная/нейтральная)
2. Выдели ключевые темы и понятия
3. Определи основную мысль
4. Выяви эмоциональную окраску
5. Определи целевую аудиторию

## Constraints
- Анализируй только предоставленный текст
- Не делай предположений о контексте
- Будь объективен

## Output Format
Верни ответ в формате JSON:
```json
{{
  "sentiment": "positive/negative/neutral",
  "sentiment_score": 0.0,
  "key_topics": [],
  "main_idea": "",
  "emotional_tone": "",
  "target_audience": "",
  "summary": ""
}}
```

## Examples
**Input:**
Текст: "Этот продукт превзошёл все мои ожидания! Качество отличное, доставка быстрая."
Язык: Russian

**Output:**
```json
{{
  "sentiment": "positive",
  "sentiment_score": 0.95,
  "key_topics": ["качество продукта", "доставка", "удовлетворённость"],
  "main_idea": "Клиент крайне доволен покупкой",
  "emotional_tone": "восторженный",
  "target_audience": "потребители",
  "summary": "Положительный отзыв о продукте и доставке"
}}
```
"""

prompt = PromptTemplate.from_template(template)

# Пример использования:
# result = prompt.format(
#     text="Этот продукт превзошёл все мои ожидания!...",
#     language="Russian"
# )
