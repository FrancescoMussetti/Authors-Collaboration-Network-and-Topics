# Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus”
## QUESITO F: Topic Modeling sulle Pubblicazioni Scientifiche del Database PUBMED sul Coronavirus
Questo progetto si concentra sull'analisi delle reti di collaborazione tra autori nella ricerca scientifica sul tema del "Coronavirus". Il modello proposto è basato su tecniche di Topic Modeling, in particolare sull'algoritmo Latent Dirichlet Allocation (LDA), applicato agli articoli scientifici presenti nel database PUBMED, con l'obiettivo di esplorare i principali argomenti trattati nel corso degli anni, a partire dal 1949 fino al 2023.

## Questa directory è suddivisa in due principali sotto-directory:

## 1. GridSearch
Questa sottodirectory si concentra sull'ottimizzazione del numero di topic da utilizzare per il modello LDA. È stato implementato un algoritmo di GridSearch per determinare il numero ottimale di topic per il corpus di documenti. L'analisi principale include:

Pre-processing del testo: utilizzo di tokenizzazione, lemmatizzazione e regular expressions per la pulizia e normalizzazione del testo.
Raccolta dei dati: articoli scientifici dal database PUBMED.
Analisi dei Trend Temporali: analisi del numero di documenti per topic in vari periodi di tempo.
Risultati: il numero ottimale di topic identificato tramite GridSearch è pari a 6.

## 2. TopicModeling_with_Gensim
Questa sottodirectory è dedicata all'implementazione del modello LDA utilizzando la libreria Gensim. In questo branch sono stati utilizzati anche strumenti di visualizzazione avanzati per facilitare l'interpretazione dei risultati. Le principali analisi e strumenti utilizzati includono:

Tokenizzazione avanzata: sia per singole parole che per bigrammi e trigrammi.
Lemmatisation: applicata al testo per ridurre le parole alle loro forme base.
Visualizzazioni:
WordCloud per visualizzare i termini più rappresentativi di ciascun topic.
t-SNE per la riduzione della dimensionalità e l'identificazione di cluster nei dati.
pyLDAvis per l'analisi interattiva dei topic.
Analisi globale e temporale: esplorazione dei principali argomenti e delle tendenze nel tempo, a partire dal 1949 fino al 2023.

## Dipendenze
Per eseguire correttamente il progetto, è necessario installare le seguenti librerie Python:
- gensim
- nltk
- pyLDAvis
- matplotlib
- seaborn
- pandas
- numpy
- sklearn





