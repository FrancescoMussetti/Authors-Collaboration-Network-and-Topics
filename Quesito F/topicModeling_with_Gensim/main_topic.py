import matplotlib.pyplot as plt
import gensim
from gensim import models
import pandas as pd
from gensim import corpora
from wordcloud import WordCloud

import LDA
from generic_functions import process_words, visualize_topics, sent_to_words, format_topics_sentences, \
    show_topic_clusters, show_word_cloud, plot_topic_evolution
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

if __name__ == '__main__':
    # Setting general parameters:
    n_topics = 6
    n_words = 10
    start = 4
    limit = 11
    step = 1

    # Import del DataSet e formattazione:
    dataset = pd.read_excel("./../../Dataset/Dataset_Corona_1949_2023_FINALE.xlsx")
    print(dataset.isna().sum())
    dataset = dataset.dropna()
    print(dataset.isna().sum())

    # Prepare data for LDA:
    dataset_Only_Abstract = dataset["Abstract"]
    data_words = list(sent_to_words(dataset_Only_Abstract))

    # Building bigram and trigram models:
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=150)  # higher threshold fewer phrases
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    data_ready = process_words(
        data_words,
        bigram_mod=bigram_mod,
        trigram_mod=trigram_mod
    )

    # Create Dictionary:
    id2word = corpora.Dictionary(data_ready)

    # Create Corpus (Term Document Frequency):
    corpus = [id2word.doc2bow(text) for text in data_ready]

    # LDA Model:
    print(f"\n\n ########## LATENT DIRICHLET ALLOCATION:    ############")
    print(f"\n^^^^ Contributo delle {n_words} parole più importanti per {n_topics} Topics: ^^^^")
    lda_model = LDA.create_lda_model(corpus, id2word, n_topics, n_words)
    # Format topics and sentences:
    df_topic_sents_keywords = format_topics_sentences(model=lda_model, corpus=corpus, texts=data_ready)
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

    # Add PMID column:
    pmid_list = dataset['PMID'].tolist()
    df_dominant_topic['PMID'] = pmid_list

    ################ CREATE & EXPORT DATASET WITH TOPICS #################################################
    # Merge the two dataframes based on PMID:
    df_new = pd.merge(dataset, df_dominant_topic[['PMID', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords']],
                      on='PMID', how='inner')
    # Export the DataFrame containing topic information for each document to an Excel file:
    df_new.to_excel('Dataset_Corona_1949_2023_TOPIC_new.xlsx', index=False, sheet_name='Sheet1', startrow=0, startcol=0)

    ##===### Visualize WordCloud for each Topics in LDA Model:
    print("\nVisualize WordCloud for each Topics in LDA Model... (Vedi grafico)")
    show_word_cloud(lda_model)


############ ^^^^^^^^^ Visualize HTML reports of topics and topic clusters: ^^^^^^^^^^^^^^^^
    #TOPIC CLUSTERS
    print(f"\n^^^^ Informazioni relative alla generazione dei Cluster: ^^^^")
    show_topic_clusters(lda_model, corpus, n_topics=n_topics)
    ### TOPICS TOP-30 MOST SALIENT TERMS:
    visualize_topics(lda_model, corpus)


    # Visualize the Evolution of Topics during the Years:
    plot_topic_evolution(lda_model, corpus, dataset)

