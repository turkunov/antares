from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
import json

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

# сехма для новостей
class newsSchema(BaseModel):
    title: str
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
def dataset_inference():
    """
    GET-эндпоинт для получения инференса модели на датасете
    """
    return None

@app.get('/api/single_inference/')
async def single_inference(article: newsSchema):
    """
    GET-эндпоинт для получения инференса модели на конкретной новости
    """
    return None