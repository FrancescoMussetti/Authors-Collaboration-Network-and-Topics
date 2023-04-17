# Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus” #
# PREPROCESSING: #

## Descrizione
 Scriviamo del codice che vada a concatenare i diversi CSV scaricati da PUBMED che fanno riferimento al medesimo anno.
Andiamo inoltre ad implementare del codice che vada a leggere i file txt scaricati da PUBMED contenenti l'Abstract in
modo da creare un secondo DataFrame con "PMID" e "Abstract".
Successivamente uniremo i due Dataframe per crearne uno solo sulla base del PMID comune, ottenendo cosi il nostro Dataset
completo di tutti gli articoli per tutti gli anni-

Andiamo inoltre ad eliminare tutti i valori anomali quali:
- Valori duplicati
- Valori nulli
- Variabili che non sono d'interesse all'analisi da effettuare.

Procediamo con un ulteriore pulizia della colonna Authors, dove vengono ricercati tutti i valori sospetti che potrebbero
generare doppioni di autori e inficiare la qualità dell'analisi.
Infine i nomi degli autori vengono standardizzati in lettere minuscole al fine di evitare la generazione di doppioni.





