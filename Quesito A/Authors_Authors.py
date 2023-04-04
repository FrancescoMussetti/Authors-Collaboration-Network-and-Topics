######################################## CONTROLLO LIBRERIE ################################################

# Per rendere il codice riproducibile
import importlib
import subprocess

librerie_richieste = ['pandas', 'networkx', 'matplotlib', 'warnings',
                      'community','operator']

for lib in librerie_richieste:
    try:
        importlib.import_module(lib)
    except ImportError:
        subprocess.check_call(['pip', 'install', lib])

############################## IMPORTAZIONE LIBRERIE ##############################################
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import community as community_louvain
from operator import itemgetter

warnings.filterwarnings("ignore")

######################################### PULIZIA DEL DATASET ################################################
############################################### PARTE 1 ######################################################

# Importazione del dataset
df_completo = pd.read_excel("./Dataset_Corona_1949_2023_FINALE.xlsx")

############################################### PARTE 2 ######################################################

# Ai fini esplorativi abbiamo individuato due periodi da comparare, uno pre-pandemico (1949-2018)
# e uno post-pandemico (2019-2023)

# Creiamo il dataframe relativo all'intervallo temporale 1949-2018:
publication_year_interval = (1949, 2018)
df_49_18 = df_completo[(df_completo["Publication Year"] >= publication_year_interval[0]) & (df_completo["Publication Year"] <= publication_year_interval[1])]
print(df_49_18.shape[0])

# Il dataframe relativo all'intervallo temporale 1949-2018 consta di 14 414 osservazioni

# Creiamo il dataframe relativo all'intervallo temporale 2019-2023:
publication_year_interval = (2019, 2023)
df_19_23 = df_completo[(df_completo["Publication Year"] >= publication_year_interval[0]) & (df_completo["Publication Year"] <= publication_year_interval[1])]
print(df_19_23.shape[0])

# Il dataframe relativo all'intervallo temporale 2019-2023 consta di 209 969 osservazioni


# Creiamo due nuovi dataframe contenenti il 10% delle osservazioni per alleggerire il calcolo
# Qualora si volesse in futuro ripetere l'analisi con computer dotati di una maggiore potenza di calcolo
# tramite la variabile 'perc' è possibile modificare la percentuale di osservazioni del dataframe completo da
# destinare al campione

perc = 0.1

# Creiamo il campione del dataframe 1949-2018
df_part_1 = df_49_18.sample(frac = 1-perc, random_state = 123)
df_part_2 = df_49_18.drop(df_part_1.index)
df_49_18 = df_part_2

# Creiamo il campione del dataframe 2019-2023
df_part_1 = df_19_23.sample(frac = 1-perc, random_state = 123)
df_part_2 = df_19_23.drop(df_part_1.index)
df_19_23 = df_part_2

############################################### PARTE 3 ######################################################

# Creiamo un dizionario "esploso" per autore
# Sia per il periodo 1949-2018
df_authors_49_18 = (
    df_49_18.assign(Authors= df_49_18["Authors"].astype(str).str.strip().str.split(","))
        .explode("Authors")
        .drop_duplicates()
)
df_authors_49_18["Authors"] = df_authors_49_18["Authors"].str.strip()

# Sia per il periodo 2019-2023
df_authors_19_23 = (
    df_19_23.assign(Authors= df_19_23["Authors"].astype(str).str.strip().str.split(","))
        .explode("Authors")
        .drop_duplicates()
)
df_authors_19_23["Authors"] = df_authors_19_23["Authors"].str.strip()
# Le righe di questi dizionari hanno la forma
# PMID#1   .... AUTORE#1
# PMID#1   .... AUTORE#2
# PMID#1   .... AUTORE#3
# PMID#2   .... AUTORE#3
# PMID#2   .... AUTORE#4
# PMID#3   .... AUTORE#5
# PMID#3   .... AUTORE#6
# PMID#4   .... AUTORE#1
# PMID#5   .... AUTORE#7
# ......   .... ........

##################################### ANALISI GENERALI ##################################################

pd.set_option('display.max_rows', None)  # Visualizza tutte le righe della tabella
print(df_completo['Publication Year'].value_counts().sort_index())



############################################ CREAZIONE DEI GRAFI #########################################

