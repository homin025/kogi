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
    """ Question Generation API related to Kogi
    Input:
        content(str): Input text
        model(str): Name of model
        temperature(float): Temperature value
        top_k(int): Top K value
        top_p(float): Top P value

        keywords(list): List of keywords

    Output:
        questions(list): List of generated questions
        answers(list): List of answers for generated questions
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

        result = question_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, keywords)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/article-summarization', methods=['POST', 'OPTIONS'])
def article_summarization_api():
    """ Article Summarization API related to Kogi
    Input:
        content(str): Input text
        model(str): Name of model
        temperature(float): Temperature value
        top_k(int): Top K value
        top_p(float): Top P value

        sentence_length(int): Length limit of generation

    Output:
        summary(str): Generated summary
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
    """ Tale Generation API related to Kogi
    Input:
        content(str): Input text
        model(str): Name of model
        temperature(float): Temperature value
        top_k(int): Top K value
        top_p(float): Top P value

        count(int): How many outputs to be provided
        recommend_flag(bool): Text generation of [True for sentence / False for word]
        auto_flag(bool): Auto generation if [True for on / False for off]

    Output:
        sentences(list): List of generated sentences
        words(list): List of generated words
        paragraph(str): Auto-generated paragraph
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
    """ Review Generation API related to Kogi
    Input:
        content(str): Input text
        model(str): Name of model
        temperature(float): Temperature value
        top_k(int): Top K value
        top_p(float): Top P value

        count(int): How many outputs to be provided
        recommend_flag(bool): Text generation of [True for sentence / False for word]
        auto_flag(bool): Auto generation if [True for on / False for off]

    Output:
        sentences(list): List of generated sentences
        words(list): List of generated words
        paragraph(str): Auto-generated paragraph
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
        count = int(data['count'])

        result = review_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, count)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/chat-bot', methods=['POST', 'OPTIONS'])
def chat_bot_api():
    """ Chat Bot API related to Kogi
    Input:
        content(str): Input text
        model(str): Name of model
        temperature(float): Temperature value
        top_k(int): Top K value
        top_p(float): Top P value

    Output:
        sentence(str): Generated sentence
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
def get_example_api():
    """ Get Example API related to Kogi
    This API loads example from MySQL.
    Input:
        testID(str): Name of API
        index(int): Index of example

    Output:
        content(str): Content of example
        Question Generation -> keyword(str): Keywords
        Article Summarization -> summary(str): Summary
        Tale Generattion ->
        Review Generation ->
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



@app.route('/api/load-article')
def load_article_api():
    """ Load Article API related to Kogi
    This API loads content of news article from url of Naver news.
    Input:
        content(str): Input url

    Output:
        body(str): Content of news
        summary(str): Summary of news
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

        result = article_summarization.load_article_from_url(content)

        response.set_data(json.dumps(result, ensure_ascii=False))

    return response


@app.route('/api/save-post', methods=['POST', 'OPTIONS'])
def save_post():
    """ Save Post API related to Cornor of Book
    Input:
        id(str): ID of card
        body(str): Content of card
        img(int): Index of image

    Output:
        content(str): Content of example
        Question Generation -> keyword(str): Keywords
        Article Summarization -> summary(str): Summary
        Tale Generattion ->
        Review Generation ->
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'POST':
        response.headers.add("Access-Control-Allow-Origin", "*")

        data = request.get_json()

        _id = data['id']
        _body = "'" + data['body'] + "'"
        _img = "'" + data['img'] + "'"

        sql = 'INSERT INTO list (body, img) VALUES(' + _body +', ' + _img + ')'

        connection = pymysql.connect(
            host='localhost',
            user='woongjin',
            passwd='1029',
            db='cob',
            charset='utf8'
        )

        result = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            print('inserting data into database succeeds')
        except:
            print('inserting data into database fails')

    return response


@app.route('/api/load-post', methods=['GET', 'OPTIONS'])
def load_post():
    """ Load Post API related to Cornor of Book
    Input:
        None

    Output:
        content(str): Content of example
        Question Generation -> keyword(str): Keywords
        Article Summarization -> summary(str): Summary
        Tale Generattion ->
        Review Generation ->
    """
    response = Response()

    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST")

    elif request.method == 'GET':
        response.headers.add("Access-Control-Allow-Origin", "*")

        sql = 'INSERT INTO list (body, img) VALUES(' + _body +', ' + _img + ')'

        connection = pymysql.connect(
            host='localhost',
            user='woongjin',
            passwd='1029',
            db='cob',
            charset='utf8'
        )

        result = None
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM list order by list.date DESC;'
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            print('inserting data into database succeeds')
        except:
            print('inserting data into database fails')

        cards = []
        for card in result:
            cards.append({'id': card[0], 'body': card[1], 'img': card[2], date: card[3].strftime('%d %b, %H:%M')})
        
        response.set_data(json.dumps({'cards': cards}))

    return response


@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test_api():
    result = Response()

    result.headers.add('Access-Control-Allow-Origin', "*")
    result.headers.add('Access-Control-Allow-Headers', "*")
    result.set_data(json.dumps({"body": "TEST"}))

    return result


if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available else "cpu")

    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path="taeminlee/kogpt2")

    tokenizer = SentencePieceBPETokenizer.from_file(
        vocab_filename='./tokenizer/tokenizers_vocab.json',
        merges_filename='./tokenizer/tokenizers_merges.txt',
        add_prefix_space=False
    )

    app.run(host='localhost', port=9999, debug=True)
