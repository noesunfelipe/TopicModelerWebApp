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
import pandas as pd
import index as ind

MALLETPATH = ind.app.config['MALLET_PATH']
path = ind.app.config['UPLOAD_FOLDER']
TempData = ind.app.config['TEMP_DATA']
Plots = ind.app.config["STATIC"]
os.environ['MALLET_HOME'] = MALLETPATH
CSVPATH = ind.app.config["CLIENT_CSV"]


#Importar la data lematizada
DLPATH = os.path.join(TempData, "DL.json")
with open(DLPATH,'r') as f:
    DL = json.load(f)

#Importar el/los parámetros seleccionados por el usuario en el front
NTOPICSFINPATH = os.path.join(TempData, "NTopicsFin.json")
with open(NTOPICSFINPATH,'r') as parametros:
    NTopics_String = json.load(parametros)

#Importar el/los parámetros seleccionados por el usuario en el front
MODELOSELECTPATH = os.path.join(TempData, "ModeloSelec.json")
with open(MODELOSELECTPATH,'r') as ChosenModel:
    SelectedModel = json.load(ChosenModel)

#Importar el modelo final
if SelectedModel == "lda_model":
    LDAMODELFINPATH = os.path.join(TempData, "lda_model_fin.pkl")
    modelselected = pickle.load(open(LDAMODELFINPATH, "rb"))
    
else:
    LDAMALLETFINPATH = os.path.join(TempData, "ldamallet_fin.pkl")
    modelselected = pickle.load(open(LDAMALLETFINPATH, "rb"))


#Importar el/los parámetros seleccionados por el usuario en el front
CORPUSPATH = os.path.join(TempData, "corpus.json")
with open(CORPUSPATH,'r') as corp:
    corpus = json.load(corp)


ID2WORDPATH = os.path.join(TempData, "id2word.pkl")
id2word = pickle.load(open(ID2WORDPATH, "rb"))
#corpus = pickle.load(open("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.pkl", "rb"))



#corpus = corpora.MmCorpus("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/corpus.mm")
NTopics = int(NTopics_String)

print(corpus)

path = ind.app.config['UPLOAD_FOLDER']
for filename in os.listdir(path):
    #Archivo = table_list.append(filename)
    pathname = path + str("/")+str(filename)

df = pd.read_excel(os.path.join(pathname), engine='openpyxl')
print(pathname)

ID = df.caso_numero.values.tolist()
RecD = df.reclamo_descripcion.values.tolist()

def format_topics_sentences_mallet(modelselected, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    for i, row in enumerate(modelselected[corpus]):
        #row = row_list[0] if modelselected.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = modelselected.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    #Este texto es para probar la incorporación de los ID al documento final la segunda línea y el argumento IDs
    contents = pd.Series(texts)
    IDs = pd.Series(ID)
    sent_topics_df = pd.concat([sent_topics_df, contents, IDs], axis=1)
    #sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

def format_topics_sentences_lda(modelselected, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    for i, row_list in enumerate(modelselected[corpus]):
        row = row_list[0] if modelselected.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = modelselected.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    #Este texto es para probar la incorporación de los ID al documento final la segunda línea y el argumento IDs
    contents = pd.Series(texts)
    IDs = pd.Series(ID)
    sent_topics_df = pd.concat([sent_topics_df, contents, IDs], axis=1)
    #sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


if SelectedModel == "lda_model":
    df_topic_sents_keywords = format_topics_sentences_lda(modelselected=modelselected, corpus=corpus, texts=RecD)
    
else:
    df_topic_sents_keywords = format_topics_sentences_mallet(modelselected=modelselected, corpus=corpus, texts=RecD)





# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
#df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'reclamo_descripcion', 'ID']
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'reclamo_descripcion', 'ID']
# Show
df_dominant_topic.head(10)




# Group top 5 sentences under each topic
sent_topics_sorteddf_mallet = pd.DataFrame()

sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)

# Reset Index    
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

# Format
sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text", "caso_numero"]

# Show
sent_topics_sorteddf_mallet.head()



# Number of Documents for Each Topic
topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()

# Percentage of Documents for Each Topic
topic_contribution = round(topic_counts/topic_counts.sum(), 4)

# Topic Number and Keywords
topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']]

# Concatenate Column wise # Agregar el ID del df original a este ultimo DF
df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)

# Change Column names
df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']

# Show
df_dominant_topics


#Exportar los DF y cruzarlos con la base original

df_dominant_topic.head()
CSVFINALPATH = os.path.join(CSVPATH, "topico_dominante.csv")
df_dominant_topic.to_csv(CSVFINALPATH)

