################################ DESCRIZIONE ###################################
### Nel seguente codice riprendiamo l'analisi effettuata sui collegamenti tra gli Autori che hanno collaborato
### ad una stessa pubblicazione scientifica in ambito "Coronavirus" durante il periodo di riferimento indicato.
###  Nel dettaglio andremo a integrare l'analisi precedente con le informazioni ottenute dalla Topic Modeling precedentemente
### effettuata in modo da individuare, per quanto possibile, gli argomenti trattati da ogni singolo autore nel periodo di riferimento
### e visualizzandoli direttamente nel grafo attraverso un codice colore che identifica i differenti Topic.

### In particolare il seguente codice genera due distinti grafici:

### 1) Il primo è il grafo  attraverso il quale riusciamo a visualizzare:
### - I nodi, rappresentanti ogni singolo Autore, colorati in base al Topic maggiormente trattato da quel autore nel periodo di riferimento e
### le cui dimensioni sono date dalla rispettiva Degree (numero di archi in entrata), dunque maggiore degree maggiore grandezza del nodo.
# # # - Gli edge, che rappresentano i collegamenti tra Autori che hanno collaborato ad una stessa pubblicazione,
# dove lo spessore dell'edge è rappresentativo del peso dello stesso, quindi di quante collaborazioni hanno effettivamente avuto i due autori collegati.

### 2) Il secondo è un grafico a barre sovrapposte attraverso il quale riusciamo a visualizzare:
### - La Degree dei primi 10 Nodi con maggior degree pesata per numero di collaborazioni e dunque l'elenco dei rispettivi 10 Autori con maggiori collaborazioni.
### - Le proporzioni di ciascun Topic trattato da ogni singolo autore della TOP10 nel periodo di riferimento.

### Un maggior grado di dettaglio è fornito per ciascun blocco di codice è fornito a seguire:


### NB: E' possibile effettuare l'analisi  di prova suddividendo il Dataframe iniziale  in parti minori e si analizza
### il dataset frazionato  al fine di allegerire il calcolo e visualizzare in tempi più brevi i grafi.


### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#####################################               CODICE                   #######################################
###################################################################################################################
########################################## Import Packages  ##########################
from matplotlib.lines import Line2D
import random
import pandas as pd
import warnings
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
warnings.filterwarnings("ignore")

##########################################CARICAMENTO E PREPROCESSING ######################################
#Carichiamo i dati nel dataframe selezionando il periodo di riferimento desiderato:
df = pd.read_excel("./Dataset_Topic/Dataset_Corona_1949_2023_TOPIC.xlsx")
# definisci l'intervallo di anni  da analizzare desiderato:
publication_year_interval = (2019, 2023)
# seleziona solo le righe che rientrano nell'intervallo di anni desiderato
df = df[(df["Publication Year"] >= publication_year_interval[0]) & (df["Publication Year"] <= publication_year_interval[1])]


# #### Se si vuole allegerire il calcolo effettuare il seguente codice:
# #### Seleziona casualmente il 95% delle righe del dataframe:
# df_part_1 = df.sample(frac=0.95, random_state=1234)
# # Seleziona il restante 5% delle righe del dataframe:
# df_part_2 = df.drop(df_part_1.index)
# df = df_part_2

# # #Creiamo un nuovo Dataframe che contiene le informazioni del Df originario, ma per ciascun Autore presente
# nelle righe della colonna "Authors", inoltre ripuliamo da tutti i possibili caratteri indesidrati.
df_authors = (
    df.assign(Authors=df["Authors"].astype(str).str.strip().str.split(","))
    .explode("Authors")
    .drop_duplicates()

)
df_authors["Authors"] = df_authors["Authors"].str.strip()

# Selezionare le righe contenenti "et al" e eliminarle
df_authors = df_authors.loc[df_authors["Authors"] != "et al"].copy()


# Filtriamo gli autori che hanno un numero di pubblicazioni maggiore di (scegliere il valore):
authors = df_authors["Authors"].value_counts()[df_authors["Authors"].value_counts() >= 2].index.tolist()
df_authors = df_authors[df_authors["Authors"].isin(authors)]

# ########################################## CREAZIONE GRAFO ################################
#### Crea un grafo vuoto con:
G = nx.Graph()
# Aggiungi gli autori come nodi al grafo con:
G.add_nodes_from(authors)

# Creaiamo un dizionario che associ a ogni PMID gli autori che hanno lavorato su quel PMID:
coauthors = {}
for pmid, group in df_authors.groupby("PMID"):
    coauthors[pmid] = list(group["Authors"])
