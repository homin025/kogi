import os

from flask import Flask, request, jsonify

from backend.api import question_generation, article_summarization, review_generation, tale_generation, chat_bot

app = Flask(__name__)


@app.route('/question-generation', methods=['POST'])
def question_generation_api():
    """ Question Generation API
    Input:
        content(str): 입력 내용
        keywords(list): 키워드 리스트
        model(str): 모델명
    Output:
        questions(list): 생성된 질문 리스트
        answers(list): 생선된 질문의 정답 리스트
    """
    data = request.get_json()

    content = data['content']
    keywords = data['keywords']
    model = data['model']

    result = question_generation.main(content, keywords, model)
    return jsonify(result)


@app.route('/article-summarization', methods=['POST'])
def article_summarization_api():
    """ Article Summarization API
    Input:
        content(str): 입력 내용
        model(str): 모델명
    Output:
        summaries(str): 생성된 요약 문장 리스트
    """
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
    """ Review Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        flag(bool): 문장추천(False) 단어추천(True)
    Output:
        sentence(str): 생성된 문장
        words(list): 생성된 단어 리스트
    """
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
    """ Tale Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        flag(bool): 문장추천(False) 단어추천(True)
    Output:
        sentence(str): 생성된 문장
        words(list): 생성된 단어 리스트
    """
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
    """ Tale Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
    Output:
        sentence(str): 생성된 문장
    """
    data = request.get_json()

    content = data['content']
    model = data['model']

    result = tale_generation.main(content, model)
    return jsonify(result)


if __name__ == '__main__':
    # print(question_generation.main("토끼가 거북이한테 졌어요.", ["토끼", "거북이"], "korquad"))
    # print(article_summarization.main("", "gpt2"))
    # print(tale_generation.main("토끼가", "kogpt2", False))
    # print(review_generation.main("토끼가", "naver_movie", True))
    app.run(host='127.0.0.1', debug=True)
