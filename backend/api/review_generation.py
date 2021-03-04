import random
import numpy as np

import torch

from .util import sample_sequence_sentence, sample_sequence_words, sample_sequence_paragraph


def main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, recommend_flag, auto_flag, count):
    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    model.load_state_dict(torch.load(model_file, map_location=device))

    model.to(device)
    model.eval()

    # 자동완성 문단 return
    if auto_flag:
        paragraph = sample_sequence_paragraph(model, tokenizer, device, content, temperature, top_k, top_p, count)
        return {'paragraph': paragraph}
    # 문장추천 텍스트 return
    elif recommend_flag:
        sentences = sample_sequence_sentence(model, tokenizer, device, content, temperature, top_k, top_p, count)
        return {'sentences': sentences, 'words': []}
    # 단어추천 리스트 return
    else:
        words = sample_sequence_words(model, tokenizer, device, content, temperature, top_k, top_p, count)
        return {'words': words, 'sentences': []}
