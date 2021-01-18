import random
import numpy as np

import torch
from transformers import GPT2LMHeadModel
from tokenizers import SentencePieceBPETokenizer

from .config import ASConfig


def main(content, model_name, temperature, top_k, top_p, sentence_length, sentence_count):
    config = ASConfig()

    model_dict = config.model_dict

    model_file = model_dict[model_name]

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = torch.device("cpu")

    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path="taeminlee/kogpt2",
                                            state_dict=torch.load(model_file, map_location=device))

    model.to(device)
    model.eval()

    tokenizer = SentencePieceBPETokenizer.from_file(
        vocab_filename='./model/kogpt2_vocab.json',
        merges_filename='./model/kogpt2_merges.txt',
        add_prefix_space=False
    )

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
    input_ids = torch.LongTensor([input_ids])
    attention_mask = torch.LongTensor([[1.0] * len_input_ids])

    model.to(device)
    input_ids.to(device)
    attention_mask.to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_masks=attention_mask,
        max_length=len_input_ids+250,
        min_length=len_input_ids+5,
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
    generated_summary = generated_summary.split("</s>")[0].replace("<s>", "")

    return {"summary": generated_summary}
