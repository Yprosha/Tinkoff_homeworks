import random
import pandas as pd
import re
from nltk.corpus import stopwords
from gensim.models import Word2Vec



class Document:
    def __init__(self, title, text):
        # можете здесь какие-нибудь свои поля подобавлять
        self.title = title
        self.text = text
    
    def format(self, query):
        # возвращает пару тайтл-текст, отформатированную под запрос
        return [self.title, self.text + ' ...']

index = []

def build_index():
    data = pd.read_csv('news_summary.csv')
    # считывает сырые данные и строит индекс
    for text in data:
        index.append(Document(text['headlines'], text['text']))

def something(data):
    dictionary = list(data.text)
    expr = r'[^\w ]'
    dictionary = list(map(lambda x: (re.sub(expr, '', x)), dictionary))

    sentences = list(map(lambda dictionary: dictionary.split(), dictionary))
    model = Word2Vec(sentences, min_count=1, seed=1, workers=1)
    wv = model.wv
    return wv





def score(search, document, wv):
    sw_eng = set(stopwords.words('english'))
    search = list(map(lambda x: ' '.join([word for word in x.split() if not word in sw_eng]), [search]))[0]
    expr = r'[^\w ]'
    document = list(map(lambda x: (re.sub(expr, '', x)), [document]))[0]
    news_score = []
    for word in search.split():
        score = []
        for i in document.split():
            score.append(wv.similarity(word, i))
        news_score = news_score + sorted(score)[-3:]
    return sum(sorted(news_score)[-2:])
    # возвращает какой-то скор для пары запрос-документ
    # больше -- релевантнее

def retrieve(query):
    # возвращает начальный список релевантных документов
    # (желательно, не бесконечный)
    candidates = []
    for doc in index:
        #if query.lower() in doc.title.lower() or query in doc.text.lower():
        candidates.append(doc)
    return candidates