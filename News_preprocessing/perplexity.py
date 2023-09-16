import json
import pathlib
from datetime import datetime
import re
import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import numpy as np
from functools import partial

import os
import multiprocessing


def get_timestamp() -> str:
    return datetime.now().isoformat()


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def remove_special_symbols(text):
    return re.sub(r'[^\w\s]', '', text.lower())


def perplexity_count(data, n=3):
    model = MLE(n)
    perplexity = []
    perplexity_values = []

    sentences = [data[i]['text'] for i in range(len(data))]

    tokenized_text = [list(nltk.tokenize.word_tokenize(remove_special_symbols(sent)))
                      for sent in sentences]

    train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)

    model.fit(train_data, padded_vocab)

    test_data, _ = padded_everygram_pipeline(n, tokenized_text)

    for i, test in enumerate(test_data):
        perp = model.perplexity(test)

        perplexity_values.append(perp)

    return perplexity_values


def perplexity_outliers(perplexity_values):
    values = np.array(perplexity_values)
    high = np.quantile(values, 0.75) + 1.5 * np.std(values)
    return (values < high).nonzero()[0]


def write_to_jsonl(path, out_dir):
    write_path = out_dir / path.name

    try:
        data = read_jsonl_file(path)
    except Exception as e:
        print(f'Exception {e} had occured, reading next file...\n')

    try:
        perplexity_values = perplexity_count(data)
        indexes = perplexity_outliers(perplexity_values)
    except Exception as e:
        print(f'Exception {e} had occured, count perplexity in next file...\n')

    try:
        with open(write_path, 'w', encoding='utf-8') as fl:
            for index in indexes:
                if perplexity_values[index] is not None:
                    fl.write(json.dumps(data[index]) + '\n')
        print(f'{get_timestamp()} file {write_path} is done')
    except Exception as e:
        print(f'Exception {e} is occured, writing next file...')


def perplexity(data_paths, out_dir):

    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    num_cpus = multiprocessing.cpu_count()
    print(f"Using {num_cpus} processes\n")

    with multiprocessing.Pool(processes=num_cpus) as pool:
        pool.map(partial(write_to_jsonl, out_dir=out_dir), data_paths)


if __name__ == '__main__':
    data_paths = list(pathlib.Path('dedup_news').glob("*.jsonl"))
    perplexity(data_paths)
