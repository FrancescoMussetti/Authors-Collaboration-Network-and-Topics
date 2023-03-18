import pandas as pd
import Docs_Normalization
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
#plotting tools
import matplotlib.pyplot as plt
def plot_top_words(model, feature_names, n_top_words, title):
    fig, axes = plt.subplots(1, 8, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic {topic_idx + 1}',
                     fontdict={'fontsize': 30})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)
    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()
if __name__ == '__main__':
    ### ^^^^^^^^^^^^^^^^^^ Import DataSet ^^^^^^^^^^^^^^^^^^
    rows = pd.read_excel("./../Dataset_Corona_2023_COMPLETO.xlsx").to_dict('records')
    dataset = pd.DataFrame(data=rows)
    dataset = dataset.dropna()
    dataset_Only_Abstract = dataset["Abstract"].dropna()
    # ### ^^^^^^^^^^^^^^^^^^  Choosing best parameters with GridSearch  ^^^^^^^^^^^^^^^^^^
    print("Choosing Optimal Hyperparameter ")
    parameters = {
        'vect__max_features': [1000, 1500],
        'vect__ngram_range': [[1, 2]],
        'model__n_components': [n_topic for n_topic in range(4, 11)],
        'model__learning_decay': [.50, .75, .90]
    }
    pipe = Pipeline([
        ('vect', CountVectorizer(
            tokenizer=Docs_Normalization.tokenizer,
            max_df=0.8,
            min_df=0.2)),
        ('model', LatentDirichletAllocation(
            random_state=2))
    ])
    grid_search = GridSearchCV(pipe, parameters, n_jobs=-1)
    grid_search.fit(dataset_Only_Abstract)
    print("Best Score Likelyhood: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))