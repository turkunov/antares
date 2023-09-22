import pandas as pd
import dask.dataframe as dd
import nltk
import re
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

import warnings
warnings.filterwarnings("ignore")

def txt_to_dataframe(df: pd.DataFrame, texts_column: str) -> pd.DataFrame:
  """
  Конвертация сырого датасета, прочитанного из текстового файла в нормальный датасет
  """

  df_texts = df.iloc[::2,0].reset_index()[[0]]
  df_targets = df.iloc[1::2,0].str.replace('"\t', '').astype(int).reset_index()[[0]]
  df = pd.concat([df_texts, df_targets], axis=1)
  df.columns = [texts_column,'targets']
  df.dropna(subset=['targets', texts_column], inplace=True)
  replacements = {
    original_class: i for i, original_class in enumerate(df['targets'].unique())
  }
  df['targets'].replace(replacements,inplace=True)
  df['targets'] = df['targets'].astype(int)
  df.drop_duplicates(subset=texts_column, inplace=True)

  return df

class textPreprocesser:

  def __init__(self, df: pd.DataFrame, columns_for_preprocessing: list, partitions: int = 100) -> None:
    """
    Класс для препроцессинга столбцов columns_for_preprocessing в датафрейме df. 
    Для более качественных результатов по итогам происходит стемматизация токенов 
    вместо их лемматизации. 

    :params:
    df: pd.DataFrame
      - Датафрейм для обработки
    columns_for_preprocessing: list
      - Список из столбцов для препроцессинга
    partitions: int
      - Объем частей датасета для деления для разбиения их затем на графы через dask
    """
    df = df.reset_index()
    try: 
        self.stemmer = SnowballStemmer('russian')
        self.stop_words = set(stopwords.words('russian') + stopwords.words('english'))
        self.cols = columns_for_preprocessing
        self.df = dd.from_pandas(df, npartitions=partitions)
    except Exception as e:
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stemmer = SnowballStemmer('russian')
        self.stop_words = set(stopwords.words('russian') + stopwords.words('english'))
        self.cols = columns_for_preprocessing
        self.df = dd.from_pandas(df, npartitions=partitions)

    self.original_df = self.df.loc[:,columns_for_preprocessing]
    
  def tokenize_to_processing(self, token_string: str) -> list:
    if type(token_string) == str:
        return [w for s in sent_tokenize(token_string) for w in word_tokenize(s)]
    else:
       return []

  def stem(self, tokens: list) -> list:
    return [self.stemmer.stem(token) for token in tokens]

  def clean(self) -> None:
    """
    Метод для очистки заранее определенных столбцов self.cols. После очистки
    обновляет столбцы self.cols датафрейма self.df.
    """
    for column in self.cols:
      self.df[column] = self.df[column].str.lower()

      # удаление ссылок и всех других символов кроме букв, пробелов и точек
      self.df[column] = self.df[column].str.replace('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', regex=True)
      self.df[column] = self.df[column].str.replace('[^A-Za-zА-Яа-я.\s]+', ' ', regex=True)
      self.df[column] = self.df[column].str.replace('quot',' " ')

      # удаление стоп-слов
      self.df[column] = self.df[column].str.replace(' | '.join([x + '\s' for x in self.stop_words]), ' ', regex=True)

      # токенизация и стемматизация
      self.df[column] = self.df[column].map_partitions(lambda df: df.apply(self.tokenize_to_processing))
      self.df[column] = self.df[column].map_partitions(lambda df: df.apply(self.stem)).compute(scheduler='processes')

      # удаление пустых значений, которые могли получиться после препроцессинга
      self.df = self.df[self.df[column].str.len() > 0].compute()
      self.original_df = self.original_df.compute()
      self.original_df = pd.DataFrame(self.original_df.values[self.df.index.values,:])

  @staticmethod
  def clean_text(text: str) -> list:
    """
    Статичный метод для обработки единственного текста
    """
    try: 
        stemmer = SnowballStemmer('russian')
        stop_words = set(stopwords.words('russian') + stopwords.words('english'))
    except Exception as e:
        nltk.download('punkt')
        nltk.download('stopwords')
        stemmer = SnowballStemmer('russian')
        stop_words = set(stopwords.words('russian') + stopwords.words('english'))

    text = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", "", text)
    text = text.replace('quot', '"')
    text = re.sub(r"[^A-Za-zА-Яа-я.\s]+", " ", text)
    text = re.sub(' | '.join([x + '\s' for x in stop_words]), '', text)
    text = [w for s in sent_tokenize(text) for w in word_tokenize(s)]

    return [stemmer.stem(token) for token in text]
