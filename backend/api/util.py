import torch
import torch.nn.functional as F


special_tokens = ['<s>', '</s>', '<usr>', '<pad>', '<sys>', '<unk>', ]
special_characters = [' ', '.', '.', ',', '!', '?', '\'', '\"', '“', '”', '‘', '’', ' .', ' .', '..', '.,', '.!', '.?', '.\'', '.\"', '.“', '.”', '.‘', '.’', ]


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


def sample_sequence_sentence(model, tokenizer, device, text, temperature, top_k, top_p, sentence_count):
    context_tokens = tokenizer.encode(text).ids  # 받은 문장

    generated_ids = []
    generated_text = []

    bos_token = tokenizer.token_to_id("<s>")
    eos_token = tokenizer.token_to_id("</s>")

    """ Get the first following N tokens """
    input_ids = [bos_token] + context_tokens

    if len(input_ids) > 1000:
        input_ids = input_ids[len(input_ids) - 1000:]

    input_ids = torch.tensor([input_ids]).cuda()

    input_ids.to(device)

    predicts = model(input_ids)
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

    prev = torch.multinomial(log_probs, num_samples=sentence_count)

    for generated_id in prev.squeeze().tolist():
        generated_ids.append([generated_id])
        generated_token = tokenizer.id_to_token(generated_id)

        if generated_token not in special_tokens:
            generated_token = generated_token.replace('▁', ' ')
            generated_text.append(generated_token)
        else:
            generated_text.append('')

    """ Get to the end of sentence with each first tokens """
    for idx in range(sentence_count):
        while True:
            input_ids = [bos_token] + context_tokens + generated_ids[idx]

            if len(input_ids) > 1000:
                input_ids = input_ids[len(input_ids) - 1000:]

            input_ids = torch.tensor([input_ids]).cuda()

            input_ids.to(device)

            predicts = model(input_ids)
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

            generated_ids[idx] += prev.tolist()[0]

            generated_token = tokenizer.id_to_token(prev)

            if generated_token == '.' or generated_token == '</s>':
                generated_token = generated_token.replace('</s>', '')
                generated_text[idx] += generated_token
                break
            elif generated_token not in special_tokens:
                generated_token = generated_token.replace('▁', ' ')
                generated_text[idx] += generated_token

    return generated_text


def sample_sequence_words(model, tokenizer, device, text, temperature, top_k, top_p, word_count):
    context_tokens = tokenizer.encode(text).ids  # 받은 문장

    generated_ids = []
    generated_words = []

    bos_token = tokenizer.token_to_id("<s>")
    eos_token = tokenizer.token_to_id("</s>")

    input_ids = [bos_token] + context_tokens

    if len(input_ids) > 1000:
        input_ids = input_ids[len(input_ids) - 1000:]

    input_ids = torch.tensor([input_ids]).cuda()

    predicts = model(input_ids)
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

    prev = torch.multinomial(log_probs, num_samples=word_count)

    for generated_id in prev.squeeze().tolist():
        generated_ids.append([generated_id])
        generated_token = tokenizer.id_to_token(generated_id)

        if generated_token.strip('▁') not in special_tokens and generated_token.strip('▁') not in special_characters:
            generated_token = generated_token.replace('▁', ' ')
            generated_words.append(generated_token)
        else:
            generated_words.append('')

    for idx in range(word_count):
        if generated_words[idx] != '':
            continue

        while True:
            input_ids = [bos_token] + context_tokens + generated_ids[idx]

            if len(input_ids) > 1000:
                input_ids = input_ids[len(input_ids) - 1000:]

            input_ids = torch.tensor([input_ids]).cuda()

            input_ids.to(device)

            predicts = model(input_ids)
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

            generated_ids[idx] += prev.tolist()[0]

            generated_token = tokenizer.id_to_token(prev)

            if generated_token.strip('▁') not in special_tokens and generated_token.strip('▁') not in special_characters:
                generated_token = generated_token.replace('▁', ' ')
                generated_words[idx] += generated_token
                break

        generated_words.append(generated_token)

    return generated_words


def sample_sequence_paragraph(model, tokenizer, device, text, temperature, top_k, top_p, paragraph_count):
    context_tokens = tokenizer.encode(text).ids  # 받은 문장

    generated_text = ''
    generated_count = 0

    generated_id = []

    bos_token = tokenizer.token_to_id("<s>")
    eos_token = tokenizer.token_to_id("</s>")

    while generated_count <= paragraph_count:
        input_ids = [bos_token] + context_tokens + generated_id

        if len(input_ids) > 1000:
            input_ids = input_ids[len(input_ids) - 1000:]

        input_ids = torch.tensor([input_ids]).cuda()

        input_ids.to(device)

        predicts = model(input_ids)
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

        generated_id += prev.tolist()[0]

        generated_token = tokenizer.id_to_token(prev)

        if generated_token == '.' or generated_token == '</s>':
            generated_token = generated_token.replace('</s>', '')
            generated_text += generated_token
            generated_count += 1
        elif generated_token not in special_tokens:
            generated_token = generated_token.replace('▁', ' ')
            generated_text += generated_token

    return text + generated_text
