######################################### PRE-PROCESSING ################################################
#### Scriviamo del codice che vada a concatenare i diversi CSV scaricati da PUBMED che fanno riferimento al medesimo anno.
### Andiamo inoltre ad implementare del codice che vada a leggere i file txt scaricati da PUBMED contenenti l'Abstract in
### modo da creare un secondo DataFrame con "PMID" e "Abstract".
### Successivamente uniremo i due Dataframe per crearne uno solo sulla base del PMID comune, ottenendo cosi il nostro Dataset
### completo di tutti gli articoli per tutti gli anni e avente come variabili :
###  *** scrivere le variabili *****
### Andiamo inoltre ad eliminare tutti i valori anomali quali:
# - Valori duplicati
# - Valori nulli
## Eliminiamo le variabili che non sono d'interesse all'analisi da effettuare.
## Procediamo con un ulteriore pulizia della colonna Authors, dove vengono ricercati tutti i valori sospetti che potrebbero
## generare doppioni di autori e inficiare la qualità dell'analisi
## Infine i nomi degli autori vengono standardizzati in lettere minuscole al fine di evitare la generazione di doppioni.




#### Import Packages:
import pandas as pd
import re


################################  CREAZIONE DEL PRIMO DATAFRAME #############################################
### Caricamento dei vari Dataset:
###### ANNO 1949 - 1999 #####
t1_49_99 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_1949_1999.csv")
###### ANNI 2000 - 2015 #####
t1_00_15 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2000_2015.csv")
###### ANNO 2016 #####
t1_16 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2016.csv")
###### ANNO 2017 #####
t1_17 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2017.csv")
###### ANNO 2018 #####
t1_18 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2018.csv")
###### ANNO 2019 #####
t1_19 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2019.csv")
###### ANNO 2020 #####
t1_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_1_20_._30_4_20(pt.1).csv")
t2_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_1_20_._30_4_20(pt.2).csv")
t3_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_5_20_._31_5_20.csv  ")
t4_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_6_20_._15_7_20(pt.1).csv ")
t5_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_6_20_._15_7_20(pt.2).csv  ")
t6_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_16_7_20_._1_9_20(pt.1).csv ")
t7_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_16_7_20_._1_9_20(pt.2).csv ")
t8_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_02_9_20_._31_10_20(pt.1).csv")
t9_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_02_9_20_._31_10_20(pt.2).csv")
t10_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_11_20_._31_12_20(pt.1).csv")
t11_20 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2020/csv-coronaviru-set_1_11_20_._31_12_20(pt.2).csv")


###### ANNO 2021 #####
t1_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_01_21_._25_01_21(pt.1).csv")
t2_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_01_21_._25_01_21(pt.2).csv")
t3_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_26_1_21_._31_3_21(pt.1).csv")
t4_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_26_1_21_._31_3_21(pt.2).csv ")
t5_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_4_21_._31_5_21(pt.1).csv  ")
t6_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_4_21_._31_5_21(pt.2).csv ")
t7_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_6_21_._31_7_21(pt.1).csv ")
t8_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_6_21_._31_7_21(pt.2).csv")
t9_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_1_8_21_._30_9_21(pt.1).csv")
t10_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_1_8_21_._30_9_21(pt.2).csv")
t11_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_10_21_._30_11_21(pt.1).csv")
t12_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_01_10_21_._30_11_21(pt.2).csv")
t13_21 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2021/csv-coronaviru-set_1_12_21_._31_12_21.csv")


###### ANNO 2022 #####
t1_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_01_2022(pt.1).csv")
t2_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_01_2022(pt.2).csv")
t3_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_03_01_2022_._31_03_2022(pt.1).csv")
t4_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_03_01_2022_._31_03_2022(pt.2).csv ")
t5_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_04_22_._30_06_22(pt.1).csv  ")
t6_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_04_22_._30_06_22(pt.2).csv ")
t7_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_07_22_._30_09_22(pt.1).csv ")
t8_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_07_22_._30_09_22(pt.2).csv")
t9_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_10_22_._31_12_22(pt.1).csv")
t10_22 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/2022/csv-coronaviru-set_01_10_22_._31_12_22(pt.2).csv")

