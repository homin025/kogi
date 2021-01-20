import json

import torch
from tokenizers import SentencePieceBPETokenizer
from transformers import GPT2LMHeadModel

from flask import Flask, Response, request, jsonify
# from flask_cors import CORS

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
        sentence_count(int): 출력 문장 수

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
        sentence_count = data['sentence_count']

        result = article_summarization.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, sentence_length, sentence_count)

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


@app.route('/api/tale-generation', methods=['POST', 'OPTIONS'])
def tale_generation_api():
    """ Tale Generation API
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
        model_file = config.TGConfig().model_dict[data['model']]
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

        result = tale_generation.main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, sentence_count, word_count)

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


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available else "cpu")
    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path="taeminlee/kogpt2")
    tokenizer = SentencePieceBPETokenizer.from_file(
        vocab_filename='./tokenizer/kogpt2_vocab.json',
        merges_filename='./tokenizer/kogpt2_merges.txt',
        add_prefix_space=False
    )

    temperature = 1.0
    top_k = 40
    top_p = 0.9

    content = "한나라당 홍준표, 민주당 원혜영, 선진과 창조의 모임 문국현 원내대표는 이날 국회 귀빈식당에서 원내대표 회담을 두 차례 열어 미디어 관계 법안 등 쟁점 법안의 처리 방안에 대한 10개 " \
              "항에 합의했다. 여야는 이견이 없는 민생법안 등 100여 건을 이번 임시국회에서 협의 처리하되 아직 상임위원회에 상정되지 않았거나 심의를 거치지 못한 법안은 9일 다시 임시국회를 열어 " \
              "처리하기로 했다. 그러나 여야는 이날 합의에서 상당수 쟁점법안의 처리 시기는 물론이고 법안 상정 여부조차 정하지 못해 2월 1일 열리는 임시국회에서 이를 둘러싼 ‘제2차 입법전쟁’이 " \
              "벌어질 가능성이 높다. 여야는 최대 쟁점이었던 미디어 관계 법안 8건 중 언론중재법 등 여야 간 이견이 없는 법안 2건만 이번 임시국회에서 협의 처리하고 신문·방송 겸영 허용과 대기업 " \
              "방송 진출 허용 등 여야가 맞서는 6개 법안은 이른 시일 안에 합의 처리하도록 노력하기로 했다. 한미 자유무역협정(FTA) 비준동의안은 미국 차기 행정부가 출범(이달 20일)한 뒤 " \
              "이른 시일 안에 협의 처리하기로 했다. 출자총액제한제도 폐지 법안은 이번 임시국회에서 상임위원회에 상정하되 2월 임시국회에서 협의 처리하고 금산분리 완화 법안 역시 이번 임시국회에서 " \
              "상정하되 여야가 합의 처리하도록 노력하기로 했다. 재외국민에게 대선과 총선의 투표권을 부여하는 내용의 공직선거법 개정안은 여야 동수로 정치개혁특별위원회를 구성해 2월 임시국회에서 합의 " \
              "처리하기로 했다. 이에 앞서 민주당은 이날 오전 국회 본회의장과 행정안전위, 정무위 회의장 점거 농성을 풀었다. 민주당은 7일엔 문화체육관광방송통신위 회의장에서 철수하기로 했다. " \
              "김형오 국회의장은 6일 질서유지권 발동을 해제했다. "
    keywords = ["제2차 입법전쟁", "임시국회"]

    # print(question_generation.main(content, model, tokenizer, device, "./model/kogpt2_qg_korquad_30.ckpt", temperature, top_k, top_p, keywords, 100))

    # print(article_summarization.main(content, "korean", temperature, top_k, top_p, 100, 3))
    # (content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, sentence_count, word_count)
    print(tale_generation.main("사람들이 하늘을 바라보며 말했어요. 와 하늘이", model, tokenizer, device, "./model/kogpt2_tg_woongjin_15.ckpt", temperature, top_k, top_p, True, True, 3, 3))

    # print(review_generation.main("이 동화책은 생각보다 ", "naver_movie", True))
