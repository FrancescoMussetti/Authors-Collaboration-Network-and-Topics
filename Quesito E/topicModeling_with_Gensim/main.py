import matplotlib.pyplot as plt
import gensim
from gensim import models
import pandas as pd
from gensim import corpora
from wordcloud import WordCloud

import LDA
from generic_functions import process_words, visualize_topics, sent_to_words, format_topics_sentences,\
    show_topic_clusters, show_word_cloud,plot_topic_evolution
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
if __name__ == '__main__':
    ###     Setting general parameters:
    n_topics = 6
    n_words = 10
    start = 4
    limit = 11
    step = 1

    ###     Import del DataSet e formattazione:
    rows = pd.read_excel("./../../Dataset/Dataset_Corona_2000_2019_FINALE.xlsx").to_dict('records')
    dataset = pd.DataFrame(data=rows)
    dataset.dropna(subset=["Abstract"], inplace=True)  # rimuove le righe con abstract vuoti
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

    ##########^^^^^^^^^ Visualize the Evolution of Topics during the Years"
    plot_topic_evolution(lda_model, corpus, dataset)
    ### Format:
    df_topic_sents_keywords = format_topics_sentences(model=lda_model, corpus=corpus, texts=data_ready)
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    print(f"\n^^^^ Analisi dei Topic Dominanti per ciascun Doc analizzato: ^^^^")
    print(df_dominant_topic.head(10))


    ##===### Visualize WordCloud for each Topics in LDA Model:
    def show_word_cloud(lda_model, n_topics=6, n_words=20):
        topics = lda_model.show_topics(num_topics=n_topics, num_words=n_words, formatted=False)
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        for i, ax in enumerate(axs.ravel()):
            if i < n_topics:
                words = dict(topics[i][1])
                wc = WordCloud(background_color='black', max_words=200, width=800, height=400)
                wc.generate_from_frequencies(words)
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                ax.set_title(f"WordCloud Topic#{i }")
        plt.tight_layout()
        plt.show()

    print("\nVisualize WordCloud for each Topics in LDA Model... (Vedi grafico)")
    show_word_cloud(lda_model)


   ############ ^^^^^^^^^ Visualize HTML reports of topics and topic clusters: ^^^^^^^^^^^^^^^^
    #TOPIC CLUSTERS
    print(f"\n^^^^ Informazioni relative alla generazione dei Cluster: ^^^^")
    show_topic_clusters(lda_model, corpus, n_topics=n_topics)
    ### TOPICS TOP-30 MOST SALIENT TERMS:
    visualize_topics(lda_model, corpus)




   ################ CREATE & EXPORT DATASET WITH TOPICS #################################################
    ## Creazione del nuovo dataset
    df_new = pd.concat([dataset, df_dominant_topic[['Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords']]], axis=1)
    df_new.dropna(inplace=True)
   # ## Esporta il DataFrame contenente le informazioni sui Topic per ogni Doc in un file Excel
   #  df_new.to_excel('Dataset_Corona_1949_2023_TOPIC.xlsx', index=False, sheet_name='Sheet1', startrow=0, startcol=0)


# ### ^^^^^^^^^^^^^^^^^^^^^^^^^^^  Historical Trend Analysis for year (****) :   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    for year in range(1949, 2000):
        year_dataset = dataset.loc[dataset['Publication Year'] == year]
        if not year_dataset.empty:
            year_abstracts = year_dataset['Abstract']
            year_words = list(sent_to_words(year_abstracts))
            year_data_ready = process_words(year_words, bigram_mod=bigram_mod, trigram_mod=trigram_mod)
            year_id2word = corpora.Dictionary(year_data_ready)
            year_corpus = [year_id2word.doc2bow(text) for text in year_data_ready]
            year_lda_model = LDA.create_lda_model(year_corpus, year_id2word, n_topics, n_words)
            year_topics = year_lda_model.show_topics(num_topics=n_topics, num_words=n_words, formatted=False)
            print(f"Contributo delle 10 parole più importanti per {n_topics} Topics per l'Anno {year}:")
            print()
            for topic in year_topics:
                print(f"Topic {topic[0]}:")
                print(f"({topic[1]})")
                print(f"{' '.join([word[0] for word in topic[1]])}\n")