###### ANNO 2023 #####
t1_23 = pd.read_csv("./Dataset_CoronaVirus_1949_2023/csv-coronaviru-set_2023.csv")


df1 = pd.concat([t1_49_99,t1_00_15,t1_16,t1_17,t1_18,t1_19,
                            t1_20,t2_20,t3_20,t4_20,t5_20,t6_20, t7_20, t8_20, t9_20, t10_20, t11_20,
                            t1_21,t2_21,t3_21,t4_21,t5_21,t6_21,t7_21,t8_21,t9_21,t10_21,t11_21,t12_21,t13_21,
                            t1_22,t2_22,t3_22,t4_22,t5_22,t6_22,t7_22,t8_22,t9_22,t10_22,
                            t1_23
                            ], axis=0)

#INFO SUL PRIMO DATAFRAME :
# df1_summary= df1.info()
# print(df1_summary)
### Verifichiamo la presenza di valori duplicati:
# print(df1.duplicated())
# Remove duplicates:
df1 = df1.drop_duplicates()



###############################  CREAZIONE DEL SECONDO DATAFRAME #############################################
##Il codice definisce una lista di campi che si vogliono estrarre dal file di testo, legge il file di testo
# come una lista di stringhe e divide le stringhe in righe separate. Poi per ogni riga, estrae il valore del campo
# corrispondente e lo aggiunge a un dizionario che rappresenta una riga del DataFrame.
# Infine, crea un DataFrame con tutte le righe e colonne corrispondenti ai campi definiti inizialmente e lo stampa a schermo.

import os
import pandas as pd

# definire la lista di campi da estrarre dal file di testo
fields = ['PMID', 'AB']

# creare una lista vuota per memorizzare tutti i DataFrame
dfs = []

# loop attraverso tutti i file txt nella cartella "File_txt_for_Abstract"
for filename in os.listdir('./File_txt_for_Abstract/'):
    if filename.endswith('.txt'):
        # leggere il file di testo come una lista di stringhe
        with open('./File_txt_for_Abstract/' + filename, 'r', encoding='utf-8') as f:
            txt = f.read()

        # split del testo in base ai caratteri "PMID-" e "OWN -"
        txt_list = txt.split("PMID-")[1:]

        # inizializzazione delle liste che conterranno i dati estratti
        pmid_list = []
        abstract_list = []

        # loop su tutte le sezioni del testo estratte
        for t in txt_list:
            # estrazione del PMID
            pmid = t.split("\n")[0].strip()
            pmid_list.append(pmid)

            # estrazione dell'abstract
            abstract_start = "AB  - "
            abstract_end1 = "FAU - "
            abstract_end2 = "CI  - "

            if abstract_start in t:
                if abstract_end1 in t:
                    abstract = t.split(abstract_start)[1].split(abstract_end1)[0].strip()
                elif abstract_end2 in t:
                    abstract = t.split(abstract_start)[1].split(abstract_end2)[0].strip()
                else:
                    abstract = t.split(abstract_start)[1].strip()

                # Rimuovi gli spazi dall'abstract
                abstract = abstract.replace('\n', '')

            else:
                abstract = ""

            abstract_list.append(abstract)

        # creazione del DataFrame
        df = pd.DataFrame({"PMID": pmid_list, "Abstract": abstract_list})

        # Aggiungi il dataframe alla lista di dataframe
        dfs.append(df)

# concatenare tutti i DataFrame nella lista in un unico DataFrame
df2 = pd.concat(dfs, ignore_index=True)

# stampare il DataFrame
# print(df2)

#INFO SUL SECONDO DATAFRAME :
# df2_summary= df2.info()
# print(df2_summary)
### Verifichiamo la presenza di valori duplicati:
# print(df2.duplicated())
# Remove duplicates:
df2 = df2.drop_duplicates()