# Aggiungiamo gli archi al grafo tra coautori che hanno lo stesso PMID:
for pmid, authors in coauthors.items():
    for i, author1 in enumerate(authors):
        for author2 in authors[i+1:]:
            G.add_edge(author1, author2)

# print("Number of nodes:", G.number_of_nodes())
# print("\n\nNumber of edges:", G.number_of_edges())
# print("\n\n\nG.degree =", G.degree)

# Calcola la degree di ogni nodo del grafo
degrees = dict(G.degree())
# Imposta il valore di soglia della degree da considerare nel filtro
degree_filter = 200
# Filtra i nodi in base alla degree
nodes_filtered = [node for node, degree in degrees.items() if degree >= degree_filter]
# Crea un sottografo che include solo i nodi filtrati
G_filtered = G.subgraph(nodes_filtered)
# # Visualizza il numero di nodi e di archi del grafo filtrato
# print("Number of nodes:", len(G_filtered.nodes))
# print("Number of edges:", len(G_filtered.edges))

G=G_filtered

#########################################################   BETWEENESS   #######################################################
# Convert the multigraph to a simple graph
G_simple = nx.Graph(G)
# Calculate betweenness centrality
betweenness = nx.betweenness_centrality(G_simple)
# Print the betweenness centrality of each node
bw_value = []
# for node, bc in betweenness.items():
#     print(f"Node {node} has betweenness centrality {bc:.5f}")
#     bw_value.append(f"{bc:.5f}")
# print(bw_value)


# #####################  COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES ####################################################
edgelist = G.edges
dict_edges_occurences = {}
#
for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1
#
# print("Il numero di EDGE per ciascuna coppia di nodi è: \n",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))


# # ##################################   VISUALISATION ##############################
# # ##########################################  kamada_kawai_layout ##############################
## #Kamada-Kawai Layout è un algoritmo di NetworkX che posiziona i nodi di un grafo in modo che la somma delle energie
## potenziali dei nodi sia minima. Questo algoritmo utilizza un modello fisico di forze repulsive tra i nodi e
## forze attrattive tra i nodi connessi da un arco. Il risultato è un disegno del grafo che cerca di minimizzare
## l'intersezione degli archi e la sovrapposizione dei nodi.
## In generale, l'algoritmo di Kamada-Kawai Layout produce un disegno di grafo equilibrato e piacevole esteticamente.

#Nel seguente grafo, rispetto ai precedenti, viene associato ad ogni autore anche il topic trattato dallo stesso.
### Dato che però un autore può trattare più topic nello stesso periodo di riferimento, si è optato per calcolare il
### numero di ciascun topic trattato da ciascun autore e assegnare all'autore il colore associato al topic da lui maggiormente trattato.

### Visualizzazione del grafico
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("Collaborazioni tra Autori durante (select the year) evidenziati secondo Topic di riferimento")
#### Troviamo il numero di topic con maggiori occorrenze per ciascun autore:
author_topics = {}
for idx, row in df_authors.iterrows():
    author = row["Authors"]
    topic = row["Dominant_Topic"]
    if author not in author_topics:
        author_topics[author] = [0] * 6  # inizializza la lista dei conteggi dei topic a zero per ogni autore
    author_topics[author][topic] += 1  # aggiorna il conteggio del topic per l'autore corrente
### Stampa i conteggi dei topic per ogni autore:
# for author, topic_counts in author_topics.items():
#     print(f"Autor: {author} - Conteggi dei Topic: {topic_counts}")

### Assegnamo il topic con maggiori occorrenze ai rispettivi nodi e li coloriamo di conseguenza:
color_map = []
for node in G.nodes():
    if node in author_topics:
        topic_counts = author_topics[node]
        most_common_topics = [i for i, x in enumerate(topic_counts) if x == max(topic_counts)]
        if len(most_common_topics) == 1:  # if there's a clear most common topic
            node_color = most_common_topics[0]
        else:  # if there's a tie for most common topic, choose one randomly
            node_color = random.choice(most_common_topics)
        if node_color == 0:
            color_map.append("blue")
        elif node_color == 1:
            color_map.append("orange")
        elif node_color == 2:
            color_map.append("green")
        elif node_color == 3:
            color_map.append("red")
        elif node_color == 4:
            color_map.append("#8B00FF")
        elif node_color == 5:
            color_map.append("#654321")
        else:
            color_map.append("gray")  # default color for nodes not found in the dataframe
    else:
        color_map.append("gray")  # default color for nodes not found in the dataframe

