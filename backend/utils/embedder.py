from transformers import BertTokenizer
import numpy as np

def create_embeddings(texts_array: np.ndarray = None, 
                      tokenizer: BertTokenizer = None, max_len: int = 64) -> np.ndarray:
    """
    Функция для векторизации массива токенов в фомате str
    """
    if texts_array is None or tokenizer is None:
        raise Exception('Параметры texts_array / tokenizer пустые')
    
    encodings = []

    for text_arr in texts_array:
        encodings.append(tokenizer.encode_plus(
            text_arr,
            add_special_tokens=True,
            max_length=max_len,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )['input_ids'].flatten().detach().cpu().numpy())

    return np.array(encodings)

