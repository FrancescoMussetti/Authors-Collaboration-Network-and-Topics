############################## DESCRIZIONE ###################################
# Nel seguente codice cerchiamo di andare ad analizzare i collegamenti tra Autori principali
# di una pubblicazione scientifica in ambito "Coronavirus" e Rivista o Libro di pubblicazione
#della stessa durante il periodo di riferimento.
#Attraverso il grafo riusciamo a visualizzare:
# - I nodi, suddivisi in "ROSSI" se riferiti ai "Journal/Book","VERDI" se riferiti ai "First Author",
# - Gli edge, che rappresentano i collegamenti tra Autore Principale e Rivista Scientifica.


######################################## CODICE #######################################
#######################################################################################

########################################## Import Packages  ##########################
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns

##########################################CARICAMENTO E PREPROCESSING ######################################
# CARICHIAMO IL DATASET
df = pd.read_excel("./Dataset_Corona_2023_GENERALE.xlsx")

# #Creiamo un nuovo dataframe contenente il 30% delle osservazioni per alleggerire il calcolo
# Creating a dataframe with 70% values of original dataframe
df_part_1 = df.sample(frac = 0.7, random_state = 49)
# # Creating dataframe with rest of the 30% values
df_part_2 = df.drop(df_part_1.index)
df = df_part_2


########################################## CREAZIONE GRAFO ################################
G=nx.from_pandas_edgelist(df, "First Author", "Journal/Book",create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("\n\nNumber of edges:", G.number_of_edges())
print("\n\n\nG.degree =", G.degree)


####################   BETWEENESS
#Convert the multigraph to a simple graph
G_simple = nx.Graph(G)
#Calculate betweenness centrality
betweenness = nx.betweenness_centrality(G_simple)
# Print the betweenness centrality of each node
bw_value = []
for node, bc in betweenness.items():
    print(f"Node {node} has betweenness centrality {bc:.3f}")
    bw_value.append(f"{bc:.3f}")


##############################   COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES
edgelist = G.edges
dict_edges_occurences = {}
#
for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

print("Il numero di EDGE per ciascuna coppia di nodi è: \n",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))

# ##################################   VISUALISATION ################
# ###Questo codice in Python crea un grafico che visualizza i contatti tra autori principali e riviste/libri.
# # Il grafico viene creato utilizzando la libreria "matplotlib" e il grafo è rappresentato da un oggetto "G".
# # Il codice inizia creando un oggetto "fig" e "ax" utilizzando la funzione "plt.subplots" e impostando
# # la dimensione del grafico. Un titolo viene assegnato al grafico utilizzando "fig.suptitle".
# #Successivamente, il codice crea una mappa colore che assegna il colore "blu" ai nodi che
# # rappresentano gli autori principali e il colore "rosso" ai nodi che rappresentano le riviste/libri.
# # Questo viene fatto verificando se il nome del nodo esiste nella colonna "First Author" del dataframe.
# #Inoltre, viene creata una mappa di dimensioni che assegna la dimensione di ogni nodo in base al
# # loro grado di ingresso. Questo viene fatto moltiplicando il grado di ingresso di un nodo per 7.
# # Infine, il codice crea una legenda per il grafico utilizzando "Line2D". La legenda specifica che i nodi
# # rappresentati con cerchi rossi rappresentano le riviste/libri e i nodi rappresentati
# # con cerchi blu rappresentano gli autori.
#
## #Visualize the graph
fig, ax = plt.subplots(figsize=(100, 100))
fig.suptitle("Contact between First Authors and Journal/Book in (select the eyar))")
# Add a color attribute to each node based on its column value
color_map = []
for node in G.nodes():
    if node in df["First Author"].values:
         color_map.append("green")
    else:
        color_map.append("red")

size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 7 )

############# LEGGENDA ##############
legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='Journal/Book',markerfacecolor='red', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='First Author',markerfacecolor='green', markersize=13),]


# #Kamada-Kawai Layout è un algoritmo di NetworkX che posiziona i nodi di un grafo in modo che la somma delle energie
# potenziali dei nodi sia minima. Questo algoritmo utilizza un modello fisico di forze repulsive tra i nodi e
# forze attrattive tra i nodi connessi da un arco. Il risultato è un disegno del grafo che cerca di minimizzare
# l'intersezione degli archi e la sovrapposizione dei nodi. In generale, l'algoritmo di Kamada-Kawai Layout produce un disegno di grafo equilibrato e piacevole esteticamente.

pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color=color_map,
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
                        font_size=5)

############# LEGENDA ##############
ax.legend(handles=legend_elements1, loc='lower left', prop={'size': 60})
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
plt.xlabel('Journal/Book')
plt.ylabel('Collaborazioni')
plt.xticks(rotation=15)

plt.show()