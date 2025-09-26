# Детальний План Стеку AI-Агентів через ComfyUI для Генерації 100 Унікальних Image-Prompts

**Головний висновок:**
Цей стек із п’яти спеціалізованих AI-агентів, реалізований в ComfyUI, забезпечує автоматичний збір трендових зображень із фотостоків, глибокий аналіз, створення 100 актуальних, не повторюваних промптів та формування знаньних баз із рекомендаціями Google. Кожен промпт записується в текстовий файл з іменем у форматі YYYY-MM-DD.txt.

***

## 1. Функції Агентів

1. **Crawler Agent**
    - Пошук і парсинг популярних та нішевих фотостоків (Unsplash, Shutterstock, Adobe Stock тощо)
    - Витяг назви, теги, кількість завантажень, аналіз конкурентності
2. **Trend Analyzer Agent**
    - Обробка зібраних метаданих: обчислення трендів за обсягом пошуків (Google Trends API), соціальними сигналами (Pinterest, Instagram хештеги)
    - Оцінка перспективності та конкуренції кожної теми
3. **Prompt Generator Agent**
    - Використовує LLM (Ollama/Gemini) з RAG: підтягує релевантні приклади з internal Dataset DB
    - Генерує 100 промптів за сесію, дотримуючись рекомендацій Google (тезове формулювання, чіткі стилі, позитивні формати)
    - Перевіряє унікальність проти історії (Vector DB в Pinecone) та виключає дублікати
    - Має вибір між Gemini або Ollama для LLM залежно від конфігурації
4. **Quality Checker Agent**
    - Автоматичне оцінювання сформованих промптів за критеріями: релевантність, креативність, насиченість деталей
    - Фільтрація некоректних або занадто загальних формулювань
5. **File Writer Agent**
    - Створює текстовий файл із назвою `YYYY-MM-DD.txt`
    - Записує по одному промпту на рядок у хронологічному порядку
    - Зберігає файл у хмарному сховищі (S3/GCS) або локально

***

## 2. ComfyUI-Workflow зі Нодами

ComfyUI - це візуальний інструмент для створення workflow генерації зображень на основі Stable Diffusion та інших моделей. Для реалізації стеку AI-агентів ми використаємо custom nodes (розширення), які дозволять інтегрувати API виклики, LLM, бази даних та інші функції. Це включає встановлення ComfyUI Manager для управління custom nodes та створення власних вузлів на Python.

### 2.1 Початковий Тригер

- **Manual Trigger або Scheduler Node**: Для щоденного запуску о 02:00 використовуйте custom scheduler node (наприклад, на основі APScheduler). Альтернативно, запускайте вручну через веб-інтерфейс ComfyUI.
- **Set Variable Node**: Збереження `currentDate` у форматі YYYY-MM-DD за допомогою custom node з datetime.

### 2.2 Crawler Agent Workflow

1. **Custom HTTP Request Node**: Виклики API фотостоків (Unsplash, Shutterstock) з використанням requests library у Python. Вузол приймає URL, headers (наприклад, Authorization для Unsplash), parameters (query, per_page).
2. **Custom HTML Parser Node**: Якщо API обмежене, парсинг сторінок за допомогою BeautifulSoup. Витягає title, tags, downloads, competition.
3. **Data Aggregation Node**: Збереження масиву `{ title, tags, downloads, competition }` у JSON або list format для передачі далі.

### 2.3 Trend Analyzer Workflow

1. **Custom Google Trends Node**: Виклик Google Trends API (або scraping) для отримання індексів популярності. Використовуйте pytrends library у custom node.
2. **Math/Function Node**: Обчислення score = `popularity / competition` за допомогою Python expressions.
3. **Sort/Filter Node**: Сортування за `score` → топ N тем. Використовуйте built-in list operations або custom node.

### 2.4 Prompt Generator Workflow

1. **Custom RAG Node**: Пошук релевантних прикладів у Vector DB (Pinecone) за допомогою pinecone-client у custom node. Приймає query, повертає embeddings.
2. **Custom AI Text Generation Node**: Запит LLM (Gemini або Ollama) з шаблоном. Використовуйте google-generativeai або requests для Ollama. Шаблон: «Створити детальний image-prompt для фотостоку на тему {{topic}} з стилем {{style}}…».
3. **Merge Arrays Node**: Поєднання 100 згенерованих промптів у масив.
4. **Custom Deduplication Node**: Перевірка через Vector DB на подібність (>90% cosine) з використанням cosine similarity у Python.

### 2.5 Quality Checker Workflow

1. **Custom Metrics Node**: Обчислення метрик (length, keyword density) за допомогою text analysis у Python.
2. **Custom AI Moderation Node**: Перевірка тональності та відповідності рекомендаціям Google через додатковий LLM виклик або rule-based.
3. **Conditional Filter Node**: Відфільтровує <95% quality → повернути на доопрацювання. Використовуйте if-else logic у custom node.

### 2.6 File Writer Workflow

1. **Set Filename Node**: Іменування файла як `{{currentDate}}.txt`.
2. **Split Batches Node**: Поодинокі промпти з масиву.
3. **Custom Write File Node**: Запис рядок за рядком до файлу з використанням Python file I/O.
4. **Custom S3/GCS Upload Node**: Збереження файла в облако з boto3 або google-cloud-storage.

### 2.7 Knowledge Base Update

