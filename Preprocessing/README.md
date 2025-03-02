# Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus” #
# PREPROCESSING: #

## Descrizione
Una volta ottenuti i dati grezzi, si è passati alla fase di pre-processing in modo da ripulire i dati e
trasformarli in un formato più adatto alla nostra analisi. In tal senso si è proceduto a una prima
rielaborazione generale dei dataset e a successive rielaborazioni più specifiche a seconda dell’analisi da
effettuare per rispondere ai differenti quesiti. 

Con riguardo al pre-processing generale,non essendo possibile scaricare più di 10.000 records alla volta da 
PubMed, si è reso necessario il Download di più Dataset distinti a seconda della numerosità degli articoli 
scientifici per anno, che sono stati successivamente concatenati grazie all’utilizzo della libreria Pandas di 
Python andando a creare un nuovo Dataset completo , contenente 227.737 articoli scientifici in tema 
“coronavirus” da 1949 al 2023 senza duplicati. 
Al fine di migliorare la qualità dei dati di partenza delle nostre analisi, si è deciso di verificare la presenza di 
valori anomali quali Na e NaN e di variabili non utili all'analisi, procedendo alla loro eliminazione. 
Nel dettaglio vista la grande presenza di valori anomali per le Variabili PMCID (PubMed Central Identifier), 
NIHMS ID (National Institutes of Health Manuscript System Identifier) e DOI (Digital Object Identifier)
 e al contempo vista il loro scarso contributo informativo, abbiamo optato per una loro eliminazione così 
come per Create Date e Citation assicurandoci infine di eliminare anche ulteriori righe che presentassero 
valori anomali. 

Un ulteriore grado di qualità è stato fornito tramite una seconda analisi, dove si è andato a ripulire il 
Dataset specialmente in riferimento alla variabile “Authors” che, dovendo essere processata per 
individuare i vari coautori nelle analisi successive, presentava al suo interno caratteri anomali che, associati 
al nome di un autore, avevano come effetto quello di fornire duplicati degli stessi, fornendo un quadro più 
confusionario e con maggiori attori rispetto alla realtà. 
Lo stesso discorso vale per quegli autori che erano presentati sia in carattere minuscolo e maiuscolo. 
A tale scopo è stata quindi effettuata un’analisi dettagliata che individuasse i caratteri anomali e li 
eliminasse, fornendo così un'informazione più chiara ed intellegibile. 

Al fine di rispondere al quesito E si è optato per l’implementazione di una Topic Modeling, e si è reso 
dunque necessario un ulteriore fase di pre-processing al fine di ricercare gli Abstract di ciascun articolo 
analizzato sui quali applicare il modello. 
L’abstract, contenuto all’interno dei file di testo scaricabili da PubMed secondo le medesime condizioni 
valide per il pre-processing generale affrontato in precedenza, è stato estratto grazie al codice contenuto 
nello stesso file Python “ Preprocessing_FINALE “ ed associato a ciascun articolo tramite il suo 
PMID,ottenendo così il “Dataset_Corona_1949_2023_FINALE.xlsx” alla base di tutte le analisi effettuate 
successivamente, avente 224.383 osservazioni e avente le seguenti 7 variabili: 
- PMID (PubMed Identifier): un numero univoco assegnato a ciascuna pubblicazione presente nel database.
- Title: il titolo della pubblicazione.
- Authors: l'elenco degli autori che hanno contribuito alla pubblicazione.
- First Author: il primo autore della pubblicazione, che spesso è anche il corrispondente autore.
- Journal/Book: il nome della rivista o del libro in cui è stata pubblicata la pubblicazione.
- Publication Year: l'anno di pubblicazione della pubblicazione. - Abstract: l’abstract collegato a ciascuna pubblicazione.





