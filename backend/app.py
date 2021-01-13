import os

from flask import Flask, request, jsonify

from backend.apis import tale_generation

app = Flask(__name__)


@app.route('/', methods=['POST'])
def tale_generation_api():
    data = request.get_json()
    text = data['content']
    result = tale_generation.main(text)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
