from flask import Flask, Response, request, jsonify
# from flask_cors import CORS

from api import question_generation, article_summarization, review_generation, tale_generation, chat_bot


app = Flask(__name__)
# cors = CORS(app, resource={r'/api/*': {'origin': '*'}})


@app.route('/api/question-generation', methods=['POST'])
def question_generation_api():
    """ Question Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        keywords(list): 키워드 리스트
        sentence_length(int): 출력 문장 길이

    Output:
        questions(list): 생성된 질문 리스트
        answers(list): 생선된 질문의 정답 리스트
    """
    
    data = request.get_json()

    content = data['content']
    model = data['model']
    temperature = float(data['temperature'])
    top_k = int(data['top_k'])
    top_p = float(data['top_p'])

    keywords = data['keywords']
    sentence_length = data['sentence_length']

    result = question_generation.main(content, model, temperature, top_k, top_p, keywords, sentence_length)
    return jsonify(result)


@app.route('/api/article-summarization', methods=['POST', 'OPTIONS'])
def article_summarization_api():
    """ Article Summarization API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        sentence_length(int): 출력 문장 길이
        sentence_count(int): 출력 문장 수

    Output:
        summary(str): 생성된 요약 문장 리스트
    """

    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()
        print(data)

        content = data['content']
        model = data['model']
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])

        sentence_length = data['sentence_length']
        sentence_count = data['sentence_count']

        result = article_summarization.main(content, model, temperature, top_k, top_p, sentence_length, sentence_count)

        response.set_data(json.dumps(result))

    return response


@app.route('/api/review-generation', methods=['POST'])
def review_generation_api():
    """ Review Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        sentence_length(int): 출력 문장 길이
        word_count(int): 출력 단어 수
        flag(str): 문장추천(True) / 단어추천(False)

    Output:
        sentence(str): 생성된 문장
        words(list): 생성된 단어 리스트
    """

    data = request.get_json()

    content = data['content']
    model = data['model']
    temperature = float(data['temperature'])
    top_k = int(data['top_k'])
    top_p = float(data['top_p'])

    if data['flag'] == "True":
        flag = True
    else:
        flag = False

    if flag:
        sentence_length = int(data['length'])
    else:
        word_count = int(data['count'])

    result = review_generation.main(content, model, temperature, top_k, top_p, flag, sentence_length, word_count)
    return jsonify(result)


@app.route('/api/tale-generation', methods=['POST'])
def tale_generation_api():
    """ Tale Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        length(int): 출력 문장 길이
        count(int): 출력 단어 수
        flag(str): 문장추천(True) / 단어추천(False)

    Output:
        sentence(str): 생성된 문장
        words(list): 생성된 단어 리스트
    """

    data = request.get_json()

    content = data['content']
    model = data['model']
    temperature = float(data['temperature'])
    top_k = int(data['top_k'])
    top_p = float(data['top_p'])

    if data['flag'] == "True":
        flag = True
    else:
        flag = False

    if flag:
        sentence_length = int(data['length'])
    else:
        word_count = int(data['count'])

    result = tale_generation.main(content, model, temperature, top_k, top_p, flag, sentence_length, word_count)
    return jsonify(result)


@app.route('/api/chat-bot', methods=['POST'])
def chat_bot_api():
    """ Chat Bot API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

    Output:
        sentence(str): 생성된 문장
    """

    data = request.get_json()

    content = data['content']
    model = data['model']
    temperature = float(data['temperature'])
    top_k = int(data['top_k'])
    top_p = float(data['top_p'])

    result = chat_bot.main(content, model, temperature, top_k, top_p)
    return jsonify(result)


import json


@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test_api():
    data = request.get_json()

    result = Response()

    result.headers.add('Access-Control-Allow-Origin', "*")
    result.headers.add('Access-Control-Allow-Headers', "*")
    result.set_data(json.dumps({"body": "확인"}))

    return result


if __name__ == '__main__':
    app.run(host='localhost', port=8888, debug=True)
