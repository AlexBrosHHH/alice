from flask import Flask, request
import openai

app = Flask(__name__)

# Здесь необходимо указать свой API-ключ для OpenAI
openai.api_key = "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"

# Это начальный текст, который Алиса отправляет пользователю
START_MESSAGE = "Привет! Я генератор сочинений. Я могу сгенерировать любое сочинение по теме, либо по краткому описанию! Начнем?"

# Это сообщение, которое отправляется пользователю, если не удалось получить ответ от OpenAI
ERROR_MESSAGE = "Извините, произошла ошибка. Попробуйте еще раз."


# Функция, которая генерирует текст на заданную тему с помощью OpenAI
def generate_essay(topic):
    # Модель, которая будет использоваться для генерации текста
    model_engine = "text-davinci-002"

    # Задаем параметры генерации текста
    prompt = f"Напишите сочинение на тему '{topic}'"
    temperature = 0.8
    max_tokens = 2048

    # Генерируем текст с помощью OpenAI API
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred while generating essay: {e}")
        return None


# Функция, которая обрабатывает запросы пользователя
def process_request(user_input):
    if "сгенерируй сочинение" in user_input:
        # Если пользователь хочет сгенерировать сочинение, то запускаем процесс генерации
        topic = request.form["text"]  # Получаем тему из запроса пользователя
        generated_essay = generate_essay(topic)
        if generated_essay:
            return generated_essay
        else:
            return ERROR_MESSAGE
    else:
        # Если пользователь просто написал текст, отвечаем ему с подсказкой
        return "Вы можете запросить сочинение, написав 'сгенерируй сочинение'."


# Функция, которая возвращает начальное сообщение
def get_start_message():
    return START_MESSAGE


# Функция, которая обрабатывает POST-запросы от Яндекс.Диалогов
@app.route("/", methods=["POST"])
def handle_dialog():
    # Получаем данные от Яндекс.Диалогов
    request_data = request.json
    # Получаем текст, написанный пользователем
    user_input = request_data["request"]["command"]
    # Отвечаем пользователю
    response = {
        "response": {
            "text": process_request(user_input),
            "end_session": False
        },
        "version": request_data["version"]
    }
    return response
