import random
import numpy as np

import torch
import gluonnlp
from gluonnlp.data import SentencepieceTokenizer
from transformers import GPT2Config, GPT2LMHeadModel

from backend.api.utils import sample_sequence_sentence, sample_sequence_words


kogpt2_config = {
    "initializer_range": 0.02,
    "layer_norm_epsilon": 1e-05,
    "n_ctx": 1024,
    "n_embd": 768,
    "n_head": 12,
    "n_layer": 12,
    "n_positions": 1024,
    "vocab_size": 50000,
    "activation_function": "gelu"
}


def main(text, model_name):
    """ Independent variables """
    temperature = 0.7
    top_k = 40
    top_p = 0.9

    model_dict = {
        "kogpt2": "./model/kogpt2_model.params",
        "woongjin_books": "./model/kogpt2_tg_woongjin_books_70.ckpt",
        "aesop_fables": "./model/kogpt2_tg_aesop_fables_20.ckpt"
    }

    model_path = model_dict[model_name]

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path=None,
                                            config=GPT2Config.from_dict(kogpt2_config),
                                            state_dict=torch.load(model_path, map_location=device))

    model.to(device)
    model.eval()

    vocab = gluonnlp.vocab.BERTVocab.from_sentencepiece('./model/kogpt2_vocab.spiece',
                                                        mask_token='<msk>',
                                                        sep_token='<sep>',
                                                        cls_token='<cls>',
                                                        unknown_token='<unk>',
                                                        padding_token='<pad>',
                                                        bos_token='<s>',
                                                        eos_token='</s>')

    tokenizer = SentencepieceTokenizer('./model/kogpt2_tokenizer.spiece')

    # 문장진행 텍스트 return
    if flag:
        sentence = sample_sequence_sentence(model, vocab, tokenizer, device, text, temperature, top_p, top_k)
        sentence = sentence.replace("<unused0>", "\n")
        return {'sentence': sentence}
    # 단어진행 리스트 return
    else:
        words = sample_sequence_words(model, vocab, tokenizer, device, text, temperature, top_p, top_k)
        return {'words': words}
