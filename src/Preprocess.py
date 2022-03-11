#Importando librerías necesarias
import pandas as pd 
import nltk
nltk.download('stopwords')
import re
import numpy as np
import pandas as pd
from pprint import pprint
import pickle
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# spacy for lemmatization
import spacy
# Plotting tools
import matplotlib.pyplot as plt
#%matplotlib inline
# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
#Medición del rendimiento
from time import time

t_inic = time()

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('spanish')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
#print(stop_words)

#Como debemos usar algunos documentos de este archivo en otros, los mantendremos a través de json
import json


#enrutado
import index as ind

path = ind.app.config['UPLOAD_FOLDER']
TempData = ind.app.config['TEMP_DATA']


#Enrutado del archivo excel
import os 
#path = 'C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/ReceptorArchivos/'
for filename in os.listdir(path):
    #Archivo = table_list.append(filename)
    pathname = path + str("/")+str(filename)

df = pd.read_excel(os.path.join(pathname), engine='openpyxl')
#print(pathname)

#Convertir el texto en lista
data = df.reclamo_descripcion.values.tolist()
ID = df.caso_numero.values.tolist()

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(data))


#Creamos una bag of words que me permita eliminar las palabras con mayor y menor frecuencia
bag_of_words = []

for recl in data_words:
    for wd in recl:
        bag_of_words.append(wd)
        
# Python code to demonstrate 
# sort list by frequency 
# of elements 

from collections import Counter 
ini_list = bag_of_words

# sorting on bais of frequency of elements 
result = [item for items, c in Counter(ini_list).most_common() 
                                    for item in [items] * c] 


# Frequency grouping of list elements 
# using Counter() + items() 
res = list(Counter(result).items()) 

# printing result 
#print("Frequency of list elements : " + str(res)) 

#Al hacer el print anterior vemos que hay muchos elementos con muy alta frecuencia y 
#la mayor parte son stopwords. Vamos a tomar todas las palabras con valor 1, a una lista aparte que 
#posteriormente utilizaremos como "stopword":
final_bag = []
for (x,y) in res:
    if y <= 1:
        final_bag.append(x)

##Añadimos la final_bag a la bolsa de stopwords.        
stop_words = stop_words + final_bag


# Build the bigram and trigram models
#Por las dudas: bigrama es un par de palabras que frecuentemente están una al lado de otra
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)


#python -m spacy download es_core_news_sm
#El código actual que quiero probar es:
#import es_core_news_sm
#nlp = es_core_news_sm.load()

#pip3 install spacy_spanish_lemmatizer
#python -m spacy_spanish_lemmatizer download wiki


#import spacy
#from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
# Change "es" to the Spanish model installed in step 2

#import es_core_news_sm
#nlp = es_core_news_sm.load()
import es_dep_news_trf
nlp = es_dep_news_trf.load()
#lemmatizer = SpacyCustomLemmatizer()
#nlp = nlp.add_pipe(SpacyCustomLemmatizer, name="lemmatizer", after="tagger")


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    #lemmatizer = SpacyCustomLemmatizer()
    #nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

import spacy
import es_dep_news_trf
#from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
# Change "es" to the Spanish model installed in step 2
#nlp = spacy.load("es_core_news_sm")
nlp = spacy.load("es_dep_news_trf")

#lemmatizer = SpacyCustomLemmatizer()
#nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")
#for token in nlp(
#    """Con estos fines, la Dirección de Gestión y Control Financiero monitorea
#       la posición de capital del Banco y utiliza los mecanismos para hacer un
#       eficiente manejo del capital."""
#):
#    print(token.text, token.lemma_)


    # Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
#nlp = es_core_news_sm.load(disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

#print(data_lemmatized[:2])

DLPATH = os.path.join(TempData, "DL.json")
with open(DLPATH, 'w') as f:
    json.dump(data_lemmatized, f, indent =2)

def preprocess(data_lemmatized):
    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    #print(corpus[:1])
    return id2word, corpus

id2word, corpus = preprocess(data_lemmatized)
#print("Esta es la primera versión del corpus")
#print(corpus)
#with open ("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.json", 'w') as cor:
#    json.dump(corpus, cor, indent =2)
CORPUSPATH = os.path.join(TempData, "corpus.json")
with open (CORPUSPATH, 'w') as cor:
    json.dump(corpus, cor, indent = 2)

#pickle.dump(corpus, open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.pkl", "wb"))

#corpora.MmCorpus.serialize("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.mm", corpus)

ID2WORDPATH = os.path.join(TempData, "id2word.pkl")
pickle.dump(id2word, open(ID2WORDPATH, "wb"))


t_fin = time()
t_elap = t_fin-t_inic
#print("el tiempo de procesamiento es " + str(t_elap))

os.system('python src/Rendimiento.py')
