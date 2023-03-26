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
        response_text = "Я генератор сочинений. Я могу сгенерировать любое сочинение по теме, либо по краткому описанию! Начнем?"
        if "начнём" in command:
            response_text = "*переход к сочинителю!*"
    elif "нет" in command:
        response_text = "*переход к сочинителю!*"

    response = {
        'response': {
            'text': response_text,
            'end_session ': end_session,
        },
        'version': '1.0'
    }
    return response
