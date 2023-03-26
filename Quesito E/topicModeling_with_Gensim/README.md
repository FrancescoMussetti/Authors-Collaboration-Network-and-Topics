# Analisi delle Reti di Collaborazione tra Autori nella Ricerca Scientifica in ambito “Coronavirus” #
# Topic Modeling sugli articoli scientifici presenti sul Database PUBMED riguardanti le pubblicazioni relative al tema del "Coronavirus" #
## Descrizione
##  BRANCH TopicModeling_Gensim_NWE
Nel branch TopicModeling_Gensim_NWE, il modello proposto è quello della Latent Dirichlet Allocation(LDA), con un numero di topics pari a 6.
In questo branch sono stati implementati differenti algoritmi col fine di effettuare più analisi del modello proposto rendendole maggiormente
intellegibili grazie all'ausilio di strumenti di visualizzazione grafica.
In particolare sono stati utilizzati anche strumenti di visualizzazione grafica che permettono un'interazione con i grafici stessi, aumentandone il contenuto informativo.
....
 ## Analisi principali
### Normalizzazione
In questo branch la tokenizzazione è stata effettuata sia per singole parole che per bigrammi e trigrammi, in modo tale da riuscire a costruire dei topics maggiormente esplicativi delle argomentazioni trattate nei vari abstracts.
Riguardo la lemmatizzazione e lo stemming anche in questo branch abbiamo preferito optare per la sola lemmatizzazione in quanto quest’ultima considera il contesto e converte la parola nella sua forma base significativa, ovvero nel suo lemma,che è presente nel dizionario preso come riferimento dal metodo.
## Analisi principali
 * Raccolta pubblicazioni scientifiche dal database PUBMED a partire dal 1949 fino al 2023.
 * Topic Modeling su i documenti e analisi del trend temporale dei topics (# documenti per topic per periodo di riferimento scelto)
 * Analisi ottimale del numero di topic per il corpus di documenti
 * Implementazione della Topic Modeling sullo strumento Grafo ( % di topic per ciascun autore, classificazione degli autori per topic)
 ###WordCloud:
In questo caso, per visualizzare il contenuto di ciascun topic, abbiamo optato per l’utilizzo della tecnica delle WordCloud, le quali rappresentano i termini secondo un font di grandezza differente in base al peso associato a ciascun termine, peso che in questo caso è rappresentato dalla Term Frequency.

### Grafici Interattivi:
Nel nostro caso specifico utilizzeremo le librerie TSNE e pyLDAvis:
 * t-SNE è un algoritmo non lineare per la riduzione della dimensionalità in grado di rilevare la presenza di Cluster di diverse dimensioni tramite una funzione che consente di rappresentare punti di dati simili vicini tra loro e, allo stesso tempo, dati diversi lontani tra loro.
 * pyLDAvis: grazie a questa libreria viene generato un grafico interattivo che fornisce sia una visione globale degli argomenti e di come differiscono l'uno dall'altro, sia una visione locale consentendo allo stesso tempo un'analisi approfondita dei termini più strettamente associati a ciascun singolo argomento.

### Analisi Globale e Temporale degli Argomenti
Sulla base del miglior modello ottenuto, si è poi effettuata:
* Un'analisi Globale degli argomenti trattati nel Dataset di Documenti. 
* Un'analisi Temporale in grado di individuare i possibili Trend argomentativi che si sono susseguiti nel periodo dal 1949 al 2023 in merito al tema oggetto di studio.

## Per questioni di visualizzazione vengono esposti solo i primi 10 termini più importanti del modello LDA cosi come viene effettuato un focus sugli Autori con maggiori Collaborazioni (degree).