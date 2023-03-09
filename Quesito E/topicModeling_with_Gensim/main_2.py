from pprint import pprint
import gensim
from gensim import models
import pandas as pd
from gensim import corpora
import LDA
import LSA
from generic_functions import process_words, visualize_topics, sent_to_words, format_topics_sentences,\
    show_topic_clusters, show_word_cloud, \
    show_results_coherence_plot
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
if __name__ == '__main__':
    ###     Setting general parameters:
    n_topics = 7
    n_words = 10
    start = 4
    limit = 11
    step = 1

    ###     Import del DataSet e formattazione:
    rows = pd.read_excel("./../Dataset_Corona_1949_1999_COMPLETO.xlsx").to_dict('records')
    dataset = pd.DataFrame(data=rows)
    dataset_Only_Abstract = dataset["Abstract"]
    data_words = list(sent_to_words(dataset_Only_Abstract))

    ###     Building bigram and trigram models:
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=150)  # higher threshold fewer phrases
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    data_ready = process_words(
        data_words,
        bigram_mod=bigram_mod,
        trigram_mod=trigram_mod
    )
    ###     Creazione Dictionary:
    id2word = corpora.Dictionary(data_ready)
    ###     Creazione Corpus: Term Document Frequency:
    corpus = [id2word.doc2bow(text) for text in data_ready]

    ####    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^     LDA:     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    print(f"\n\n ########## LATENT DIRICHLET ALLOCATION:    ############")
    print(f"\n^^^^ Contributo delle {n_words} parole più importanti per {n_topics} Topics: ^^^^")
    lda_model = LDA.create_lda_model(corpus, id2word, n_topics, n_words)
    ### Format:
    df_topic_sents_keywords = format_topics_sentences(model=lda_model, corpus=corpus, texts=data_ready)
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    print(f"\n^^^^ Analisi dei Topic Dominanti per ciascun Doc analizzato: ^^^^")
    print(df_dominant_topic.head(10))
    ### Visualize WordCloud for each Topics in LDA Model:
    print("\nVisualize WordCloud for each Topics in LDA Model... (Vedi grafico)")
    show_word_cloud(lda_model)




   ############ ^^^^^^^^^ Visualize HTML reports of topics and topic clusters: ^^^^^^^^^^^^^^^^
    #TOPIC CLUSTERS
    print(f"\n^^^^ Informazioni relative alla generazione dei Cluster: ^^^^")
    show_topic_clusters(lda_model, corpus, n_topics=n_topics)
    ### TOPICS TOP-30 MOST SALIENT TERMS:
    visualize_topics(lda_model, corpus)
#
#

### ^^^^^^^^^^^^^^^^^^^^^^^^^^^  Historical Trend Analysis 1949-1999:   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ###    Splitting dataset by year and creating separate corpus for each year:
    years = dataset["Publication Year"].unique()
    corpus_by_year = []
    for year in years:
        data_year = [doc for i, doc in enumerate(data_ready) if dataset["Publication Year"][i] == year]
        corpus_year = [corpus[i] for i, doc in enumerate(data_ready) if dataset["Publication Year"][i] == year]
        corpus_by_year.append((year, data_year, corpus_year))

    ###    LDA for each year and printing topics for each year:
    for year, data_year, corpus_year in corpus_by_year:
        print(f"\n\n ########## LATENT DIRICHLET ALLOCATION for Year {year}:    ############")
        lda_model_year = LDA.create_lda_model(corpus_year, id2word, n_topics, n_words)
        df_topic_sents_keywords_year = format_topics_sentences(model=lda_model_year, corpus=corpus_year,
                                                               texts=data_year)
        df_dominant_topic_year = df_topic_sents_keywords_year.reset_index()
        df_dominant_topic_year.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        print(f"\n^^^^ Analisi dei Topic Dominanti per ciascun Doc analizzato nell'anno {year}: ^^^^")
        print(df_dominant_topic_year.head(10))

