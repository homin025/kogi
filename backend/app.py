import json

import torch
from tokenizers import SentencePieceBPETokenizer
from transformers import GPT2LMHeadModel

from flask import Flask, Response, request, jsonify
# from flask_cors import CORS

import pymysql

from api import question_generation, article_summarization, review_generation, tale_generation, chat_bot, config

app = Flask(__name__)
# cors = CORS(app, resource={r'/api/*': {'origin': '*'}})


@app.route('/api/question-generation', methods=['POST', 'OPTIONS'])
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
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        content = data['content']
        model_file = config.QGConfig().model_dict[data['model']]
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])

        keywords = data['keywords']
        sentence_length = int(data['sentence_length'])

        result = question_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, keywords, sentence_length)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


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

    Output:
        summary(str): 생성된 요약 본문
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        content = data['content']
        model_file = config.ASConfig().model_dict[data['model']]
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])

        sentence_length = data['sentence_length']

        result = article_summarization.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, sentence_length)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/tale-generation', methods=['POST', 'OPTIONS'])
def tale_generation_api():
    """ Tale Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        count(int): 출력 문장 / 단어 수
        recommend_flag(bool): 문장추천(True) / 단어추천(False)
        auto_flag(bool): 자동완성 ON(True) / OFF(False)

    Output:
        sentences(str): 생성된 문장 리스트
        words(list): 생성된 단어 리스트
        paragraph(str): 자동완성된 문단
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        content = data['content']
        model_file = config.TGConfig().model_dict[data['model']]
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])
        recommend_flag = data['recommend_flag']
        auto_flag = data['auto_flag']
        count = int(data['count'])

        result = tale_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, count)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/review-generation', methods=['POST', 'OPTIONS'])
def review_generation_api():
    """ Review Generation API
    Input:
        content(str): 입력 내용
        model(str): 모델명
        temperature(float): 온도 값
        top_k(int): top_k 값
        top_p(float): top_p 값

        sentence_count(int): 출력 문장 수
        word_count(int): 출력 단어 수
        recommend_flag(bool): 문장추천(True) / 단어추천(False)
        auto_flag(bool): 자동완성 ON(True) / OFF(False)

    Output:
        sentence(str): 생성된 문장
        words(list): 생성된 단어 리스트
        paragraph(str): 자동완성된 문단
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        content = data['content']
        model_file = config.RGConfig().model_dict[data['model']]
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])
        recommend_flag = data['recommend_flag']
        auto_flag = data['auto_flag']

        if recommend_flag:
            sentence_count = int(data['sentence_count'])
            word_count = 0
        else:
            word_count = int(data['word_count'])
            sentence_count = 0

        result = review_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, sentence_count, word_count)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/chat-bot', methods=['POST', 'OPTIONS'])
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
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        content = data['content']
        model_file = config.CBConfig().model_dict[data['model']]
        temperature = float(data['temperature'])
        top_k = int(data['top_k'])
        top_p = float(data['top_p'])

        result = chat_bot.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/get-example', methods=['POST', 'OPTIONS'])
def get_data_api():
    """ Get Example API
    Input:
        testID(str): API 이름
        index(int): 데이터 순서

    Output:
        content(str): 데이터 본문
        질문생성 keyword(str): 데이터 키워드
        기사요약 summary(str): 데이터 요약
        리뷰생성
        동화창작
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        textID = data['textID']
        index = data['index']

        connection = pymysql.connect(
            host='localhost',
            user='woongjin',
            passwd='1029',
            db='kogi',
            charset='utf8'
        )

        if textID == 'QuestionGeneration':
            result = None
            try:
                with connection.cursor() as cursor:
                    sql = 'SELECT * FROM question where id =' + str(index)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                print('loading data from database succeeds')
            except:
                print('loading data from database fails')

            if result:
                content = result[0][2]
                keyword = result[0][3].split(',')
            else:
                content = ""
                keyword = [""]

            response.set_data(json.dumps({'content': content, 'keyword': keyword}))

        elif textID == 'ArticleSummarization':
            result = None
            try:
                with connection.cursor() as cursor:
                    sql = 'SELECT * FROM summary where id =' + str(index)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                print('loading data from database succeeds')
            except:
                print('loading data from database fails')

            if result:
                content = result[0][2]
                summary = result[0][4]
            else:
                content = ""
                summary = ""

            response.set_data(json.dumps({'content': content, 'summary': summary}))

        # elif textID == 'TaleGeneration':

        # elif textID == 'ReviewGeneration':

    return response


@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test_api():
    result = Response()

    result.headers.add('Access-Control-Allow-Origin', "*")
    result.headers.add('Access-Control-Allow-Headers', "*")
    result.set_data(json.dumps({"body": "TEST"}))

    return result


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available else "cpu")
    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path="taeminlee/kogpt2")
    tokenizer = SentencePieceBPETokenizer.from_file(
        vocab_filename='./tokenizer/kogpt2_vocab.json',
        merges_filename='./tokenizer/kogpt2_merges.txt',
        add_prefix_space=False
    )

    app.run(host='localhost', port=9999, debug=True)