#### ^^^^^^^^^^^^^^^^^^^^^^     UNIONE DEI DUE DATAFRAME IN UNO SOLO:  ^^^^^^^^^^^^^^^^^^^^^^^^^^
#converti il tipo di dati della colonna "PMID" in df1 in object
df2['PMID'] = df2['PMID'].astype('int64')
#unisce i due DataFrame
merged_df = pd.merge(df1, df2, on='PMID')
#visualizza il risultato
# print(merged_df)
df = merged_df


#### ^^^^^^^^^^^ Verifichiamo la presenza di valori anomali quali NA e NaN
print(df.isna().sum())
### ^^^^^^^^^^^^ ELIMINIAMO QUELLE VARIABILI CHE NON RISULTANO UTILI AI FINI DELL'ANALISI E PRESENTANO VALORI ANOMALI (NaN)
df.drop(["PMCID"],axis=1, inplace=True)
df.drop(["DOI"],axis=1, inplace=True)
df.drop(["NIHMS ID"],axis=1, inplace=True)
df.drop(["Create Date"],axis=1, inplace=True)
df.drop(["Citation"],axis=1, inplace=True)
# print(df)
#
### ^^^^^^^^^^^^^^^^^^^ Ci assicuriamo di eliminare le righe che presentano eventuali valori nulli restanti
print(df.isna().sum())
df = df.dropna()
print(df.isna().sum())

### ^^^^  Puliamo la colonna "Authors" da simboli non voluti e renderla minuscola ^^^^^
### ^^^^^^^ (vengono eliminati anche i nomi delle organizzazioni dopo ";" erano pochi)  ^^^^^^
def clean_authors(authors):
    # rimuove tutti i caratteri diversi da lettere, virgola, punto e virgola, parentesi tonde, spazi e trattino
    cleaned_authors = re.sub(r'[^a-zA-Z,;\(\)\-\s]', '', authors)
    # dividi la stringa di autori in una lista di autori separati dalla virgola
    authors_list = cleaned_authors.split(",")
    # per ogni autore, elimina tutti i caratteri dopo il punto e virgola nella stringa
    authors_list = [author.split(";")[0] for author in authors_list]
    # unisci la lista di autori in una stringa separata da virgole
    cleaned_authors = ",".join(authors_list)
    # trasforma la stringa in minuscolo
    cleaned_authors = cleaned_authors.lower()
    # rimuove gli spazi all'inizio e alla fine della stringa
    cleaned_authors = cleaned_authors.strip()
    return cleaned_authors

# applica la funzione alla colonna Authors del DataFrame
df['Authors'] = df['Authors'].apply(clean_authors)
# Converte i nomi degli autori principali in minuscolo
df["First Author"] = df["First Author"].str.lower()


### Verifichiamo la presenza di valori duplicati attraverso il PMID:
# Rimozione delle righe duplicate, mantenendo solo quella con il valore meno recente di "Publication Year"
df = df.sort_values(by=['PMID', 'Publication Year'], ascending=False).drop_duplicates(subset=['PMID'], keep='last')
# Stampa del DataFrame dopo la rimozione delle righe duplicate
# print("DataFrame dopo la rimozione delle righe duplicate:")
# print(df)



# ################################# SELEZIONE E EXPORT #########################################
# # #Ci assicuriamo di analizzare gli articoli effettivamente pubblicati nell'anno desiderato:
# df_selected = df.query('`Publication Year` >= 2000 and `Publication Year` <= 2019')
df_selected = df.query('`Publication Year` == 2023')

# # # Esporta il dataframe in un file CSV
# ####df_selected.to_csv('Dataset_Corona_2023_COMPLETO===.csv', index=False)
#esporta il DataFrame in un file Excel
df_selected.to_excel('Dataset_Corona_2023_FINALE.xlsx', index=False, sheet_name='Sheet1', startrow=0, startcol=0)

# apre il file Excel appena creato
os.startfile('Dataset_Corona_2023_FINALE.xlsx')
