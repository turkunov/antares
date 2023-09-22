from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Response
import json
import pandas as pd
import numpy as np
from transformers import BertTokenizer
import pickle
from io import StringIO

# кастомные утилиты для предобработки входных текстов
from utils.embedder import create_embeddings
from utils.deduplicator import l2_dists, dedup
from utils.preprocessing import textPreprocesser, txt_to_dataframe

def json_read(filepath: str) -> dict:
    with open(filepath,'r',encoding='utf-8') as f:
        return json.load(f)

# подгрузка мета данных для описания в swagger UI
META_PATH = 'api_meta.json'
META_DATA = json_read(META_PATH)

app = FastAPI(
    title=META_DATA['CLIENT_META']['title'],
    description=META_DATA['CLIENT_META']['description'],
    version=META_DATA['CLIENT_META']['version'],
    terms_of_service=None,
    contact=META_DATA['CLIENT_META']['contact'],
    license_info=None
)

# костанты для обучения
tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
classifier = pickle.load(open('model', 'rb'))

# сехма для новостей
class newsSchema(BaseModel):
    channelid: str
    text: str

# CORS для удобства отладки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/dataset_inference/')
async def dataset_inference(dataset: UploadFile = File(...)):
    """
    GET-эндпоинт для получения инференса модели на датасете. Возвращает обработанный датасет в .csv
    """
    # returning new file tutorial
    # https://www.ihsanmohamad.com/blog/posts/how-to-read-excel-and-temporary-download.html

    contents = dataset.file.read()
    data = str(contents,'utf-8')
    dataset.file.close()

    data = StringIO(data)
    extension = dataset.filename.split('.')[1]
    if extension is not None:
        if extension == 'txt':
            df = pd.read_csv(data, delimiter='\n\"\t', header=None)
            df = txt_to_dataframe(df, 'texts')
        elif extension == 'csv':
            df = pd.read_csv(data, delimiter='\t', header=None)
            df.columns = ['texts','channelid']
        else:
            df = pd.read_excel(data)
    data.close()

    # препроцессинг
    preprocesser = textPreprocesser(df.copy(), ['texts'])
    preprocesser.clean()
    X = preprocesser.df['texts'].str.join(' ').str.replace('\.*', '', regex=True).values

    # создание эмбеддингов
    embeddings = create_embeddings(X, tokenizer)

    # удаление дубликатов
    dists, indices = l2_dists(embeddings)
    dedup_df, removed_n = dedup(preprocesser.original_df, dists, indices)

    # создание предсказаний
    pred_classes = classifier.predict(embeddings[dedup_df.index.values,:]).reshape(-1,1)
    dedup_df['classes'] = pred_classes
    
    headers = {'Content-Disposition': 'attachment; filename="results.csv"'}
    return Response(dedup_df.to_csv(), headers=headers, media_type="text/csv")

@app.get('/api/single_inference/')
async def single_inference(article: newsSchema):
    """
    GET-эндпоинт для получения инференса модели на конкретной новости
    """
    try:
        stemmed_tokens = ' '.join(textPreprocesser.clean_text(article.text))
        stemmed_embeddings = create_embeddings(np.array([stemmed_tokens]), tokenizer)

        pred_class = classifier.predict(stemmed_embeddings).item()

        return {
            'status_code': 200,
            'class': pred_class
        }
    except Exception as err:
        print(f'[ERR] GET single_inference: {err}')
        {
            'status_code': 400,
            'error': str(err)
        }