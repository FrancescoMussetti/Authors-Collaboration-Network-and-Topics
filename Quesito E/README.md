# Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus” #
# QUESITO E: #

## Descrizione
Nel seguente codice riprendiamo l'analisi effettuata sui collegamenti tra gli Autori che hanno collaborato
 ad una stessa pubblicazione scientifica in ambito "Coronavirus" durante il periodo di riferimento indicato.
  Nel dettaglio andremo ad indagare come i Primi Autori si posizionano all'interno del grafo in termini di livelli Degree e
 di Betweenneess che presentano gli stessi,  in modo da evidenziare, per quanto possibie, se i Primi Autori risultano essere
 autori con un maggior numero di collaborazioni ed in particolare se gli stessi svolgano un ruolo di "ponte" tra due o più gruppi di
autori e che abbiano una posizione importante nel passaggio delle informazioni tra le varie sotto-comunità scientifiche.

In particolare il seguente codice genera quattro distinti grafici:

1) Il primo è il grafo  attraverso il quale riusciamo a visualizzare:
- I nodi, rappresentanti ogni singolo Autore, colorati in base al fatto che essi siano Primi Autori (BLU) o Autori Secondari (ROSSO) e
le cui dimensioni sono date dalla rispettiva Degree (numero di archi in entrata), dunque maggiore degree maggiore grandezza del nodo.
- Gli edge, che rappresentano i collegamenti tra Autori che hanno collaborato ad una stessa pubblicazione,
dove lo spessore dell'edge è rappresentativo del peso dello stesso, quindi di quante collaborazioni hanno effettivamente avuto i due autori collegati.

2) Il secondo è un grafico a barre  attraverso il quale riusciamo a visualizzare:
- La Degree dei primi 20 Nodi con maggior degree pesata per numero di collaborazioni e dunque l'elenco dei rispettivi
20 Autori con maggiori collaborazioni, colorati come detto precedentemente.


3) Il terzo è un grafico a barre  attraverso il quale riusciamo a visualizzare:
- La Betweenness Centrality dei primi 20 Nodi con maggior betweenness e dunque l'elenco dei rispettivi
20 Autori  con una centralità di intermediazione elevata che potrebbero avere una posizione privilegiata nel grafo,
 agendo come intermediari chiave nel facilitare la comunicazione o la collaborazione tra altri autori o gruppi di autori che altrimenti
potrebbero non essere direttamente connessi, anch'essi colorati come detto precedentemente.


4) Il quarto è un' insieme di sottografi attraverso il quale riusciamo a visualizzare:
- Tutti i sottografi generati dall'eliminazione dei 20 Autori con maggior betweenness individuati
precedentemente, in modo da darci un'idea del carico informativo che questi nodi possedevano, anch'essi colorati
come indicato precedentemente.





