from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "text": request.json["or"],
        "text": request.json["Hello"],
        "response": {
            "end_session": False
        }
    }

    req = request.json
    if req["session"]["new"]:
        response["response"]["text"] = "Привет! Как твои дела? Как отметил новый год?"
    else:
        if req["request"]["original_utterance"].lower() in ["хорошо", "отлично"]:
            response["response"]["text"] = "Супер! Я за вас рада!"
        elif req["request"]["original_utterance"].lower() in ["плохо", "скучно"]:
            response["response"]["text"] = "Это печально... нужно было позвать меня!"

    return json.dumps(response)
