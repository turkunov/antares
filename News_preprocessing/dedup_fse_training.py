import json
import os
from tqdm import tqdm
from fse import Vectors
from fse import IndexedList
from fse.models import uSIF


def train_fse(data_folder: str = './news_2014', model_name: str = 'fse.model'):
    """
    Функция для обучения модели Sentence2Vec
    Input:
        data_folder: str = './data' - путь до папки с исходными текстами в формате JSON Lines
        model_name: str = 'fse.model' - название файла, в который будет сохранена модель
    """
    glove = Vectors.from_pretrained("glove-wiki-gigaword-100")
    model = uSIF(glove, workers=1, lang_freq="ru")
    for file in tqdm(os.listdir(data_folder), desc='Folder'):
        with open(os.path.join(data_folder, file), 'r', encoding='utf-8') as f:
            json_list = list(f)

        sentences = []
        for json_str in tqdm(json_list, desc='File'):
            js = json.loads(json_str)
            data = js['text']
            sentences.append(data.split())
        s = IndexedList(sentences)
        model.train(s)

    model.save(model_name)
