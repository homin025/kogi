import time
import random
import requests
import numpy as np

import torch

from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display


def main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, sentence_length):
    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    model.load_state_dict(torch.load(model_file, map_location=device))

    model.to(device)
    model.eval()

    bos_token = tokenizer.token_to_id("<s>")
    eos_token = tokenizer.token_to_id("</s>")
    task_token = tokenizer.encode("요약:").ids

    context_tokens = tokenizer.encode(f"문맥:{content}").ids

    len_input_ids = 1 + len(context_tokens) + len(task_token)

    if len_input_ids >= 1000:
        len_available = len_input_ids - 1000
        context_tokens = context_tokens[len_available:]

    input_ids = [bos_token] + context_tokens + task_token
    len_input_ids = len(input_ids)
    input_ids = torch.tensor([input_ids]).cuda()
    attention_mask = torch.tensor([[1.0] * len_input_ids]).cuda()

    model.to(device)
    input_ids.to(device)
    attention_mask.to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_masks=attention_mask,
        max_length=len_input_ids+sentence_length,
        min_length=len_input_ids,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        num_return_sequences=1,
    )

    output_tokens = output.tolist()[0]
    generated_summary = tokenizer.decode(output_tokens[len_input_ids:])
    generated_summary = generated_summary.split("</s>")[:3]
    generated_summary = ''.join(generated_summary).replace("<s>", "")

    return {"summary": generated_summary}

def load_article_from_url(url):
    if not url.startswith('https://news.naver.com'):
        return {"body": 'This is not an url from Naver news'}

    re = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(re.text, 'html.parser')
    news = html.find('meta', property='me2:category1')['content']
    body = clean_body(html.select_one('#articleBodyContents'), news)
    summary = load_summary_from_url(url)

    return {"body": body, "summary": summary}

def load_summary_from_url(url):
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    time.sleep(2)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
    driver.get(url)

    try:
        driver.find_element_by_xpath('//a[@class="media_end_head_autosummary_button _toggle_btn nclicks(sum_summary)"]').click()

        time.sleep(1)

        summary = driver.find_element_by_xpath('//div[@class="_contents_body"]')
        body = clean_summary(summary.text)
    except:
        body = "This article does not support Naver Summary Bot."
        pass
    finally:
        driver.quit()

    display.stop()

    return body

def clean_body(body, news):
    result = ""
    for item in body.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<","/"]:
            result += str(item).strip()

    result.replace("&apos;", "")
    result = result[11:]

    # Case 1: 앞은 ']' 까지 자르고 뒤은 마지막 '다.' 이후 자르기
    case1 = ['이데일리','미디어오늘','프레시안','경향신문','머니투데이','서울경제','아시아경제','헤럴드경제','더팩트','미디어오늘','아이뉴스24','오마이뉴스','디지털데일리','디지털타임스','블로터']

    # Case 2: 처음에 있는 '= ' 까지 자르기
    case2 = ['뉴시스','연합뉴스','뉴스1']

    # Case 3: 앞에  '】 ' 있으면 '】 ' 까지 자르고 뒤은 마지막 '다.' 이후 자르기
    case3 = ['파이낸셜뉴스']

    # Case 4: YTN - ※ '당신의 제보가 뉴스가 됩니다' YTN은 여러분의 소중한 제보를 기다립니다. 가 있으면 먼저 자르고 마지막 '다.' 이후 자르기
    case4 = ['YTN']

    start = 0
    end = -1
    if news in case1:
        start = result.find(']')
        end = result.rfind('다.')
    elif news in case2:
        start = result.find('= ') + 1
        end = result.rfind('다.')
    elif news in case3:
        start = result.find('】') + 1
        end = result.rfind('다.')
    elif news in case4:
        flag = result.find('※ ')
        if not flag == -1:
            result = result[:flag]
        end = result.rfind('다.')
    else:
        if result.startswith('('):
            start = result.find(')')
        elif result.startswith('['):
            start = result.find(']')
        end = result.rfind('다.')

    if start == 0:
        result = result[:end+2]
    else:
        result = result[start+1:end+2]
    
    return result

def clean_summary(text):
    result = text.replace("\n\n", " ")

    return result