# Procediamo con la creazione di due grafi per fini analitici, uno relativo a ciascun periodo

# 1949-2018

G_49_18 = nx.Graph()
# Creiamo un insieme di tutti gli autori univoci
authors = set(df_authors_49_18["Authors"])
# Facciamo in modo che ciascun nodo del grafo coincida con gli autori
G_49_18.add_nodes_from(authors)
# Creiamo un dizionario che associ a ogni PMID gli autori che hanno lavorato su quell'articolo
coauthors = {}
for pmid, group in df_authors_49_18.groupby("PMID"):
    coauthors[pmid] = list(group["Authors"])
# Aggiungiamo gli archi al grafo per coautori che hanno lo stesso PMID:
for pmid, authors in coauthors.items():
    for i, author1 in enumerate(authors):
        for author2 in authors[i+1:]:
            G_49_18.add_edge(author1, author2)

# 2019-2023

G_19_23 = nx.Graph()
# Creiamo un insieme di tutti gli autori univoci
authors = set(df_authors_19_23["Authors"])
# Facciamo in modo che ciascun nodo del grafo coincida con gli autori
G_19_23.add_nodes_from(authors)
# Creiamo un dizionario che associ a ogni PMID gli autori che hanno lavorato su quell'articolo
coauthors = {}
for pmid, group in df_authors_19_23.groupby("PMID"):
    coauthors[pmid] = list(group["Authors"])
# Aggiungiamo gli archi al grafo per coautori che hanno lo stesso PMID:
for pmid, authors in coauthors.items():
    for i, author1 in enumerate(authors):
        for author2 in authors[i+1:]:
            G_19_23.add_edge(author1, author2)


################################## EVENTUALI FILTRI DA APPORRE AL GRAFO #######################################

# # Estraggo un sottografo che abbia solo nodi di almeno un grado pari a k
# k_degree=10
# sub_k_degree = grafo.subgraph([node for node, degree in dict(grafo.degree()).items() if degree >= k_degree])
# # Il codice in questione va modificato tenendo conto del nome dato al grafo

############################################## ANALISI DEI GRAFI ##########################################
################################################## MISURE #################################################

# pulizia dei grafi
G_49_18.remove_node('et al')
G_19_23.remove_node('et al')

lista_grafi=[G_49_18,G_19_23]

def confronta_grafi(lista_grafi,k):
    # Per ogni grafo nella lista
    for i, graph in enumerate(lista_grafi):
        if i < len(lista_grafi) - 1:
            print(f"Confronto tra il {i + 1}° e il {i + 2}° grafo")

        # Identifica i primi k nodi con il grado più alto
        top_nodes = sorted(nx.degree(graph), key=lambda x: x[1], reverse=True)[:k]

        # Se ci sono altri grafi nella lista
        if i < len(lista_grafi) - 1:
            # Identifica i primi k nodi con il grado più alto dell'altro grafo
            other_graph = lista_grafi[i + 1]
            other_top_nodes = sorted(nx.degree(other_graph), key=lambda x: x[1], reverse=True)[:k]

            # Determina i nodi in comune
            common_nodes = set([node[0] for node in top_nodes]).intersection(set([node[0] for node in other_top_nodes]))
            num_common_nodes = len(common_nodes)

            # Stampa il numero di nodi in comune
            if num_common_nodes!=0:
                print(f"Gli autori in comune nelle prime {k} posizioni in termini di grado del nodo tra il {i + 1}° e il {i + 2}° grafo sono: {num_common_nodes}")
            else:
                print(f"Non ci sono autori in comune nelle prime {k} posizioni in termini di grado del nodo")

            # Stampa la posizione dei nodi in comune nell'altro grafo e nel grafo in questione
            for node in top_nodes:
                if node[0] in common_nodes:
                    index_other = [j for j, n in enumerate(other_top_nodes) if n[0] == node[0]][0]
                    index_self = [j for j, n in enumerate(top_nodes) if n[0] == node[0]][0]
                    print(
                        f"L'autore '{node[0]}' si trovava nella posizione {index_self + 1} nel {i + 1}° grafo, mentre nel {i + 2}° grafo si trova nella posizione {index_other + 1}")

