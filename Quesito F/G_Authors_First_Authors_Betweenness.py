################################ DESCRIZIONE ###################################
### Nel seguente codice riprendiamo l'analisi effettuata sui collegamenti tra gli Autori che hanno collaborato
### ad una stessa pubblicazione scientifica in ambito "Coronavirus" durante il periodo di riferimento indicato.
###  Nel dettaglio andremo ad indagare come i Primi Autori si posizionano all'interno del grafo in termini di livelli Degree e
### di Betweenneess che presentano gli stessi,  in modo da evidenziare, per quanto possibie, se i Primi Autori risultano essere
### autori con un maggior numero di collaborazioni ed in particolare se gli stessi svolgano un ruolo di "ponte" tra due o più gruppi di
## autori e che abbiano una posizione importante nel passaggio delle informazioni tra le varie sotto-comunità scientifiche.

### In particolare il seguente codice genera quattro distinti grafici:

### 1) Il primo è il grafo  attraverso il quale riusciamo a visualizzare:
### - I nodi, rappresentanti ogni singolo Autore, colorati in base al fatto che essi siano Primi Autori (BLU) o Autori Secondari (ROSSO) e
### le cui dimensioni sono date dalla rispettiva Degree (numero di archi in entrata), dunque maggiore degree maggiore grandezza del nodo.
# # # - Gli edge, che rappresentano i collegamenti tra Autori che hanno collaborato ad una stessa pubblicazione,
# dove lo spessore dell'edge è rappresentativo del peso dello stesso, quindi di quante collaborazioni hanno effettivamente avuto i due autori collegati.

### 2) Il secondo è un grafico a barre  attraverso il quale riusciamo a visualizzare:
### - La Degree dei primi 20 Nodi con maggior degree pesata per numero di collaborazioni e dunque l'elenco dei rispettivi
### 20 Autori con maggiori collaborazioni, colorati come detto precedentemente.


### 3) Il terzo è un grafico a barre  attraverso il quale riusciamo a visualizzare:
### - La Betweenness Centrality dei primi 20 Nodi con maggior betweenness e dunque l'elenco dei rispettivi
### 20 Autori  con una centralità di intermediazione elevata che potrebbero avere una posizione privilegiata nel grafo,
### agendo come intermediari chiave nel facilitare la comunicazione o la collaborazione tra altri autori o gruppi di autori che altrimenti
### potrebbero non essere direttamente connessi, anch'essi colorati come detto precedentemente.


### 3) Il quarto è un' insieme di sottografi attraverso il quale riusciamo a visualizzare:
### - Tutti i sottografi generati dall'eliminazione dei 20 Autori con maggior betweenness individuati
### precedentemente, in modo da darci un'idea del carico informativo che questi nodi possedevano, anch'essi colorati
### come indicato precedentemente.



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
import matplotlib.patches as mpatches
import plotly.express as px
from collections import Counter
warnings.filterwarnings("ignore")

##########################################CARICAMENTO E PREPROCESSING ######################################
#Carichiamo i dati nel dataframe selezionando il periodo di riferimento desiderato:
df = pd.read_excel("./Dataset/Dataset_Corona_1949_2023_FINALE.xlsx")
# definisci l'intervallo di anni  da analizzare desiderato:
publication_year_interval = (1949, 1999)
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
authors = df_authors["Authors"].value_counts()[df_authors["Authors"].value_counts() >= 1].index.tolist()
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


# Calcola la degree di ogni nodo del grafo
degrees = dict(G.degree())
# Imposta il valore di soglia della degree da considerare nel filtro
degree_filter = 5
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
for node, bc in betweenness.items():
    print(f"Node {node} has betweenness centrality {bc:.5f}")
    bw_value.append(f"{bc:.5f}")
print(bw_value)


##################### ^^^^^^  COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES ^^^^^^
edgelist = G.edges
dict_edges_occurences = {}
#
for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

# print("Il numero di EDGE per ciascuna coppia di nodi è: \n",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))

# ##################################   VISUALISATION ################
# Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("Contact between Authors in (select the year)")

size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 15)

pos = nx.kamada_kawai_layout(G)

# Creare una lista di colori per i nodi in base alla presenza nella colonna "First Author"
node_colors = []
for node in G.nodes:
    if node in df['First Author'].values:
        node_colors.append('blue')
    else:
        node_colors.append('red')

nx.draw_networkx_nodes(G, pos=pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color=node_colors,  # Utilizzare la lista di colori creata
                       alpha=0.7)
nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist=dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)

