# Analisi della tecnologia Blockchain e sue applicazione nel Agri-Food #
# Topic Modeling su documenti riguardanti le applicazioni Blockchain nel settore dell’ Agri-Food #
## Descrizione
##  BRANCH topicModeling_with_Gensim
Nel branch topicModeling_with_Gensim, i modelli proposti sono due, LDA e LSA, entrambi con un numero di topics, anche in questo caso, pari a 4.
In questo branch sono stati implementati differenti algoritmi col fine di effettuare più analisi comparative tra i modelli sopracitati, sia sulla base di metriche di valutazione,
sia grazie all'ausilio di strumenti di visualizzazione grafica.
Con riguardo al modello LDA sono stati utilizzati ulteriori strumenti di visualizzazione grafica, che permettono un'interazione con i grafici stessi, aumentandone il contenuto informativo.
....
 ## Analisi principali
### Normalizzazione
In questo branch la tokenizzazione è stata effettuata sia per singole parole che per bigrammi e trigrammi, in modo tale da riuscire a costruire dei topics maggiormente esplicativi delle argomentazioni trattate nei vari abstracts.
Riguardo la lemmatizzazione e lo stemming anche in questo branch abbiamo preferito optare per la sola lemmatizzazione in quanto quest’ultima considera il contesto e converte la parola nella sua forma base significativa, ovvero nel suo lemma,che è presente nel dizionario preso come riferimento dal metodo.
## Analisi principali
Raccolta documenti web e pubblicazioni scientifiche degli ultimi 5 anni
 * Topic Modeling su i documenti e analisi del trend temporale dei topics (# documenti per topic per anno)
 * Analisi ottimale del numero di topic per il corpus di documenti
 * Analisi comparativa degli algoritmi di topic modeling: LDA e NNMF
 ###WordCloud:
In questo caso, per visualizzare il contenuto di ciascun topic, abbiamo optato per l’utilizzo della tecnica delle WordCloud, le quali rappresentano i termini secondo un font di grandezza differente in base al peso associato a ciascun termine, peso che in questo caso è rappresentato dalla Term Frequency.
###Coherence:
Volendo effettuare un’analisi più approfondita e un'ulteriore confronto rispetto ai modelli LDA e LSA, si è deciso di implementare due differenti algoritmi per entrambi i modelli che si basano sulla metrica di valutazione detta “Coherence”.
 * Un primo algoritmo fornisce un'unica Coherence in base ai parametri e al numero di Topics prefissati in maniera discrezionale.
 * Un secondo algoritmo fornisce più Coherence associate a ciascun numero di Topics dato da a un range di valori da noi indicato, permettendo così una valutazione ulteriore del miglior numero di Topics,ma stavolta in base alla Coherence.
Inoltre lo stesso algoritmo fornisce una visualizzazione grafica che fornisce la stessa informazione in modo molto intuitivo.
L’algoritmo basato sulla MultiCoherence fornisce anche la possibilità di ottenere degli output che ci indicano il contributo in percentuale di ciascun termine all’interno di ciascun Topic, secondo il numero di Topics ottimale fornito dall’algoritmo.
# Per questioni di visualizzazione vengono esposti solo i primi 10 termini più importanti sia per il modello LDA che per il modello  LSA.
### Grafici Interattivi:
Nel nostro caso specifico utilizzeremo le librerie TSNE e pyLDAvis:
 * t-SNE è un algoritmo non lineare per la riduzione della dimensionalità in grado di rilevare la presenza di Cluster di diverse dimensioni tramite una funzione che consente di rappresentare punti di dati simili vicini tra loro e, allo stesso tempo, dati diversi lontani tra loro.
 * pyLDAvis: grazie a questa libreria viene generato un grafico interattivo che fornisce sia una visione globale degli argomenti e di come differiscono l'uno dall'altro, sia una visione locale consentendo allo stesso tempo un'analisi approfondita dei termini più strettamente associati a ciascun singolo argomento.
