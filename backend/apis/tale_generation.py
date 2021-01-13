import random
import numpy as np

import torch
import torch.nn.functional as F
import gluonnlp
from gluonnlp.data import SentencepieceTokenizer
from transformers import GPT2Config, GPT2LMHeadModel


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


def top_k_logits(logits, k):
    if k == 0:
        return logits
    values, _ = torch.topk(logits, k)
    min_values = values[:, -1]
    return torch.where(logits < min_values, torch.ones_like(logits, dtype=logits.dtype) * -1e10, logits)


def top_p_logits(logits, top_p=0.0, filter_value=-float('Inf')):
    """Nucleus sampling"""
    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs >= top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[:, indices_to_remove] = filter_value
    return logits


def sample_sequence(model, vocab, tokenizer, device, text, length, temperature, top_p, top_k):
    tokenized = tokenizer(text)  # 받은 문장

    generated_text = ''
    generated_length = 0

    """ START: Customization for sampling is optional """
    while True:
        input = torch.tensor([vocab[vocab.bos_token], ] + vocab[tokenized]).unsqueeze(0)
        input = input.to(device)

        predicts = model(input)
        pred = predicts[0]

        # temperature applying
        logits = pred
        logits = logits[:, -1, :] / temperature

        # top k sampling
        logits = top_k_logits(logits, top_k)

        # top p sampling
        logits = top_p_logits(logits, top_p)

        # probabilities
        log_probs = F.softmax(logits, dim=-1)

        prev = torch.multinomial(log_probs, num_samples=1)

        generated = vocab.to_tokens(prev.squeeze().tolist())

        if generated == '</s>' or generated_length > length:
            text += generated.replace('▁', ' ')
            text += '\n'
            generated_text += generated.replace('▁', ' ')
            generated_text += '\n'
            break

        text += generated.replace('▁', ' ')
        generated_text += generated.replace('▁', ' ')
        generated_length += 1

        tokenized = tokenizer(text)
    """ END: Customization for sampling is optional """

    return text.replace('</s>', '.')


def main(text, model='kogpt2', flag=False):
    length = 250
    temperature = 0.7
    top_k = 40
    top_p = 0.9

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path=None,
                                            config=GPT2Config.from_dict(kogpt2_config),
                                            state_dict=torch.load('./models/kogpt2_model.params'))

    model.to(device)
    model.eval()

    vocab = gluonnlp.vocab.BERTVocab.from_sentencepiece('./models/kogpt2_vocab.spiece',
                                                        mask_token='<msk>',
                                                        sep_token='<sep>',
                                                        cls_token='<cls>',
                                                        unknown_token='<unk>',
                                                        padding_token='<pad>',
                                                        bos_token='<s>',
                                                        eos_token='</s>')

    tokenizer = SentencepieceTokenizer('./models/kogpt2_tokenizer.spiece')

    sentence = sample_sequence(model, vocab, tokenizer, device, text, length, temperature, top_p, top_k)
    sentence = sentence.replace("<unused0>", "\n")

    return {'content': sentence}