# Get top 20 nodes by betweenness
sorted_nodes = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:20]
# Create dictionary of labels for top 20 nodes
top20_labels = {node[0]: node[0] for node in sorted_nodes}
nx.draw_networkx_labels(G, pos=pos,
                        labels=top20_labels,
                        font_color='black',
                        font_size=6)

# Aggiungere una legenda per i colori
blue_patch = mpatches.Patch(color='blue', label='First Author')
red_patch = mpatches.Patch(color='red', label='Secondary Author')
plt.legend(handles=[blue_patch, red_patch], loc='best', prop={'size': 12})

plt.axis('off')
plt.show()


####################     TOP 20 IN-DEGREE NODES: ##########################

degrees_dict = {}
for t in degrees:
    degrees_dict[t[0]] = t[1]

degrees_list = sorted(degrees_dict.items(), key=lambda x: x[1], reverse=True)
top20_degree_nodes = degrees_list[:20]

# Creare una lista di colori per le barre in base alla presenza nella colonna "First Author"
bar_colors = []
for node in top20_degree_nodes:
    if node[0] in df['First Author'].values:
        bar_colors.append('blue')
    else:
        bar_colors.append('red')

data = top20_degree_nodes
fig, ax = plt.subplots(figsize=(12, 8))
plt.bar(*zip(*data), color=bar_colors)
plt.title('Top 20 Autori con la maggior Degree')
plt.xlabel('Authors')
plt.ylabel('Collaborazioni')


# Aggiungi una legenda per i colori
blue_patch = mpatches.Patch(color='blue', label='First Author')
red_patch = mpatches.Patch(color='red', label=' Secondary Author')
plt.legend(handles=[blue_patch, red_patch], loc='best')

plt.xticks(rotation=90)
plt.show()


######## TOP 20 BETWEENNESS NODES #####################

# Ordina i nodi in base alla betwenness centrality in ordine decrescente
sorted_nodes = sorted(betweenness, key=betweenness.get, reverse=True)
# Seleziona i primi 20 autori con la maggior betwenness centrality
top_20_authors = sorted_nodes[:20]
# Estrai i valori di betwenness centrality per i primi 20 autori
top_20_bc = [betweenness[node] for node in top_20_authors]

# Creazione lista di colori per le barre del grafico
bar_colors = []
for author in top_20_authors:
    if author in df['First Author'].values:
        bar_colors.append('blue')
    else:
        bar_colors.append('red')

# Crea il grafico a barre
fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(top_20_authors, top_20_bc, color=bar_colors) # Utilizza la lista di colori creata
ax.set_xlabel('Autori')
ax.set_ylabel('Betweenness Centrality')
ax.set_title('Top 20 Autori con la maggior Betweenness Centrality')

# Aggiungi una legenda per i colori
blue_patch = mpatches.Patch(color='blue', label='First Author')
red_patch = mpatches.Patch(color='red', label=' Secondary Author')
plt.legend(handles=[blue_patch, red_patch], loc='best')

plt.xticks(rotation=90)
plt.show()



# Creare una copia modificabile del grafo originale
G_copy = G.copy()

# Sort the nodes based on their betweenness centrality in descending order
sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
# Get the top 20 nodes with the highest betweenness centrality
top_nodes = [node[0] for node in sorted_nodes[:20]]
# Remove the top 20 nodes from the graph
G_copy.remove_nodes_from(top_nodes)
# Calculate the connected components in the remaining graph
subgraphs = list(nx.connected_components(G_copy))
# Print the number of subgraphs generated
print("Number of subgraphs generated:", len(subgraphs))

# Create a dictionary to store node colors
node_colors = {}

# Iterate through the nodes in the graph
for node in G_copy.nodes():
    # Check if the node is present in the "First Author" column of the main dataframe
    if node in df['First Author'].values:
        node_colors[node] = 'blue'  # Set color to blue
    else:
        node_colors[node] = 'red'  # Set color to red

# Visualize the subgraphs generated by the splits
fig, axs = plt.subplots(7, 4, figsize=(20, 30), tight_layout=True)

for i, subgraph_nodes in enumerate(subgraphs):
    if i < 7 * 4:
        ax = axs[i // 4][i % 4]
        subgraph = G_copy.subgraph(subgraph_nodes)
        # Draw nodes with specified colors
        node_color = [node_colors[node] for node in subgraph.nodes()]
        nx.draw(subgraph, with_labels=True, ax=ax, node_color=node_color)
        ax.set_title(f"Subgraph {i+1}")
        ax.axis('off')

# Create a legend
blue_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10)
red_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10)
axs[4][3].legend([blue_patch, red_patch], ['First Author', ' Secondary Author'])

plt.show()