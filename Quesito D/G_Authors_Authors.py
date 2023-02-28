# # ############################# DESCRIZIONE ###################################
# # # Nel seguente codice cerchiamo di andare ad analizzare i collegamenti tra gli Autori che hanno collaborato ad una stessa
# # # pubblicazione scientifica in ambito "Coronavirus" durante il periodo di riferimento indicato.
# # # Attraverso il grafo riusciamo a visualizzare:
# # # - I nodi, rappresentanti ogni singolo Autore,
# # # - Gli edge, che rappresentano i collegamenti tra Autori che hanno collaborato ad una stessa pubblicazione.
# #NB: E' possibile effettuare l'analisi  di prova suddividendo il Dataframe iniziale  in 70% e 30%
# e si analizza il 30% delle osservazioni al fine di allegerire il calcolo e visualizzare in tempi più brevi i grafi.
# #
# ### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# #####################################               CODICE                   #######################################
# ###################################################################################################################

# # ########################################## VERSIONE CON kamada_kawai_layout ##############################
# #Kamada-Kawai Layout è un algoritmo di NetworkX che posiziona i nodi di un grafo in modo che la somma delle energie
# potenziali dei nodi sia minima. Questo algoritmo utilizza un modello fisico di forze repulsive tra i nodi e
# forze attrattive tra i nodi connessi da un arco. Il risultato è un disegno del grafo che cerca di minimizzare
# l'intersezione degli archi e la sovrapposizione dei nodi. In generale, l'algoritmo di Kamada-Kawai Layout produce un disegno di grafo equilibrato e piacevole esteticamente.
# # ########################################## Import Packages  ##########################
import pandas as pd
import warnings
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
warnings.filterwarnings("ignore")


##########################################CARICAMENTO E PREPROCESSING ######################################
#Carichiamo i dati nel dataframe selezionando il periodo di riferimento desiderato:
df = pd.read_excel("./Dataset_Corona_2022_COMPLETO.xlsx")

##### Se si vuole allegerire il calcolo effettuare il seguente codice:
# #Creiamo un nuovo dataframe contenente il 30% delle osservazioni per alleggerire il calcolo
# Creating a dataframe with 70% values of original dataframe
df_part_1 = df.sample(frac = 0.95, random_state = 56)
# # Creating dataframe with rest of the 30% values
df_part_2 = df.drop(df_part_1.index)
# print(df_part_2)
df = df_part_2

# # #Creiamo un nuovo Dataframe che contiene le informazioni del Df originario, ma per ciascun Autore presente nelle righe
# della colonna "Authors"
df_authors = (
    df.assign(Authors= df["Authors"].astype(str).str.split(","))
        .explode("Authors")
        .drop_duplicates()
)
# print(df_authors)

# # ########################################## CREAZIONE GRAFO ################################
#Crea un grafo vuoto con:
G = nx.Graph()
# Crea un insieme di tutti gli autori univoci (nodi) con:
authors = set(df_authors["Authors"])
# print(authors)
# Aggiungi gli autori come nodi al grafo con:
G.add_nodes_from(authors)
# # Creaiamo un dizionario che associ a ogni PMID gli autori che hanno lavorato su quel PMID:
coauthors = {}
for pmid, group in df_authors.groupby("PMID"):
    coauthors[pmid] = list(group["Authors"])
# print(coauthors)
#
# Aggiungiamo gli archi al grafo tra coautori che hanno lo stesso PMID:
for pmid, authors in coauthors.items():
    for i, author1 in enumerate(authors):
        for author2 in authors[i+1:]:
            G.add_edge(author1, author2)

print("Number of nodes:", G.number_of_nodes())
print("\n\nNumber of edges:", G.number_of_edges())
print("\n\n\nG.degree =", G.degree)

##########################################################   BETWEENESS
#Convert the multigraph to a simple graph
G_simple = nx.Graph(G)
#Calculate betweenness centrality
betweenness = nx.betweenness_centrality(G_simple)
# Print the betweenness centrality of each node
bw_value = []
for node, bc in betweenness.items():
    print(f"Node {node} has betweenness centrality {bc:.5f}")
    bw_value.append(f"{bc:.5f}")
# print(bw_value)


#####################  COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES
edgelist = G.edges
dict_edges_occurences = {}
#
for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1
#
print("Il numero di EDGE per ciascuna coppia di nodi è: \n",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))




# ##################################   VISUALISATION ################
# #Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("Contact between Authors in (select the year)")

size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 15 )


pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color='red',
                       alpha=0.7)
nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)
nx.draw_networkx_labels(G, pos=pos,
                        labels=dict(zip(G.nodes,G.nodes)),
                        font_color='black',
                        font_size=2)

plt.axis('off')
plt.show()




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

print(top10_degree_nodes)
data = top10_degree_nodes
plt.bar(*zip(*data), color="red")
plt.title('Top 10 degree nodes')
plt.xlabel('Authors')
plt.ylabel('Collaborazioni')
plt.xticks(rotation=15)

plt.show()