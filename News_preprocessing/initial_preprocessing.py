import pandas as pd
import numpy as np
import multiprocessing
import json
import re
from datetime import datetime
import os
import pathlib
from functools import partial

from text_splitting import sentenize_text

hashes = []

pattern_for_path_names = re.compile(r"[!@#$%^&*()-.,/?]")


def get_timestamp() -> str:
    return datetime.now().isoformat()


def preprocess_news(path):

    records = []

    try:
        data = pd.read_csv(path)

        for index, sample in data.iterrows():
            TEXT = str(sample.text).replace('\n', ' ')
            META = {'url': sample.URL, 'timestamp': get_timestamp(),
                    'theme': 'news', 'language': 'ru'}

            if (not hash(TEXT) in hashes) and (TEXT is not None):
                for record in sentenize_text(TEXT):
                    if record != 0:
                        records.append(
                            {'text': record, 'meta': META}
                        )
                        hashes.append(hash(record))

        return records

    except Exception as e:
        print(f'Exception {e} is occured, processing next file')


def write_to_jsonl(path, out_dir):
    records = preprocess_news(path)
    if len(records) > 0:
        write_path = out_dir / \
            path.name.replace(".csv", ".jsonl").replace('-', '_')

        try:
            with open(write_path, 'w', encoding='utf-8') as fl:
                for record in records:
                    if record is not None:
                        fl.write(json.dumps(record) + '\n')
            print(f'{get_timestamp()} file {write_path} is done')
        except Exception as e:
            print(f'Exception {e} is occured, saving next file')


def initial_processing(data_paths, out_dir):

    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    num_cpus = multiprocessing.cpu_count()
    print(f"Using {num_cpus} processes\n")

    with multiprocessing.Pool(processes=num_cpus) as pool:
        pool.map(partial(write_to_jsonl, out_dir=out_dir), data_paths)
