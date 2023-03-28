почему в яндекс диалогах выдаёт ошибку "1. недопустимый ответ "

import json
import logging
import requests
#from random import randint

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)
url = "https://api.writesonic.com/v2/business/content/ai-article-writer-v2?engine=average&language=ru&num_copies=1"
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": "315f79b7-8037-4e1c-a35d-bf255c6bfd24"
            }
# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)

    logging.info('Response: %r', response)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    user_id = req['session']['application']['application_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "спорт",
                "технологии",
                "наука",
                "здоровье",
                "природа",
                "начнём",
            ]
        }
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        res['response'][
            'text'] = 'Привет! Я генератор сочинений. Я могу сгенерировать любое сочинение по теме, либо по краткому описанию! Начнем?'
        res['response']['buttons'] = get_suggests(user_id)
        return
    try:
        if req['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь', 'что ты можешь',
                                                            'что ты умеешь?', 'что ты можешь?', 'кто ты',
                                                            'зачем ты нужен', 'зачем тебя создали']:
            res['response'][
                'text'] = 'Я расскажу тебе свежую новость, нужно только выбрать одну из категорий: спорт, наука, природа, технологии, здоровье' # Вставить текст ПОМОЩЬ
            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['да', 'хочу', 'конечно', 'ага', 'валяй', 'рассказывай',
                                                        'слушаю', 'очень', 'весь внимание']:
            res['response']['text'] = 'Выбери одну из категорий: спорт, наука, природа, технологии, здоровье'
            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in [
            'спорт',
            'природа',
            'технологии',
            'здоровье',
            'наука',
        ]:
            text = req['request']['original_utterance'].lower()
            print(text)
            response = requests.post(url, headers=headers)
    except:
        if response.status_code == 200:
            res['response']['text'] = response.json()["data"][0]["output"]
            res['response']['buttons'] = get_suggests(user_id)
        else:
            raise Exception("Ошибка при получении ответа от внешнего сервиса")
        res['response']['buttons'] = get_suggests(user_id)

def get_start_suggest(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session["suggests"][5]
    ]
    return suggests
# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:4]
    ]
    return suggests