def analizza_grafi(lista_grafi):
    k=25
    for i,G in enumerate(lista_grafi):
        print(f"Analizziamo il {i+1}° grafo")
        print("L'ordine del grafo, ossia il numero di nodi, è pari a", G.order())
        print("La dimensione del grafo, corrispondente al numero di lati, è",G.size())
        nodes_and_degrees = [(node, G.degree(node)) for node in G]
        sorted_nodes_and_degrees = sorted(nodes_and_degrees, key=lambda x: x[1], reverse=True)
        top_nodes_and_degrees = sorted_nodes_and_degrees[:k]
        print(f"I {k} nodi del {i+1}° grafo con il più alto grado sono:",top_nodes_and_degrees)
        if i < len(lista_grafi) - 1:
            confronta_grafi([G, lista_grafi[i + 1]],k)
        print("La densità di un grafo, definita come il rapporto tra il numero di lati "
              "e il numero massimo di lati che il grafo potrebbe avere,\n"
              "è una misura che varia da 0 a 1:"
              "un grafo con densita' > 0.5 e' considerato denso,"
              "un grafo con densita' < 0.5 e' considerato sparso")
        print(f"La densità del {i+1}° grafo è pari a",round(nx.density(G),3))
        print("Il grado medio del grafo, pari al rapporto tra la somma del grado di tutti i nodi"
              "e il numero dei nodi del grafo, è pari a",round(sum(dict(G.degree()).values())/(G.order()),3))
        if nx.is_connected(G):
            print("esiste almeno un sentiero tra ogni coppia di nodi del grafo oppure, in altri termini \n"
                  "tutti i nodi del grafo sono raggiungibili da qualsiasi altro nodo attraverso uno o piu' lati")
            print(f"Il {i+1}° grafo è connesso")
            print("La distanza media, misura applicabile solamente a un grafo connesso\n"
                  "o a una sua componente connessa, corrispondente alla distanza media tra \n"
                  "tutte le coppie di nodi del grafo"
                  "è pari a", round(nx.average_shortest_path_length(G), 3),)
        else:
            print(f"Il {i+1}° grafo non è connesso")
            print("Nel grafo è infatti possibile individuare", nx.number_connected_components(G), "componenti")
            print("Tra esse, quella più grande, che prende il nome di sottografo indotto, è composta da",
                  G.subgraph(max(nx.connected_components(G), key=len)).order(),"nodi")
        print('\n')

analizza_grafi(lista_grafi)

########################################## ANALISI GRAFICA DEL GRAFO #########################################
####################################### BRIDGE E PUNTI DI ARTICOLAZIONE ######################################

# Per il periodo 1949-2018
# creiamo un grafo in cui vengono selezionati da quello principale
# solamente i nodi con un grado superiore a 15, al fine di migliorarne la visualizzazione
grafo = G_49_18.copy()

k_degree=15
grafo = grafo.subgraph([node for node, degree in dict(grafo.degree()).items() if degree >= k_degree])

# Creiamo un set di punti di articolazione e bridge
# I punti di articolazione sono quei nodi di un grafo la cui rimozione
# aumenta il numero di componenti connesse del grafo stesso.
# In altre parole, se si rimuove un punto di articolazione dal grafo,
# si suddivide in più parti distinte.
articulation_points = set(nx.articulation_points(grafo))
# Un bridge è un lato (o un insieme di archi) che, se rimosso dal grafo, 
# aumenta il numero di componenti connesse del grafo stesso. 
# In altre parole, un bridge è un arco che è essenziale per la connettività del grafo 
# e la sua rimozione divide il grafo in due o più parti distinte.
bridges = set(nx.bridges(grafo))

# Individuaiamo i nodi che fanno parte di archi che sono bridge
bridge_nodes = []
for u, v in bridges:
    bridge_nodes.append(u)
    bridge_nodes.append(v)

bridge_nodes = list(set(bridge_nodes))

# Stampiamo i nodi di articolazione e i bridge come set di stringhe
print("I punti di articolazione del grafo 1949-2018 sono: ", {str(node) for node in articulation_points})
print("I nodi che fanno parte dei bridge del grafo 1949-2018 sono: ", {str(node) for node in bridge_nodes})

# Calcoliamo l'intersezione come set di stringhe
intersection = {str(node) for node in articulation_points} & {str(node) for node in bridge_nodes}
print(intersection)

