import random
import numpy as np

import torch


def main(content, model, tokenizer, device, model_file, temperature, top_k, top_p, keywords, sentence_length):
    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    model.load_state_dict(torch.load(model_file, map_location=device))

    model.to(device)
    model.eval()

    bos_token = tokenizer.token_to_id("<s>")
    eos_token = tokenizer.token_to_id("</s>")
    task_token = tokenizer.encode("질문:").ids

    context_tokens = tokenizer.encode(f"문맥:{content}").ids
    answers_tokens = [tokenizer.encode(f"정답:{keyword}").ids for keyword in keywords]

    generated_questions = []
    generated_answers = []
    for answer_tokens in answers_tokens:
        len_input_ids = 1 + len(context_tokens) + len(answer_tokens) + len(task_token) + 1

        if len_input_ids >= 1000:
            len_available = len_input_ids - 1000
            context_tokens = context_tokens[len_available:]

        input_ids = [bos_token] + context_tokens + answer_tokens + task_token
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
            min_length=len_input_ids+1,
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

        for output_tokens in output.tolist():
            keyword = tokenizer.decode(answer_tokens)
            keyword = keyword.split(":")[1]
            generated_answers.append(keyword)
            sentence = tokenizer.decode(output_tokens[len_input_ids:])
            sentence = sentence.split("</s>")[0].replace("<s>", "")
            generated_questions.append(sentence)

    return {"questions": generated_questions, "answers": generated_answers}
