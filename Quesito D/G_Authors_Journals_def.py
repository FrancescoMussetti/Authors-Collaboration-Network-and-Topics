############################## DESCRIZIONE ###################################
# Nel seguente codice cerchiamo di andare ad analizzare i collegamenti tra i vari Autori
# di una pubblicazione scientifica in ambito "Coronavirus" e Rivista o Libro di pubblicazione
# della stessa durante il periodo di riferimento.
# Attraverso il grafo riusciamo a visualizzare:
# - I nodi, suddivisi in "ROSSI" se riferiti ai "Journal/Book","BLU" se riferiti agli "Authors",
# - Gli edge, che rappresentano i collegamenti tra Autore e Rivista di pubblicazione.


######################################## CODICE #######################################
#######################################################################################

########################################## Import Packages  ##########################
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib

matplotlib.use('TkAgg')
##########################################CARICAMENTO E PREPROCESSING ######################################
# CARICHIAMO IL DATASET
# df = pd.read_excel("./Dataset_Corona_2023_COMPLETO.xlsx")
df = pd.read_excel(
    r"C:\Users\ilari\Documents\economia dei network\Network-Economy\Quesito C\Dataset_Corona_1949_2023_FINALE.xlsx",
    usecols=range(0, 6), index_col=None)  # , nrows=100) #, names=["Authors","Journal/Book"])

# publication_year_interval = (1949, 2019)
publication_year_interval = (2020, 2023)

# seleziona solo le righe che rientrano nell'intervallo di anni desiderato
df = df[
    (df["Publication Year"] >= publication_year_interval[0]) & (df["Publication Year"] <= publication_year_interval[1])]
df = (df[df.Authors.str.contains(',', case=False)])

print(df.head())
# #Creiamo un nuovo dataframe contenente il 30% delle osservazioni per alleggerire il calcolo
# Creating a dataframe with 70% values of original dataframe
# df_part_1 = df.sample(frac = 0.95, random_state = 45)
# # # Creating dataframe with rest of the 30% values
# df_part_2 = df.drop(df_part_1.index)
# df = df_part_2


# Creiamo un nuovo Dataframe che contiene le informazioni del Df originario, ma per ciascun Autore presente nella colonna "Authors"
df_authors = (
    df.assign(Authors=df["Authors"].astype(str).str.split(", "))
        .explode("Authors")
        .drop_duplicates()
)
df_authors = df_authors.dropna()
# print(df_authors)

########################################## CREAZIONE GRAFO ################################
G = nx.from_pandas_edgelist(df_authors, "Authors", "Journal/Book", create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("\n\nNumber of edges:", G.number_of_edges())

print("\n\n\nG.degree =", G.degree)

# Il valore del grado minimo (in questo caso 20) può essere modificato a seconda delle
# esigenze specifiche.
# # Compute the node degree
degree = nx.degree(G)
# Create a list of nodes with high degree
high_degree_nodes = [node for node, d in degree if d >= 500]
# Create a subgraph with only high degree nodes
G_high_degree = G.subgraph(high_degree_nodes)
G = G_high_degree

# isolated_node=nx.isolates(G)
# len(list(isolated_node))
#
# G.remove_nodes_from(list(nx.isolates(G)))
len(G.nodes)

################################################   BETWEENESS:
# Convert the multigraph to a simple graph
G_simple = nx.Graph(G)

# Calculate betweenness centrality
betweenness = nx.betweenness_centrality(G_simple)
#
# # Print the betweenness centrality of each node
bw_value = []
for node, bc in betweenness.items():
    # print(f"Node {node} has betweenness centrality {bc:.5f}")
    bw_value.append(f"{bc:.5f}")
# bw_value = [value for value in bw_centrality.values()]
# quantiles = np.quantile(bw_value, [0.25, 0.5, 0.75])          ### FORSE ELIMINABILE
#
################################## #COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES:
edgelist = G.edges
dict_edges_occurences = {}
#
for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

print("Il numero di EDGE per ciascuna coppia di nodi è: \n",
      sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))

##################################   VISUALISATION ################
###Questo codice in Python crea un grafico che visualizza i contatti tra autori e riviste/libri nel 2016.
# Il grafico viene creato utilizzando la libreria "matplotlib" e il grafo è rappresentato da un oggetto "G".
# Il codice inizia creando un oggetto "fig" e "ax" utilizzando la funzione "plt.subplots" e impostando
# la dimensione del grafico. Un titolo viene assegnato al grafico utilizzando "fig.suptitle".
# Successivamente, il codice crea una mappa colore che assegna il colore "blu" ai nodi che
# rappresentano gli autori e il colore "rosso" ai nodi che rappresentano le riviste/libri.
# Questo viene fatto verificando se il nome del nodo esiste nella colonna "Authors" del dataframe "df_authors".
# Inoltre, viene creata una mappa di dimensioni che assegna la dimensione di ogni nodo in base al
# loro grado di ingresso. Questo viene fatto moltiplicando il grado di ingresso di un nodo per 7.
# Infine, il codice crea una legenda per il grafico utilizzando "Line2D". La legenda specifica che i nodi
# rappresentati con cerchi rossi rappresentano le riviste/libri e i nodi rappresentati
# con cerchi blu rappresentano gli autori.

