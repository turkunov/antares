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
      self.df[column] = self.df[column].str.replace('[^0-9A-Za-zА-Яа-я.\s]+', ' ', regex=True)
      self.df[column] = self.df[column].str.replace('quot',' " ')
      self.df[column] = self.df[column].str.replace(' | '.join([x + '\s' for x in self.stop_words]), ' ', regex=True)
      self.df[column] = self.df[column].apply(self.tokenize_to_processing)
      self.df[column] = self.df[column].apply(self.stem)

def read_n_process(file_path, out_path):
  df = pd.read_excel(file_path)
  df = df[df.text.notna()][['id', 'text', 'title']]
  preprocesserClass = textPreprocesser(df, ['text'])
  preprocesserClass.clean()
  preprocesserClass.df['text'].to_csv(out_path)

if __name__ == '__main__':
  read_n_process('initial_data/posts.xlsx', 'initial_data/result.csv')