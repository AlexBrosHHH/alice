from flask import Flask, request, jsonify
import logging
import json
import requests

app = Flask(__main__)

#logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["POST"])
def main():
    data = request.json
    command = data.get('request', {}).get('command', '')
    response_text = ''
    end_session = False

    if "начнём" in command:
        response_text = "Какую тему ты хочешь выбрать для сочинения?"
    elif "описание" in command:
        response_text = "Какое краткое описание твоего сочинения?"
    elif "сочинение" in command:
        # отправляем запрос к API нейросети
        response = requests.post('https://api.writesonic.com/v1/writesonic/gpt3/generate',
                                 json={"prompt": command, "temperature": 0.5},
                                 headers={"Authorization": "315f79b7-8037-4e1c-a35d-bf255c6bfd24"})
        # обрабатываем ответ от нейросети
        if response.status_code == 200:
            response_text = response.json().get('data', {}).get('text', '')
        else:
            response_text = "Что-то пошло не так при генерации сочинения."
        end_session = True

    response = {
        'response': {
            'text': response_text,
            'end_session': end_session,
        },
        'version': '1.0'
    }
    return jsonify(response)