## #Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("Contact between Authors and Journal/Book in 2020-2023")
# Add a color attribute to each node based on its column value
color_map = []
for node in G.nodes():
    if node in df_authors["Authors"].values:
        color_map.append("blue")
    else:
        color_map.append("red")

size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 7)

############# LEGENDA ##############
legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='Journal/Book', markerfacecolor='red', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Authors', markerfacecolor='blue', markersize=13), ]

############### ????????????????????????????  TENTATIVP DI FILTRAGGIO PER DEGREE ???????????????????????????????????? ##################
### In questo codice, prima si calcola il grado dei nodi utilizzando la funzione nx.degree,
#### quindi si crea una lista di nodi con grado maggiore o uguale a 20. Infine, si crea
# un sottografo utilizzando la funzione subgraph che contiene solo i nodi
# con grado maggiore e si visualizza il sottografo utilizzando la funzione nx.draw.
# Il valore del grado minimo (in questo caso 20) può essere modificato a seconda delle
# esigenze specifiche.
# # Compute the node degree
# degree = nx.degree(G)
# # Create a list of nodes with high degree
# high_degree_nodes = [node for node, d in degree if d >= 20]
# # Create a subgraph with only high degree nodes
# G_high_degree = G.subgraph(high_degree_nodes)
# G = G_high_degree
##################################### ??????????????????????? ############################


#
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

############# LEGGENDA ##############
ax.legend(handles=legend_elements1, loc='best')
plt.axis('off')
plt.show()

#
####################     TOP 10 IN-DEGREE NODES: ##########################
# Questo codice in Python calcola e visualizza i primi 10 nodi con il più alto grado di ingresso in un grafo.
# Il grado di ingresso di un nodo è definito come il numero di archi che entrano in un nodo.
# Il codice inizia creando un dizionario "degrees_dict" che mappa i nomi dei nodi ai loro gradi di ingresso.
# Questo viene fatto iterando su una lista "degrees" che contiene i gradi di ingresso per ogni nodo.
# Successivamente, la lista "degrees_list" viene ordinata in ordine decrescente in base ai gradi di ingresso
# utilizzando la funzione "sorted" con una funzione di ordinamento lambda che ordina gli elementi in base
# al valore di "x[1]".
# Il codice quindi seleziona i primi 10 elementi della lista ordinata e li assegna a "top10_degree_nodes".
# Infine, il codice crea un grafico a barre usando la libreria "matplotlib" che visualizza i primi 10 nodi con
# il più alto grado di ingresso. La barra viene etichettata con un titolo, etichette per l'asse x e y, e
# le barre sono ruotate di 15 gradi.
# La funzione "plt.show()" viene chiamata alla fine per visualizzare il grafico.


degrees_dict = {}
for t in degrees:
    degrees_dict[t[0]] = t[1]

degrees_list = sorted(degrees_dict.items(), key=lambda x: x[1], reverse=True)
top10_degree_nodes = degrees_list[:10]

colors = []
for node in top10_degree_nodes:
    if node[0] in df_authors["Authors"].values:
        colors.append("blue")
    else:
        colors.append("red")

print(top10_degree_nodes)
data = top10_degree_nodes
plt.bar(*zip(*data), color=colors)
plt.title('Top 10 degree nodes')
plt.xlabel('Journal/Authors')
plt.ylabel('Collaborazioni')
plt.xticks(rotation=15)

plt.show()

degrees_dict_authors = {key: value for (key, value) in degrees_dict.items() if
                        key not in df['Journal/Book'].unique().tolist()}
degrees_list_authors = sorted(degrees_dict_authors.items(), key=lambda x: x[1], reverse=True)
top10_degree_nodes_authors = degrees_list_authors[:10]

print(top10_degree_nodes_authors)
data = top10_degree_nodes_authors
plt.bar(*zip(*data), color="blue")
plt.title('Top 10 degree authors')
plt.xlabel('Authors')
plt.ylabel('Collaborazioni')
plt.xticks(rotation=15)

plt.show()

degrees_dict_journals = {key: value for (key, value) in degrees_dict.items() if
                         key in df['Journal/Book'].unique().tolist()}
degrees_list_journals = sorted(degrees_dict_journals.items(), key=lambda x: x[1], reverse=True)
top10_degree_nodes_journals = degrees_list_journals[:10]

print(top10_degree_nodes_journals)
data = top10_degree_nodes_journals
plt.bar(*zip(*data), color="red")
plt.title('Top 10 degree nodes')
plt.xlabel('Journal/Book')
plt.ylabel('Collaborazioni')
plt.xticks(rotation=15)

plt.show()