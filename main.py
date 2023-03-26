from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "text": request.json["version"],
        "text": request.json["session"],
        "response": {
            "end_session": False
        }
    }
    
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    if req['request']['original_utterance']:
        ## Проверяем, есть ли содержимое
        res['response']['text'] = req['request']['original_utterance']
    else:
        ## Если это первое сообщение — представляемся
        res['response']['text'] = "Я echo-bot, повторяю за тобой"
    
if __name__ == '__main__':
    app.run()