# Creiamo un dizionario che assegna i colori ai nodi e imposta le etichette solo per i nodi di interesse
node_colors = {}
labels = {}
for node in grafo.nodes():
    if str(node) in intersection:
        node_colors[node] = 'green'
        labels[node] = str(node)
    elif str(node) in articulation_points:
        node_colors[node] = 'blue'
        labels[node] = str(node)
    elif str(node) in bridge_nodes:
        node_colors[node] = 'red'
        labels[node] = str(node)
    else:
        node_colors[node] = 'black'
        labels[node] = ''

# Creiamo un dizionario che assegna il colore rosso ai lati che sono bridge
bridge_colors = {edge: 'red' for edge in bridges}

# Creiamo un dizionario che assegna le dimensioni ai nodi
# in modo da distinguere punti di articolazione e nodi facente parte dei bridge
# dal resto dei nodi
node_sizes = {}
for node in grafo.nodes():
    if str(node) in intersection or str(node) in articulation_points or str(node) in bridge_nodes:
        node_sizes[node] = 200
    else:
        node_sizes[node] = 1.5

# Disegniamo il grafo con etichette e colori per i nodi di interesse
pos = nx.kamada_kawai_layout(grafo)
nx.draw_networkx_nodes(grafo, pos=pos, node_shape='d',node_color=list(node_colors.values()), node_size=list(node_sizes.values()))
nx.draw_networkx_edges(grafo, pos=pos, edge_color='black', width=0.02)
nx.draw_networkx_labels(grafo, pos=pos, labels=labels, font_size=10, font_color='white',bbox=dict(facecolor='black', alpha=0.75, boxstyle='round4'),font_weight="bold",font_family='sans-serif',verticalalignment='top')
nx.draw_networkx_edges(grafo, pos=pos, edgelist=bridges, edge_color='red', width=1.5)
# Creiamo la legenda
legend_labels = {
    'Punti di articolazione': 'blue',
    'Bridge': 'red',
    'Nodi che sono sia punti di articolazione che facenti parte di bridge': 'green'
}
plt.legend(handles=[plt.Line2D([], [], color=color, label=label) for label, color in legend_labels.items()], loc='best')

# Salviamo il grafo sotto forma di svg 
# (si può modificare la risoluzione dell'immagine - ridurre a 300 se troppo "pesante")
plt.savefig('Grafo bridge 49_18 degree_15.svg', dpi=1800, pad_inches=0)

# Mostriamo il grafo
plt.show()


# Ripetiamo lo stesso procedimento anche per il periodo 2019-2023
# scegliendo però questa volta un filtro in termini di grado dei nodi pari a 100
# al fine di ridurre la numerosità
grafo = G_19_23.copy()

k_degree=100
grafo = grafo.subgraph([node for node, degree in dict(grafo.degree()).items() if degree >= k_degree])

articulation_points = set(nx.articulation_points(grafo))
bridges = set(nx.bridges(grafo))

bridge_nodes = []
for u, v in bridges:
    bridge_nodes.append(u)
    bridge_nodes.append(v)

bridge_nodes = list(set(bridge_nodes))

print("I punti di articolazione del grafo 2019-2023 sono: ", {str(node) for node in articulation_points})
print("I nodi che fanno parte dei bridge del grafo 2019-2023 sono: ", {str(node) for node in bridge_nodes})

intersection = {str(node) for node in articulation_points} & {str(node) for node in bridge_nodes}
print(intersection)

node_colors = {}
labels = {}
for node in grafo.nodes():
    if str(node) in intersection:
        node_colors[node] = 'green'
        labels[node] = str(node)
    elif str(node) in articulation_points:
        node_colors[node] = 'blue'
        labels[node] = str(node)
    elif str(node) in bridge_nodes:
        node_colors[node] = 'red'
        labels[node] = str(node)
    else:
        node_colors[node] = 'black'
        labels[node] = ''

bridge_colors = {edge: 'red' for edge in bridges}

node_sizes = {}
for node in grafo.nodes():
    if str(node) in intersection or str(node) in articulation_points or str(node) in bridge_nodes:
        node_sizes[node] = 200
    else:
        node_sizes[node] = 1.5

