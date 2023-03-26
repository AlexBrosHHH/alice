from flask import Flask, request
import logging
import json

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["POST"])
def main():
    data = request.json
    command = data.get('request', {}).get('command', '')

    end_session = False

    response_text = 'Привет! Ты здесь впервые?'

    if "да" in command:
        response_text = "Я могу тебе помочь составить мини-сочинение на любую тему. Тебе нужно сказать про что должно быть сочинение и я его тебе напишу."
    elif "нет" in command:
        response_text = "Скажи тему сочинение или опиши про что оно должно быть."

    response = {
        'response': {
            'text': response_text,
            'end_session ': end_session
        },
        'version': '1.0'
    }
    return response
