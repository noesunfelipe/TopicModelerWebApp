# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import wrappers
from gensim.models.wrappers import LdaMallet
import json
import spacy
import os
#import Preprocess as p
from time import time
import pickle
from pprint import pprint
#pprint = p.pprint
#corpus = p.corpus
#id2word = p.id2word
import index as ind
from time import time

t_inic = time()
print("comenzaré a medir el tiempo de procesamiento_1")

MALLETPATH = ind.app.config['MALLET_PATH']
path = ind.app.config['UPLOAD_FOLDER']
TempData = ind.app.config['TEMP_DATA']
Plots = ind.app.config["STATIC"]
os.environ['MALLET_HOME'] = MALLETPATH
mallet_path = os.path.join(MALLETPATH, 'bin', 'mallet.bat')
#Importar la data lematizada
DLPATH = os.path.join(TempData, "DL.json")
with open(DLPATH,'r') as f:
    DL = json.load(f)

#Importar el/los parámetros seleccionados por el usuario en el front
NTOPICSFINPATH = os.path.join(TempData, "NTopicsFin.json")
with open(NTOPICSFINPATH,'r') as parametros:
    NTopics_String = json.load(parametros)


#Importar el/los parámetros seleccionados por el usuario en el front
CORPUSPATH = os.path.join(TempData, "corpus.json")
with open(CORPUSPATH,'r') as corp:
    corpus = json.load(corp)
    
#Importar el/los parámetros seleccionados por el usuario en el front
MODELOSELECTPATH = os.path.join(TempData, "ModeloSelec.json")
with open(MODELOSELECTPATH,'r') as ChosenModel:
    SelectedModel = json.load(ChosenModel)

ID2WORDPATH = os.path.join(TempData, "id2word.pkl")
id2word = pickle.load(open(ID2WORDPATH, "rb"))

NTopics = int(NTopics_String)

def LdaModelApplication(corpus, id2word, num_topics):
    # Build LDA model
    lda_model = gensim.models.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=num_topics, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)


    # Print the Keyword in the 7 topics
    #pprint(lda_model.print_topics())
    #doc_lda = lda_model[corpus]
    #PerplejidadLDA_inic = lda_model.log_perplexity(corpus) ##Esta es la perplejidad, menos es mejor
    

    # Compute Perplexity
    #print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.
    LDAMODELFINPATH = os.path.join(TempData, "lda_model_fin.pkl")
    pickle.dump(lda_model, open(LDAMODELFINPATH, "wb"))


    return(print("Modelo LDA Generado"))


################# APLICANDO EL MODELO 2, MALLET #################

def MalletModelApplication(mallet_path, corpus, num_topics, id2word):
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
    # display topics
    #pprint(ldamallet.show_topics(formatted=False))

    # Compute Coherence Score
    #coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=corpus, dictionary=id2word, coherence='c_v')
    #coherence_ldamallet = coherence_model_ldamallet.get_coherence()

    LDAMALLETFINPATH = os.path.join(TempData, "ldamallet_fin.pkl")
    pickle.dump(ldamallet, open(LDAMALLETFINPATH, "wb"))
    
    return(print("Modelo Mallet Generado"))





if SelectedModel == "lda_model":
    LdaModel_fin = LdaModelApplication(corpus, id2word, NTopics)

else: 
    MalletModel_fin = MalletModelApplication(mallet_path, corpus, NTopics, id2word)


t_fin = time()
t_elap = t_fin-t_inic
print("el tiempo de procesamiento_1 es: " + str(t_elap))

os.system('python FinalProcess.py')