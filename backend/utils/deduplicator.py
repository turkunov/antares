import faiss
import numpy as np
import pandas as pd

def l2_dists(embeddings: np.ndarray) -> tuple:
    """
    Функция возвращает Евклидово расстояние между каждым эмбеддингом
    на основе IndexFlatL2 из FAISS

    :params: 
    embeddings: np.ndarray
        - массив эмбеддингов текстов новостей

    :returns: кортеж из расстояний между каждым эмбеддингом и соответствующие под них индексы эмбеддингов
    """
    D = embeddings.shape[1]
    N = embeddings.shape[0]

    index = faiss.IndexFlatL2(D)
    index.add(embeddings)

    return index.search(x=embeddings, k=N)

def dedup(news_dataset: pd.DataFrame, distances: np.ndarray, indices: np.ndarray, thresh: float = 1.6) -> tuple:
    """
    Функция дедубликации. Удаляет новости, которые имеют относительно себя похожие вектора

    :params:
    news_dataset: pd.DataFrame
        - датафрейм с новостями в любом формате. Необходимо только, чтобы количество строк
        в news_dataset совпадало с количеством строк в distances
    distances: np.ndarray
        - массив l2 расстояний между эмбеддингами
    indices: np.ndarray
        - массив индексов отсортированных в соответствии с distances
    thresh: float
        - максимально возможная дистанция между похожими эмбеддингами

    :returns: кортеж из обновленного датасета с убранными дубликатами, а также их количество
    """

    certain_duplicates = (distances <= thresh) & (distances != 0)
    
    # выделение уникальных новостей
    certain_non_duplicates = news_dataset[certain_duplicates.sum(axis=1) == 0]

    # выделение уникальных новостей среди дубликатов
    duplicated_dist = (indices * certain_duplicates)
    uniques, count = np.unique(duplicated_dist, return_counts=True)
    non_duplicates_in_duplicates = []
    for duplicate in uniques:
        duplicated_dist[duplicated_dist == duplicate] *= -1
        if np.all(duplicated_dist[duplicate] >= 0):
            non_duplicates_in_duplicates.append(duplicate)

    non_duplicates = pd.concat([certain_non_duplicates,news_dataset.iloc[non_duplicates_in_duplicates,:]],axis=0)

    return non_duplicates, news_dataset.shape[0] - non_duplicates.shape[0]