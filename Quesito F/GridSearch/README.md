## Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus” #

# QUESITO F: Topic Modeling sugli articoli scientifici presenti sul Database PUBMED riguardanti le pubblicazioni relative al tema del "Coronavirus" #
## Descrizione
## BRANCH GrisSearch_NWE
Nel branch GrisSearch_NWE, dopo aver effettuato le opportune operazioni di pre-processing del contenuto testuale dei Documenti viene implementato il modello LDA.
In particolare, in tale branch viene implementato un algoritmo di GridSearch capace di identificare il numero ottimale di Topics per un corpus di Documenti.
L'utilizzo del miglior numero di topic tra quelli analizzati ci ha permesso di fornire sia una migliore analisi Globale che Temporale degli argomenti trattati.
## Analisi principali:
### Normalizzazione
Abbiamo tokenizzato i documenti per singole word attraverso l’utilizzo del metodo word_tokenize() di nltk. 
Precedentemente a questa operazione abbiamo utilizzato le Regular Expression per una pre-elaborazione del testo. 
Riguardo la lemmatizzazione e lo stemming anche in questo branch abbiamo preferito optare per la sola lemmatizzazione in quanto quest’ultima considera il contesto e converte la parola nella sua forma base significativa, ovvero nel suo lemma, e questo fa si che il termine risultante sia una parola di senso compiuto che è presente nel dizionario preso come riferimento dal metodo.
 * Raccolta pubblicazioni scientifiche dal database PUBMED a partire dal 1949 fino al 2023.
 * Topic Modeling su i documenti e analisi del trend temporale dei topics (# documenti per topic per periodo di riferimento scelto)
 * Analisi ottimale del numero di topic per il corpus di documenti
 * Implementazione della Topic Modeling sullo strumento Grafo ( % di topic per ciascun autore, classificazione degli autori per topic)
### Numero di Topics Ottimale
Per la scelta degli iperparametri ottimali da utilizzare nei modelli sopracitati è stato implementato un'algoritmo di GridSearch.
Tale modello ci ha permesso di individuare il numero ottimale di Topics per la nostra analisi pari a 6.
