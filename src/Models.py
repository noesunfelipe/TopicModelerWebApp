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
import Preprocess as p
from time import time
import pickle
from pprint import pprint


#Para medir el tiempo de ejecución
t_inic = time()


#Importar la data lematizada
with open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/DL.json",'r') as f:
    DL = json.load(f)

#Importar el/los parámetros seleccionados por el usuario en el front
with open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/parametros.json",'r') as parametros:
    NTopics_String = json.load(parametros)

#Importar el/los parámetros seleccionados por el usuario en el front
with open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.json",'r') as corp:
    corpus = json.load(corp)

id2word = pickle.load(open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/id2word.pkl", "rb"))


NTopics = int(NTopics_String)


################# APLICANDO EL MODELO 1, LDA #################

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
    pickle.dump(lda_model, open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/lda_model.pkl", "wb"))


    return(print("Modelo LDA Generado"))

LdaModel = LdaModelApplication(corpus, id2word, NTopics)



################# APLICANDO EL MODELO 2, MALLET #################

os.environ.update({'MALLET_HOME':r'C:/mallet-2.0.8/'})
mallet_path = 'C:/mallet-2.0.8/bin/mallet'

def MalletModelApplication(mallet_path, corpus, num_topics, id2word):
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
    # display topics
    #pprint(ldamallet.show_topics(formatted=False))

    # Compute Coherence Score
    #coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=corpus, dictionary=id2word, coherence='c_v')
    #coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    
    pickle.dump(ldamallet, open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/ldamallet.pkl", "wb"))
    
    return(print("Modelo Mallet Generado"))

MalletModel = MalletModelApplication(mallet_path, corpus, NTopics, id2word)


#ModelsEne_LDA = enumerate(LdaModel[corpus])
#ModelsEne_mallet = enumerate(LdaMallet[corpus])
#with open ("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/ModelsEne_LDA.json", 'w') as MENELDA:
#    json.dump(ModelsEne_LDA, MENELDA, indent =2)
#with open ("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/ModelsEne_mallet.json", 'w') as MENEMALLET:
#    json.dump(ModelsEne_mallet, MENEMALLET, indent =2)



################# MOSTRANDO LOS RESULTADOS #################
os.system('python Rendimiento.py')



################# ELIMINANDO LOS ARCHIVOS UTILIZADOS PARA LA EJECUCIÓN #################
path1 = 'C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/ReceptorArchivos/'
path2 = 'C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/'
#for filename in os.listdir(path1):
#    #Archivo = table_list.append(filename)
#    pathname1 = path1 + str(filename)
#    os.remove(pathname1)
#    print("Archivo removido!")

#for filename in os.listdir(path2):
#    #Archivo = table_list.append(filename)
#    pathname2 = path2 + str(filename)
#    os.remove(pathname2)
#    print("Json removido!")


t_fin = time()
t_elap = t_fin-t_inic
print(t_elap)