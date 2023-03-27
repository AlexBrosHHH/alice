from flask import Flask, request, jsonify
import logging
import json
import requests

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"

poluch = False

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
    response_text = ''
    end_session = False

    if "начнём" in command:
        response_text = "Какую тему ты хочешь выбрать для сочинения?"
    elif "сочинение" in command:
        # отправляем запрос к API нейросети
        response_text = "Играем музыку!"
        response = {
            'response': {
                'tts': "<speaker audio='dialogs-upload/439d35b5-5924-4db3-87e3-2ab406bb8683/4c86841e-5318-4c2f-99b7-8b44f6e0596f.opus'>"
            }
        }
        print("Отправил")
        response = requests.post(url, json=payload, headers=headers)
        # обрабатываем ответ от нейросети
        if response.status_code == 200:
            print("получил")
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
