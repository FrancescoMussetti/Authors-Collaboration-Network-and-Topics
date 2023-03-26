
import gensim
from gensim.utils import simple_preprocess
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyLDAvis
from pyLDAvis.gensim_models import prepare
import seaborn as sns
import spacy
from bokeh.io import output_notebook
from bokeh.plotting import figure, output_file, save
# NLTK Stop words
from nltk.corpus import stopwords
from sklearn.manifold import TSNE
from wordcloud import WordCloud
stop_words = stopwords.words('english')
stop_words.extend(
    ['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get',
     'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack',
     'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])
def sent_to_words(sentences):
    for sent in sentences:
        sent = gensim.utils.simple_preprocess(str(sent), deacc=True)
        yield (sent)
def process_words(texts,
                  stop_words=stop_words,
                  allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'],
                  bigram_mod=None,
                  trigram_mod=None):
    """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
    texts = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
    texts = [bigram_mod[doc] for doc in texts]
    texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
    texts_out = []
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 10000000
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    # remove stopwords once more after lemmatization
    texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]
    return texts_out
def format_topics_sentences(model=None, corpus=None, texts=None):
    # Init output
    sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row_list in enumerate(model[corpus]):
        if len(row_list) == 0:
            continue
        row = row_list[0] if model.per_word_topics else row_list
        if isinstance(row, tuple):
            row = [row]
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(
                    pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return (sent_topics_df)
def visualize_topics(model, corpus):
    vis = prepare(model, corpus, dictionary=model.id2word, mds='mmds')
    pyLDAvis.save_html(vis, './report/topic_modeling_visualization.html')
def show_topic_clusters(model, corpus, n_topics=10):
    topic_weights = []
    for i, row_list in enumerate(model[corpus]):
        topic_weights.append([w for i, w in row_list[0]])
    # Array of topic weights
    arr = pd.DataFrame(topic_weights).fillna(0).values
    # Keep the well separated points (optional)
    arr = arr[np.amax(arr, axis=1) > 0.35]
    # Dominant topic number in each doc
    topic_num = np.argmax(arr, axis=1)
    # tSNE Dimension Reduction
    # t-distributed Stochastic Neighbor Embedding
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
    tsne_lda = tsne_model.fit_transform(arr)
    # Plot the Topic Clusters using Bokeh
    output_notebook()
    file_name = 'report/topic_modeling_clusters.html'
    output_file(file_name)
    mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
    plot = figure(title="t-SNE Clustering of {} LDA Topics".format(n_topics),
                  plot_width=900, plot_height=700)
    plot.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], color=mycolors[topic_num])
    save(plot)
def show_word_cloud(model):
    for t in range(model.num_topics):
        plt.figure()
        plt.imshow(WordCloud().fit_words(dict(model.show_topic(t, 200))))
        plt.axis("off")
        plt.show()
def show_results_coherence_plot(model, coherence_values, start, limit, step):
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.title(model)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence"), loc='best')
    plt.show()

def plot_topic_evolution(lda_model, corpus, dataset):
    # Get yearly topic distributions
    yearly_topic_distributions = {}
    for i, doc in enumerate(corpus):
        year = dataset.iloc[i]["Publication Year"]
        if year not in yearly_topic_distributions:
            yearly_topic_distributions[year] = [0] * lda_model.num_topics
        topics = lda_model.get_document_topics(doc)
        for topic in topics:
            topic_id = topic[0]
            topic_weight = topic[1]
            yearly_topic_distributions[year][topic_id] += topic_weight

    # Plot topic evolution over years
    fig, ax = plt.subplots()
    for i in range(lda_model.num_topics):
        topic_id = i
        topic_evolution = []
        for year in sorted(yearly_topic_distributions.keys()):
            topic_evolution.append(yearly_topic_distributions[year][topic_id])
        ax.plot(sorted(yearly_topic_distributions.keys()), topic_evolution, label=f"Topic {topic_id}")
    ax.legend()
    ax.set_xlabel('Year')
    ax.set_ylabel('Topic Frequency')
    ax.set_title('Evolution of Topics')
    plt.show()