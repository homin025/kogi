import os

from flask import Flask, request, jsonify

from backend.api import question_generation, review_generation, tale_generation

app = Flask(__name__)


@app.route('/question-generation', methods=['POST'])
def question_generation_api():
    data = request.get_json()

    content = data['content']
    keywords = data['keywords']
    model = data['model']

    result = question_generation.main(content, keywords, model)
    return jsonify(result)


@app.route('/article-summarization', methods=['POST'])
def article_summarization_api():
    data = request.get_json()

    content = data['content']
    model = data['model']
    if data['flag'] == "True":
        flag = True
    else:
        flag = False

    result = tale_generation.main(content, model, flag)
    return jsonify(result)


@app.route('/review-generation', methods=['POST'])
def review_generation_api():
    data = request.get_json()

    content = data['content']
    model = data['model']
    if data['flag'] == "True":
        flag = True
    else:
        flag = False

    result = review_generation.main(content, model, flag)
    return jsonify(result)


@app.route('/tale-generation', methods=['POST'])
def tale_generation_api():
    data = request.get_json()

    content = data['content']
    model = data['model']
    if data['flag'] == "True":
        flag = True
    else:
        flag = False

    result = tale_generation.main(content, model, flag)
    return jsonify(result)


@app.route('/chat-bot', methods=['POST'])
def chat_bot_api():
    data = request.get_json()

    content = data['content']
    model = data['model']

    result = tale_generation.main(content, model)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