### Stabiliamo la grandezza di ciascun nodo in base alla sua Degree (Maggiore Degree = Maggiore Dimensione):
size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 7)

pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G, pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color=color_map,
                       alpha=0.7)
nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist=dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)

##### Data l'elevata numerosita dei nodi,al fine di rilevare solo i nodi d'interesse e non
# creare sovrapposizione tra le etichette, si puo decidere di evidenziare tutti i nomi
# degli autori o solo i primi 10 con maggiori livelli di Degree.
# _____________________________________________________________________
#### Per visualizzare i nomi dei primi 10 autori nel grafico, eseguire:
# Get top 10 nodes by degree
top10_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
# Create dictionary of labels for top 10 nodes
top10_labels = {node[0]: node[0] for node in top10_nodes}
nx.draw_networkx_labels(G, pos=pos,
                        labels=top10_labels,
                        font_color='black',
                        font_size=6)
# _____________________________________________________________________
# Se invece si vogliono visualizzare tutti i nomi, eseguire il seguente codice:

# nx.draw_networkx_labels(G, pos=pos,
#                         labels=dict(zip(G.nodes,G.nodes)),
#                         font_color='black',
#                         font_size=4)
# _____________________________________________________________________

############# LEGENDA ##############
# Creiamo i dettagli della Legenda
legend_elements1 = [
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 0', markerfacecolor='blue', markersize=13),
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 1', markerfacecolor='orange', markersize=13),
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 2', markerfacecolor='green', markersize=13),
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 3', markerfacecolor='red', markersize=13),
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 4', markerfacecolor='#8B00FF', markersize=13),
    Line2D([0], [0], marker='o', color='w', label='Dominant_Topic 5', markerfacecolor='#654321', markersize=13)
]
ax.legend(handles=legend_elements1, loc='lower right', prop={'size': 30})
plt.axis('off')
plt.show()



###======================================================================================
# ####################     TOP 10 IN-DEGREE NODES CON EVIDENZA DI TUTTI I TOPICS TRATTATI ##########################
### Questo codice in Python calcola e visualizza i primi 10 nodi con il più alto grado di ingresso in un grafo.
### Il grado di ingresso di un nodo è definito come il numero di archi che entrano in un nodo.
### In questo caso si utilizza il codice colore associato ai 6 Topic trovati con la Topic Modeling per colorare
### i primi 10 Autori NON SOLO secondo il topic trattato maggiormente per il periodo di riferimento, ma andando a visualizzare
### tutte le proporzioni di Topics trattate da ogni singolo autore tramite un grafico a Barre sovrapposte, dando un'informazione
### molto piu accurata rispetto al grafico precedente e utile in accoppiamento al grafo.


degrees_dict = {}
for t in degrees:
    degrees_dict[t[0]] = t[1]

### Ordina il dizionario dei degree in ordine decrescente e seleziona i primi 10 autori:
top_authors = sorted(degrees_dict.items(), key=lambda x: x[1], reverse=True)[:10]
top_author_names = [a[0] for a in top_authors]
### Crea una lista di colori per i diversi topic:
colors = ['blue','orange','green','red' ,'#8B00FF',"#654321" ]
### Crea il grafico a barre sovrapposte:
fig, ax = plt.subplots(figsize=(10, 6))

for i, author in enumerate(top_author_names):
    author_topics2 = author_topics[author]
    segments = []
    for j, topic in enumerate(author_topics2):
        segments.append(degrees_dict[author] * topic)
    ax.bar(i, degrees_dict[author], color='white', edgecolor='black')
    ax.bar(i, segments[0], color=colors[0], edgecolor='black')
    ax.bar(i, segments[1], bottom=segments[0], color=colors[1], edgecolor='black')
    ax.bar(i, segments[2], bottom=sum(segments[:2]), color=colors[2], edgecolor='black')
    ax.bar(i, segments[3], bottom=sum(segments[:3]), color=colors[3], edgecolor='black')
    ax.bar(i, segments[4], bottom=sum(segments[:4]), color=colors[4], edgecolor='black')
    ax.bar(i, segments[5], bottom=sum(segments[:5]), color=colors[5], edgecolor='black')

#### Aggiungi etichette e titolo al grafico:
ax.set_xticks(range(len(top_author_names)))
ax.set_xticklabels(top_author_names, rotation=30, ha='right')
ax.set_ylabel('Degree pesata per numero di collaborazioni')
ax.set_title('Top 10 Author Degree by Dominant Topic')

plt.show()

# ================================