pos = nx.kamada_kawai_layout(grafo)
print("fatto 6")
nx.draw_networkx_nodes(grafo, pos=pos, node_shape='d',node_color=list(node_colors.values()), node_size=list(node_sizes.values()))
print("fatto 7")
nx.draw_networkx_edges(grafo, pos=pos, edge_color='black', width=0.02)
print("fatto 8")
nx.draw_networkx_labels(grafo, pos=pos, labels=labels, font_size=10, font_color='white',bbox=dict(facecolor='black', alpha=0.75, boxstyle='round4'),font_weight="bold",font_family='sans-serif',verticalalignment='top')
nx.draw_networkx_edges(grafo, pos=pos, edgelist=bridges, edge_color='red', width=1.5)

legend_labels = {
    'Punti di articolazione': 'blue',
    'Bridge': 'red',
    'Nodi che sono sia punti di articolazione che facenti parte di bridge': 'green'
}
plt.legend(handles=[plt.Line2D([], [], color=color, label=label) for label, color in legend_labels.items()], loc='best')

plt.savefig('Grafo bridge 19_23 degree_100.svg', dpi=1800, pad_inches=0)

plt.show()

############################################## CLUSTERING #################################################

# Per ogni periodo considerato abbiamo analizzato il sottografo indotto,
# ossia la componente connessa più grande del grafo
# Analizzare tutto il grafo sarebbe stato troppo oneroso da un punto
# di vista computazionale

# Per il periodo 1949-2018 scegliamo di eliminare i nodi che hanno un grado inferiore a 15
k_degree = 15

grafo = G_49_18.copy()
grafo_49_18 = grafo.subgraph([node for node, degree in dict(grafo.degree()).items() if degree >= k_degree])

# Individuiamo la componente connessa più grande
componente_massima_49_18 = max(nx.connected_components(grafo_49_18), key=len)
sottografo_indotto_49_18 = grafo.subgraph(componente_massima_49_18)


# Individua i cluster tramite l'algoritmo di Louvain
# L'algoritmo di Louvain è un algoritmo di clustering gerarchico per grafi.
# Cerca di dividere un grafo in gruppi (cluster) di nodi in modo che i nodi all'interno
# di ciascun cluster siano fortemente connessi tra loro, mentre i nodi in cluster diversi siano poco connessi.
# In sintesi, l'algoritmo di Louvain cerca di ottimizzare una funzione di modularità
# che misura la densità dei collegamenti all'interno dei cluster rispetto ai collegamenti tra i cluster,
# e utilizza questo criterio per suddividere il grafo in cluster.
# Rispetto all'algoritmo di Girvan-Newman, basato sulla betweenness dei lati, Louvain consente
# la gestione di grafi di grandi dimensioni e ordine.
partition_49_18 = community_louvain.best_partition(sottografo_indotto_49_18)

# Individuiamo i 10 nodi con il più alto valore di betweenness centrality all'interno del sottografo indotto
betweenness = nx.betweenness_centrality(sottografo_indotto_49_18)
top_betweenness_49_18 = dict(sorted(betweenness.items(), key=itemgetter(1), reverse=True)[:10])

# Generiamo una lista di colori dei nodi basato sulla partizione di Louvain
color_list = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'midnightblue', 'ivory', 'cyan', 'magenta', 'lime', 'olive', 'gold', 'navy', 'teal', 'maroon', 'coral', 'turquoise', 'indigo', 'silver', 'orchid', 'violet', 'khaki', 'salmon', 'tan', 'lavender', 'dimgray']

# Creiamo un dizionario che associa ad ogni cluster il suo colore
color_dict = {cluster: color_list[i % len(color_list)] for i, cluster in enumerate(set(partition_49_18.values()))}

# Associamo a ogni nodo del sottografo un colore
node_colors = [color_dict[partition_49_18[node]] for node in sottografo_indotto_49_18.nodes()]

# Disegniamo il grafo colorando ciascun nodo in base al cluster di appartenenza
pos = nx.kamada_kawai_layout(sottografo_indotto_49_18)
nx.draw_networkx_nodes(sottografo_indotto_49_18, pos, node_color=node_colors, node_size=75,edgecolors='black', linewidths=0.2)
nx.draw_networkx_edges(sottografo_indotto_49_18, pos, width=0.1)

