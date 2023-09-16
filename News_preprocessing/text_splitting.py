from razdel import sentenize
from itertools import islice


num_sentences = 60

def length_of_text(text):
    if len(text) > 10:
        return True
    else:
        return False

def split_seq(iterable, size=num_sentences):
    it = iter(iterable)
    item = list(islice(it, size))
    while item:
        yield item
        item = list(islice(it, size))

def sentenize_text(data):
        sentences = [sentence.text for sentence in sentenize(data)]
        for sequence in list(split_seq(sentences)):
            yield ' '.join(sequence)

def text_splitting(text):
    if length_of_text(text):
        return sentenize_text(text)
    else:
        return 0