# Analisi della tecnologia Blockchain e sue applicazione nel Agri-Food #
# Topic Modeling su documenti riguardanti le applicazioni Blockchain nel settore dell’ Agri-Food #
## Descrizione
## BRANCH topicModeling_with_ScikitLearn
Nel branch topicModeling_with_ScikitLearn, dopo aver effettuato le opportune operazioni di pre-processing del contenuto testuale dei Documenti,sono stati messi a confronto quattro differenti algoritmi di Topic Modeling: LDA, NMF, PLSA e LSA.
....
L'utilizzo del miglior modello di Topic Modeling tra quelli analizzati ci ha permesso di fornire sia un'analisi Globale che Temporale degli argomenti trattati.
## Analisi principali
## Analisi principali:
### Normalizzazione
Abbiamo tokenizzato i documenti per singole word attraverso l’utilizzo del metodo word_tokenize() di nltk. 
Precedentemente a questa operazione abbiamo utilizzato le Regular Expression per una pre-elaborazione del testo. 
Riguardo la lemmatizzazione e lo stemming anche in questo branch abbiamo preferito optare per la sola lemmatizzazione in quanto quest’ultima considera il contesto e converte la parola nella sua forma base significativa, ovvero nel suo lemma, e questo fa si che il termine risultante sia una parola di senso compiuto che è presente nel dizionario preso come riferimento dal metodo.
* Raccolta documenti web e pubblicazioni scientifiche degli ultimi 5 anni
* Topic Modeling su i documenti e analisi del trend temporale dei topics (# documenti per topic per anno)
* Analisi ottimale del numero di topic per il corpus di documenti
* Analisi comparativa degli algoritmi di topic modeling: LDA e NNMF
### Numero di Topics Ottimale
Per la scelta degli iperparametri ottimali da utilizzare nei modelli sopracitati è stato implementato un'algoritmo di GridSearch.
Tale modello ci ha permesso di individuare il numero ottimale di Topics per la nostra analisi pari a 4.
### Confronto tra i Modelli
E' stata effettuata un analisi comparativa tra i quattro modelli sulla base di:
* Metriche di valutazione quali la Likelihood 
* Strumenti di visualizzazione grafica quali i Barplot.
### Analisi Globale e Temporale degli Argomenti
Sulla base del miglior modello ottenuto, si è poi effettuata:
* Un'analisi Globale degli argomenti trattati nel Dataset di Documenti. 
* Un'analisi Temporale in grado di individuare i possibili Trend argomentativi che si sono susseguiti nel periodo dal 2017 al 2021 in merito al tema oggetto di studio.
