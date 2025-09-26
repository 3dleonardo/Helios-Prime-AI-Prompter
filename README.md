# Helios Prime AI Prompter

Автоматизована система генерації AI промптів на основі аналізу трендів через ComfyUI

## Опис проекту

Helios Prime AI Prompter - це інтелектуальна система для автоматичної генерації високоякісних промптів для AI-генераторів зображень. Система використовує аналіз трендів Google Trends для створення актуальних та популярних тем.

## Основні компоненти

### Custom Nodes для ComfyUI:

- **HeliosFreeCrawler** - збір даних з безкоштовних API (Pexels, Pixabay)
- **HeliosTrendAnalyzer** - аналіз трендів через Google Trends API
- **HeliosPromptGenerator** - генерація промптів на основі трендів
- **HeliosQualityChecker** - перевірка якості промптів
- **HeliosFileWriter** - автоматичний запис результатів з timestamp
- **HeliosKnowledgeBase** - управління базою знань

## Встановлення та запуск

### Передумови:
- Docker
- Python 3.11+
- Git

### Швидкий старт:

1. **Клонувати репозиторій:**
```bash
git clone https://github.com/3dleonardo/Helios-Prime-AI-Prompter.git
cd Helios-Prime-AI-Prompter
```

2. **Запустити ComfyUI:**
```bash
# Побудувати та запустити контейнер
docker build -t helios-comfyui ComfyUI/
docker run -d -p 8188:8188 -v $(pwd)/custom_nodes:/ComfyUI/custom_nodes -v $(pwd)/prompts:/ComfyUI/prompts --name helios-comfyui helios-comfyui
```

3. **Відкрити ComfyUI:**
Перейти на http://localhost:8188

4. **Завантажити workflow:**
Завантажити `helios_free_workflow.json` та запустити

## Архітектура

```
Data Crawling → Trend Analysis → Prompt Generation → Quality Check → File Output
     ↓              ↓              ↓              ↓              ↓
HeliosFreeCrawler → HeliosTrendAnalyzer → HeliosPromptGenerator → HeliosQualityChecker → HeliosFileWriter
```

## Особливості

- ✅ **Безкоштовні API** - використовує Pexels та Pixabay замість платних сервісів
- ✅ **Реальний аналіз трендів** - інтегрується з Google Trends для актуальних тем
- ✅ **Автоматичне збереження** - файли з timestamp для відстеження історії
- ✅ **Модульна архітектура** - легко розширювати новими вузлами
- ✅ **Docker підтримка** - просте розгортання

## Налаштування

### API ключі (опціонально):
- Gemini API key для покращеної генерації промптів
- Pinecone API key для векторної бази знань

### Workflow файли:
- `helios_free_workflow.json` - основний workflow з безкоштовними API
- `helios_workflow.json` - розширений workflow
- `simple_workflow.json` - простий тестовий workflow

## Структура проекту

```
Helios-Prime-AI-Prompter/
├── custom_nodes/           # Кастомні вузли ComfyUI
│   ├── HeliosFreeCrawler/
│   ├── HeliosTrendAnalyzer/
│   ├── HeliosPromptGenerator/
│   ├── HeliosQualityChecker/
│   ├── HeliosFileWriter/
│   └── HeliosKnowledgeBase/
├── ComfyUI/               # Docker образ ComfyUI
├── prompts/               # Згенеровані промпти
├── *.json                 # Workflow файли
└── README.md             # Цей файл
```

## Розробка

Для додавання нових вузлів:
1. Створити папку в `custom_nodes/`
2. Реалізувати клас вузла в `nodes.py`
3. Додати `__init__.py` для імпорту
4. Перезапустити ComfyUI контейнер

## Ліцензія

MIT License - дивіться файл LICENSE

## Автор

[3dleonardo](https://github.com/3dleonardo)