# Rappresentiamo le etichette dei 10 nodi con il più alto valore di betweenness
top_betweenness_labels = {k: k for k in top_betweenness_49_18}
for node, label in top_betweenness_labels.items():
    nx.draw_networkx_labels(sottografo_indotto_49_18, {node: pos[node]}, labels={node: label},
                            font_size=10, font_color=color_dict[partition_49_18[node]], bbox=dict(facecolor='black', alpha=0.75, boxstyle='round4'))

# Creiamo una legenda
handles = []
for cluster in set(partition_49_18.values()):
    handles.append(plt.scatter([],[], color=color_dict[cluster]))
plt.legend(handles, [f'Cluster {cluster}' for cluster in set(partition_49_18.values())], loc='upper right', title='Clusters')

# Stampiamo a video il numero di cluster individuati
num_clusters = len(set(partition_49_18.values()))
print(f"Numero di cluster individuati: {num_clusters}")

# Mostriamo i nodi per ogni cluster e il relativo colore così da facilitarne l'analisi grafica
for cluster in set(partition_49_18.values()):
    print(f"\nCluster {cluster} - colore: {color_dict[cluster]}")
    nodes = [node for node in sottografo_indotto_49_18.nodes() if partition_49_18[node] == cluster]
    print(f"Nodi: {nodes}")

# Salviamo la figura
plt.savefig('Cluster 49_18 degree_15.svg', dpi=1800, pad_inches=0)

# Mostriamo il grafico
plt.show()


# Ripetiamo il procedimento anche per il periodo 2019-2023
# Questa volta impostiamo un filtro per il grado dei nodi da analizzare pari a 100
k_degree = 100

grafo = G_19_23.copy()
grafo_19_23 = grafo.subgraph([node for node, degree in dict(grafo.degree()).items() if degree >= k_degree])

componente_massima_19_23 = max(nx.connected_components(grafo_19_23), key=len)
sottografo_indotto_19_23 = grafo.subgraph(componente_massima_19_23)


partition_19_23 = community_louvain.best_partition(sottografo_indotto_19_23)

betweenness = nx.betweenness_centrality(sottografo_indotto_19_23)
top_betweenness_19_23 = dict(sorted(betweenness.items(), key=itemgetter(1), reverse=True)[:10])

color_list = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'midnightblue', 'ivory', 'cyan', 'magenta', 'lime', 'olive', 'gold', 'navy', 'teal', 'maroon', 'coral', 'turquoise', 'indigo', 'silver', 'orchid', 'violet', 'khaki', 'salmon', 'tan', 'lavender', 'dimgray']

color_dict = {cluster: color_list[i % len(color_list)] for i, cluster in enumerate(set(partition_19_23.values()))}

node_colors = [color_dict[partition_19_23[node]] for node in sottografo_indotto_19_23.nodes()]

pos = nx.kamada_kawai_layout(sottografo_indotto_19_23)
nx.draw_networkx_nodes(sottografo_indotto_19_23, pos, node_color=node_colors, node_size=75,edgecolors='black', linewidths=0.2)
nx.draw_networkx_edges(sottografo_indotto_19_23, pos, width=0.1)

top_betweenness_labels = {k: k for k in top_betweenness_19_23}
for node, label in top_betweenness_labels.items():
    nx.draw_networkx_labels(sottografo_indotto_19_23, {node: pos[node]}, labels={node: label},
                            font_size=10, font_color=color_dict[partition_19_23[node]], bbox=dict(facecolor='black', alpha=0.75, boxstyle='round4'))

handles = []
for cluster in set(partition_19_23.values()):
    handles.append(plt.scatter([],[], color=color_dict[cluster]))
plt.legend(handles, [f'Cluster {cluster}' for cluster in set(partition_19_23.values())], loc='upper right', title='Clusters')

num_clusters = len(set(partition_19_23.values()))
print(f"Numero di cluster individuati: {num_clusters}")

for cluster in set(partition_19_23.values()):
    print(f"\nCluster {cluster} - colore: {color_dict[cluster]}")
    nodes = [node for node in partition_19_23.nodes() if partition_19_23[node] == cluster]
    print(f"Nodi: {nodes}")

plt.savefig('Cluster 19_23 degree_100.svg', dpi=1800, pad_inches=0)

plt.show()