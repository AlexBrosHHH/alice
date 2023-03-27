from flask import Flask, request, jsonify
from alice_scripts import Skill, request, say, suggest
#import logging
#import json
import requests

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"

payload = {
    "enable_google_results": False,
    "enable_memory": False,
    "input_text": "Кто такой дональд трамп кратко."
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": "315f79b7-8037-4e1c-a35d-bf255c6bfd24"
}

@app.route("/", methods=["POST"])
def main():
    data = request.json
    command = data.get('request', {}).get('command', '')
    end_session = False

    if "начнём" in command:
        response_text = "Какую тему ты хочешь выбрать для сочинения?"
    elif "описание" in command:
        response_text = "Какое краткое описание твоего сочинения?"
    elif "сочинение" in command:
        # отправляем запрос к API нейросети
        yield say(<speaker audio="dialogs-upload/439d35b5-5924-4db3-87e3-2ab406bb8683/4c86841e-5318-4c2f-99b7-8b44f6e0596f.opus">)
        response = requests.post(url, json=payload, headers=headers)
        # обрабатываем ответ от нейросети
        if response.status_code == 200:
            response_text = "Всё готово."
            response_text = response.json().get('data', {}).get('text', '')
            print("Получил")
        else:
            response_text = "Что-то пошло не так при генерации сочинения."
            print(response.status_code)
        end_session = True

    response = {
        'response': {
            'text': response_text,
            'end_session': end_session,
        },
        'version': '1.0'
    }
    return response
