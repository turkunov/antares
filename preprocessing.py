import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

import warnings
warnings.filterwarnings("ignore")

class textPreprocesser:

  def __init__(self, df: pd.DataFrame, columns_for_preprocessing: list) -> None:
    try: 
        self.stemmer = SnowballStemmer('russian')
        self.stop_words = set(stopwords.words('russian') + stopwords.words('english'))
        self.cols = columns_for_preprocessing
        self.df = df
    except Exception as e:
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stemmer = SnowballStemmer('russian')
        self.stop_words = set(stopwords.words('russian') + stopwords.words('english'))
        self.cols = columns_for_preprocessing
        self.df = df
    
  def tokenize_to_processing(self, token_string: str) -> list:
    if type(token_string) == str:
        return [w for s in sent_tokenize(token_string) for w in word_tokenize(s)]
    else:
       return []

  def stem(self, tokens: list) -> list:
    return [self.stemmer.stem(token) for token in tokens]

  def clean(self) -> None:
    for column in self.cols:
      self.df[column] = self.df[column].str.lower()
      self.df[column] = self.df[column].str.replace('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', regex=True)
      self.df[column] = self.df[column].str.replace('[^A-Za-zА-Яа-я.\s]+', ' ', regex=True)
      self.df[column] = self.df[column].str.replace('quot',' " ')
      self.df[column] = self.df[column].str.replace(' | '.join([x + '\s' for x in self.stop_words]), ' ', regex=True)
      self.df[column] = self.df[column].apply(self.tokenize_to_processing)
      self.df[column] = self.df[column].apply(self.stem)
      self.df = self.df[self.df[column].str.len() > 0]