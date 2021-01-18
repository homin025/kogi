import torch
import torch.nn.functional as F


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


def sample_sequence_sentence(model, vocab, tokenizer, device, text, temperature, top_k, top_p, sentence_length):
    tokenized = tokenizer(text)  # 받은 문장

    generated_text = ''
    generated_length = 0

    if len(tokenized) > 1024:
        tokenized = tokenized[len(tokenized) - 1000:]

    """ START: Customization for sampling is optional """
    while generated_length <= sentence_length:
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

        if generated == '</s>':
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

    return generated_text.replace('</s>', '.')


def sample_sequence_words(model, vocab, tokenizer, device, text, temperature, top_k, top_p, word_count):
    tokenized = tokenizer(text)  # 받은 문장

    if len(tokenized) > 1024:
        tokenized = tokenized[len(tokenized) - 1000:]

    input_ids = torch.tensor([vocab[vocab.bos_token], ] + vocab[tokenized]).unsqueeze(0)
    input_ids = input_ids.to(device)

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

    generated_words = vocab.to_tokens(prev.squeeze().tolist())

    return generated_words