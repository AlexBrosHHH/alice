from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    # Extract the user's command from the request data
    command = request.json['request']['command']

    # Extract the topic from the user's command
    topic = request.json['request']['nlu']['entities'][0]['value']

    # Let the user know that the essay is being generated
    response = {
        'response': {
            'text': 'Please wait while I generate an essay on {}...'.format(topic),
            'end_session': False
        },
        'version': request.json['version']
    }

    time.sleep(3)  # Simulate essay generation time

    # Generate the essay text
    essay = generate_essay(topic)

    # Prepare the response data for Alice
    res = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'text': essay,
            'end_session': False
        }
    }

    response.update(res)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