- **Custom Database Node**: Вставка нових прикладів до Postgres/Firestore з psycopg2 або firebase-admin. Оновлення embedding’ів у Vector DB.
- **Custom Git Node**: Commit змін у `datasets-prompt-library.md` з gitpython library.

***

## 3. Roadmap Реалізації

| Етап | Термін | Опис |
| :-- | :-- | :-- |
| 1. Налаштування ComfyUI | 2 дні | Встановлення ComfyUI через git clone, Docker Compose для баз даних (Postgres, Pinecone), встановлення ComfyUI Manager, додавання custom nodes для HTTP requests, LLM API, файлів та баз даних |
| 2. Implement Crawler Agent | 4 дні | Створення custom HTTP Request та HTML Parser nodes, тестування API фотостоків (Unsplash тощо), збереження даних у масив |
| 3. Trend Analyzer | 3 дні | Створення custom Google Trends node з pytrends, функційна оцінка score, сортування тем |
| 4. Prompt Generator | 1 тиждень | Створення custom RAG node для Pinecone, AI Text Generation node для Gemini/Ollama, генерація 100 промптів з дедуплікацією |
| 5. Quality Checker | 3 дні | Створення custom Metrics та AI Moderation nodes, фільтрація якості |
| 6. File Writer | 2 дні | Створення custom Write File та S3/GCS Upload nodes, запис промптів до файлу |
| 7. Knowledge Base | 4 дні | Створення custom Database та Git nodes, оновлення embedding’ів та commit змін |
| 8. Тестування та Валідація | 1 тиждень | Інтеграційні тести workflow, перевірка унікальності, edge-case scenarios у ComfyUI |
| 9. Моніторинг та Алерти | 3 дні | Створення custom Error Workflow node для Slack/Email алертів, дашборд метрик |
| 10. Документація | 2 дні | Опис custom nodes, інструкції по розгортанню ComfyUI, рекомендації Google |
| **Загальна тривалість** | **~6 тижнів** | До production-ready MVP |


***

**Цей план гарантує автоматизацію збору і аналізу трендів, генерацію 100 унікальних, актуальних image-prompts та централізоване управління через ComfyUI з custom nodes з урахуванням рекомендацій Google.**

***

## 4. Поточний Статус та Рекомендації

### 4.1 Поточний Статус Реалізації
- **Завершено**: Агент Генератора Промптів (Prompt Generator Agent) реалізований з використанням Google Gemini, із webhook-тригером, багатостадійними викликами LLM для напрямків/стратегій/насіння, дедуплікацією, фільтрацією якості та записом бінарного файлу.
- **Ключові Сильні Сторони**:
  - Комплексний Workflow: Охоплює введення теми, ланцюжок LLM (Архітектор → Аналітик → Стратегія → Генерація), семантичну дедуплікацію, оцінку якості та бінарний вивід файлу.
  - Конфігурабельність: Підтримує власні теми/кількості через параметри webhook; використовує змінні середовища для API-ключів.
  - Стійкість до Помилок: Логіка повторів, ignoreResponseCode=true для збоїв API.
  - Якість Виводу: Генерує різноманітні, високоякісні промпти (наприклад, 24 промпти на "topic" із різними тонами/стилями).
- **Відповідність Плану**: Реалізовано Агента Генератора Промптів та Агента Записувача Файлів. Стадія Roadmap: Завершено Prompt Generator (1 тиждень); частково Quality Checker (інтегровано у вузол Post Process).

### 4.2 Рекомендації для Покращення
1. **Додати Cron Тригер**: Реалізувати щоденні запуски о 02:00 як у плані (Cron Node + Schedule Trigger) для автоматизації генерації.
2. **Покращити Обробку Помилок**: Додати вузли Error Trigger для повторів/запасних варіантів; логувати збої до бази даних або Slack.
3. **Інтегрувати Інші Агенти**:
   - **Crawler Agent**: Додати вузли HTTP Request для API фотостоків (наприклад, Unsplash API) для збору трендів.
   - **Trend Analyzer**: Використати вузол Google Trends API для оцінок популярності; обчислити score = популярність / конкуренція.
   - **Quality Checker**: Розширити Post Process вузлом AI Moderation для перевірок тону/релевантності; фільтрувати <95% якості.
4. **Зберігання та Масштабованість**: Перемістити вивід файлів до S3/GCS (Додати S3 Node) для хмарного зберігання; зберігати промпти у Postgres для історії/дедуплікації між запусками.
5. **Безпека та Автентифікація**: Для продакшену додати API-ключ автентифікації до webhook (опції вузла Webhook); забезпечити відсутність чутливих даних у логах.
6. **Моніторинг**: Додати ComfyUI Error Workflow для сповіщень; відстежувати метрики (наприклад, кількість промптів, використання API) у дашборді.
7. **Продуктивність**: Для 100 промптів оптимізувати виклики LLM (пакетні запити, якщо можливо); додати кешування для насіння/напрямків.
8. **Тестування**: Додати unit-тести для вузлів Function; валідувати унікальність проти Vector DB (Pinecone) як у плані.
9. **Документація**: Оновити README діаграмами workflow, кінцевими точками API та відповідністю рекомендаціям Google.
10. **Вибір LLM**: Реалізувати вибір між Gemini або Ollama через конфігураційні змінні або вузли Switch, щоб користувач міг обирати backend залежно від потреб (Gemini для швидкості, Ollama для локальної приватності).

Поточне налаштування є міцним MVP для Генератора Промптів. Продовжуйте реалізацію решти агентів за 6-тижневим roadmap для досягнення повної автоматизації.

