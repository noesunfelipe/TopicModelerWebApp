import json
import pickle
from pprint import pprint
import os
#import Preprocess as p
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import wrappers
from gensim.models.wrappers import LdaMallet
import matplotlib.pyplot as plt
import index as ind


MALLETPATH = ind.app.config['MALLET_PATH']
path = ind.app.config['UPLOAD_FOLDER']
TempData = ind.app.config['TEMP_DATA']
Plots = ind.app.config["STATIC"]
os.environ['MALLET_HOME'] = MALLETPATH
#os.environ.update({'MALLET_HOME': r'MALLETPATH'})

#mallet_path = 'C:/mallet-2.0.8/bin/mallet'
mallet_path = os.path.join(MALLETPATH, 'bin', 'mallet.bat')
#src\mallet-2.0.8\bin\mallet
if __name__ == '__main__':
    
    import multiprocessing
    from multiprocessing import Process, freeze_support
    multiprocessing.set_start_method("spawn", True)
    freeze_support()

    #Importar el archivo de data lemmatizada
    DLPATH = os.path.join(TempData, "DL.json")
    with open(DLPATH,'r') as f:
        data_lemmatized = json.load(f)
    #Importar el/los parámetros seleccionados por el usuario en el front
    CORPUSPATH = os.path.join(TempData, "corpus.json")
    with open(CORPUSPATH,'r') as corp:
        corpus = json.load(corp)

    ID2WORDPATH = os.path.join(TempData, "id2word.pkl")
    id2word = pickle.load(open(ID2WORDPATH, "rb"))
    #ldamallet = pickle.load(open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/ldamallet.pkl", "rb"))
    #lda_model = pickle.load(open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/lda_model.pkl", "rb"))

    print("me voy a pegar")
    #pprint(lda_model.print_topics())
    print("me pegué")
    #PerplejidadLDA_inic = lda_model.log_perplexity(corpus) ##Mientras menor el valor, mejor.
    #print(PerplejidadLDA_inic)
    print("me pegaré de nuevo")
    # Compute Perplexity
    #print('\nPerplexity LDA: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.




    #coherence_model_lda = CoherenceModel(model=lda_model, texts=corpus, dictionary=id2word, coherence='c_v')
    #coherence_lda = coherence_model_lda.get_coherence()
    #print(coherence_lda)
    print("Acá si que me pego")

    ################# DEFINIENDO EL MODELO DE COHERENCIA GENÉRICO #################
    #from multiprocessing import Process, freeze_support

    def coherence_model(model, texts, dictionary, coherence):
        coherence_model = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence=coherence)
        coherenceindex= coherence_model.get_coherence()
        return(print("El índice de coherencia del modelo LDA es: " + str(coherenceindex)))



    #Process(target=coherence_model, args =(lda_model, DL, id2word, 'c_v')).start()
        
    #LDACIndex = coherence_model(lda_model, data_lemmatized, id2word, 'c_v')

    #LDACIndex = main(lda_model, corpus, id2word, 'c_v')
    #pprint(LDACIndex)

    #print('\nCoherence Score LDA: ', coherence_lda)


    #pprint(ldamallet.print_topics())
    #coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=corpus, dictionary=id2word, coherence='c_v')
    #coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    #pprint('\nPerplexity Mallet: ', coherence_ldamallet)

    pprint("Ahora se presentará un gráfico que muestra los índices de coherencia de los distintos modelos para el modelado de entre 2 y 10 tópicos")

    def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
        """
        Compute c_v coherence for various number of topics

        Parameters:
        ----------
        dictionary : Gensim dictionary
        corpus : Gensim corpus
        texts : List of input texts
        limit : Max num of topics

        Returns:
        -------
        model_list : List of LDA topic models
        coherence_values : Coherence values corresponding to the LDA model with respective number of topics
        """
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values

    def compute_coherence_valuesLDA(dictionary, corpus, texts, limit, start=2, step=3):
        """
        Compute c_v coherence for various number of topics

        Parameters:
        ----------
        dictionary : Gensim dictionary
        corpus : Gensim corpus
        texts : List of input texts
        limit : Max num of topics

        Returns:
        -------
        model_list : List of LDA topic models
        coherence_values : Coherence values corresponding to the LDA model with respective number of topics
        """
        LDA_coherence_values = []
        LDA_model_list = []
        for num_topics in range(start, limit, step):
            model =  gensim.models.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=num_topics, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)
            LDA_model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            LDA_coherence_values.append(coherencemodel.get_coherence())

        return LDA_model_list, LDA_coherence_values


    # Can take a long time to run.
    model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=10, step=2) #MALLET
    LDA_model_list, LDA_coherence_values = compute_coherence_valuesLDA(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=10, step=2) #LDA

########### GENERANDO GRÁFICOS ##########
    # Show graph
    limit=10; start=2; step=2
    x = range(start, limit, step)
    plt.plot(x, coherence_values, label="Mallet")
    plt.plot(x, LDA_coherence_values, label="LDA")
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(loc='best')
    plt.title("Evaluación de los modelos")
   
    #plt.show()
    PLOTHPATH = os.path.join(Plots, "Modelsplot.png")
    plt.savefig(PLOTHPATH)
    
    # Print the coherence scores
    for m, cv in zip(x, coherence_values):
        print("Mallet Num Topics =", m, " has Coherence Value of", round(cv, 4))


########### GENERANDO GRÁFICOS ##########
    # Show graph
    #limit=10; start=2; step=2
    #x_lda = range(start, limit, step)
    #plt.plot(x_lda, LDA_coherence_values, label="LDA" )
    #plt.xlabel("Num Topics")
    #plt.ylabel("LDA Coherence score")
    #plt.legend(("LDA coherence_values"), loc='best')
    #plt.title("Evaluación con LDA")
    
    #plt.show()
    #plt.savefig('C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/static/LDAplot.png')
    
    # Print the coherence scores
    for m, cv in zip(x, LDA_coherence_values):
        print("LDA Num Topics =", m, " has Coherence Value of", round(cv, 4))
