import random
import numpy as np

import torch
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer


def main(content, model_name):
    """ Independent variables """
    temperature = 0.7
    top_k = 40
    top_p = 0.9

    model_dict = {
        "gpt2": ["gpt2", "./model/gpt2_config.json", "./model/gpt2_as_cnn_30.ckpt"],
        "kogpt2": ["taeminlee/kogpt2", None, "./model/kogpt2_as_korean_corpus_30.ckpt"]
    }

    model_name, config_file, model_file = model_dict[model_name]

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path=model_name)
    if config_file:
        config = GPT2Config.from_json_file(config_file)
        model = GPT2LMHeadModel(config)
    model.load_state_dict(torch.load(model_file, map_location=device))

    model.to(device)
    model.eval()

    tokenizer = GPT2Tokenizer.from_pretrained(pretrained_model_name_or_path=model_name)

    # bos_token = tokenizer.token_to_id("<s>")
    # eos_token = tokenizer.token_to_id("</s>")
    # task_token = tokenizer.encode("질문:").ids
    #
    # context_tokens = tokenizer.encode(f"문맥:{content}").ids
    # answers_tokens = [tokenizer.encode(f"정답:{keyword}").ids for keyword in keywords]
    #
    # generated_questions = []
    # generated_answers = []
    # for answer_tokens in answers_tokens:
    #     len_input_ids = 1 + len(context_tokens) + len(answer_tokens) + len(task_token) + 1
    #
    #     if len_input_ids >= 800:
    #         len_available = 800 - len(answers_tokens) - len(task_token)
    #         context_tokens = context_tokens[:len_available]
    #
    #     input_ids = [bos_token] + context_tokens + answer_tokens + task_token
    #     len_input_ids = len(input_ids)
    #     input_ids = torch.LongTensor([input_ids])
    #     attention_mask = torch.LongTensor([[1.0] * len_input_ids])
    #
    #     model.to(device)
    #     input_ids.to(device)
    #     attention_mask.to(device)
    #
    #     output = model.generate(
    #         input_ids=input_ids,
    #         attention_masks=attention_mask,
    #         max_length=len_input_ids+50,
    #         min_length=len_input_ids+5,
    #         pad_token_id=0,
    #         bos_token_id=1,
    #         eos_token_id=2,
    #         repetition_penalty=1.3,
    #         no_repeat_ngram_size=3,
    #         num_return_sequences=1,
    #     )
    #
    #     for output_tokens in output.tolist():
    #         keyword = tokenizer.decode(answer_tokens)
    #         keyword = keyword.split(":")[1]
    #         generated_answers.append(keyword)
    #         sentence = tokenizer.decode(output_tokens[len_input_ids:])
    #         sentence = sentence.split("</s>")[0].replace("<s>", "")
    #         generated_questions.append(sentence)
    #
    # return {"questions": generated_questions, "answers": generated_answers}
