import numpy
from bs4 import BeautifulSoup
import nltk

TAG_FILTER =['CC','CD','DT','EX','IN','MD','PRP','PRP$','RB','RP','WDT','WP','WRB']


def clean_text(text):
    # tokenize sans les balises html
    bs = BeautifulSoup(text.lower(), "html.parser")
    res = nltk.RegexpTokenizer(r'[a-zA-Z0-9.#_+-]+').tokenize(bs.get_text())
    
    #filtre certain POS tag
    res_tagged = nltk.pos_tag(res)
    res_filtred = [word for word, tag in res_tagged if tag not in TAG_FILTER]
    
    #remove stop words
    stopwords = set(nltk.corpus.stopwords.words('english'))
    res_ft_sw = [word for word in res_filtred if not word in stopwords]
    
    #stemming
    stemmer = nltk.stem.PorterStemmer()
    res_ft_sw_stem = [stemmer.stem(word) for word in res_ft_sw]
    
    return ' '.join( res_ft_sw_stem )


def build_corpus_data(df):
	return clean_text(df['Title']) + ' ' + clean_text(df['Body'])

def build_corpus_element(title, body):
	return clean_text( title )  + ' ' + clean_text ( body )