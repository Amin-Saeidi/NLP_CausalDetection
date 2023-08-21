from difflib import SequenceMatcher
import torch


def get_p_and_r(tagged_sentence, target_char, result):
    """
    This function would return precision and recall and the score of sequence matcher

    :param tagged_sentence: The sentence with this format: *cause* &marker& +effect+
    :param target_char: set '*' if you want to check cause. '+' for effect. and '&' for marker
    :param result: The string that you found as the response
    :return:
    """

    if result == '' and tagged_sentence.__contains__(target_char + target_char):
        return 1, 1, 1
    elif result == '' and not tagged_sentence.__contains__(target_char + target_char):
        return 1, 0, 0

    context, sentence_copy = tagged_sentence, tagged_sentence
    for char in ['*', '+', '&']:
        sentence_copy = sentence_copy.replace(char, '') if char != target_char else sentence_copy
        context = context.replace(char, '')

    correct_ans, res_ans = [], []
    for i, word in enumerate(sentence_copy.split()):
        if word.__contains__(target_char) and word != target_char + target_char:
            correct_ans.append(i)

    if len(correct_ans) == 1:
        correct_ans.append(correct_ans[0])

    result_split, context_split = result.split(), context.split()

    for i in range(len(context_split)):
        substr = ' '.join(context_split[i: i + len(result_split)])
        r = 2
        if len(result) > 0:
            r = (len(result) - 2) / len(result)
        if SequenceMatcher(None, substr[: len(result)], result).ratio() >= r:
            res_ans.append(i)
            res_ans.append(i + len(result_split))
            break

    if len(correct_ans) > 0:
        correct_ans = list(range(correct_ans[0], correct_ans[1] + 1))
    if len(res_ans) > 0:
        res_ans = list(range(res_ans[0], res_ans[1]))

    matc = SequenceMatcher(None, ' '.join(context_split[correct_ans[0]: correct_ans[-1] + 1]), result).ratio()
    precision, recall = 0, 0
    if len(res_ans) == 0:
        precision = 1
    else:
        precision = len(set(res_ans).intersection(correct_ans)) / len(res_ans)

    if len(correct_ans) == 0:
        recall = 1
    else:
        recall = len(set(correct_ans).intersection(res_ans)) / len(correct_ans)

    return precision, recall, matc


def run_model(model, tokenizer, sentence, question):
    """

    :param model: The pre-trained model
    :param tokenizer: The tokenizer loaded from pre-trained model
    :param sentence: The raw sentence you want to find marker, cause, and effect in
    :param question: If you want to find cause or effect this should be the found marker. if you want to find marker
    set this the same as the question in training data.
    :return: This would return a substring of sentence showing marker, cause, or effect
    """

    inputs = tokenizer.encode_plus(question, sentence, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs)[0], model(**inputs)[1]

    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    return answer