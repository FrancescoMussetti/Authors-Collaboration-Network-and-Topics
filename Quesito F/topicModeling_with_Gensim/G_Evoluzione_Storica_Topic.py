import pandas as pd
import matplotlib.pyplot as plt

# Caricamento del dataset
dataset = pd.read_excel("Dataset_Corona_1949_2023_TOPIC.xlsx")

def plot_topic_evolution(dataset, start_year=None, end_year=None):
    # Raggruppamento per topic e anno e conteggio del numero di articoli per ogni gruppo
    df = dataset.groupby(["Dominant_Topic", "Publication Year"]).size().reset_index(name="Count")

    # Filtraggio per anno di inizio e fine, se specificati
    if start_year is not None:
        df = df[df["Publication Year"] >= start_year]
    if end_year is not None:
        df = df[df["Publication Year"] <= end_year]

    # Pivot del dataframe per avere i topic come colonne e gli anni come indice
    df_pivot = df.pivot(index="Publication Year", columns="Dominant_Topic", values="Count").fillna(0)

    # Plot delle linee spezzate per ogni topic
    fig, ax = plt.subplots()
    for topic in df_pivot.columns:
        ax.plot(df_pivot.index, df_pivot[topic], label=f"Topic {topic}")
    ax.legend()
    ax.set_xlabel('Anno')
    ax.set_ylabel('Frequenza del Topic')
    ax.set_title('Evoluzione dei Topic')
    plt.show()

plot_topic_evolution(dataset,start_year=2015,end_year=2023)