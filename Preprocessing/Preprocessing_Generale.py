######################################### PRE-PROCESSING ################################################
#### Scriviamo del codice che vada a concatenare i diversi CSV scaricati da PUBMED che fanno riferimento al medesimo anno.
### Andiamo inoltre ad eliminare tutti i valori anomali quali:
# - Valori duplicati
# - Valori nulli
## Eliminiamo le variabili che non sono d'interesse all'analisi da effettuare.


#### Import Packages:
import os
import pandas as pd

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


df_concatenated = pd.concat([t1_49_99,t1_00_15,t1_16,t1_17,t1_18,t1_19,
                            t1_20,t2_20,t3_20,t4_20,t5_20,t6_20, t7_20, t8_20, t9_20, t10_20, t11_20,
                            t1_21,t2_21,t3_21,t4_21,t5_21,t6_21,t7_21,t8_21,t9_21,t10_21,t11_21,t12_21,t13_21,
                            t1_22,t2_22,t3_22,t4_22,t5_22,t6_22,t7_22,t8_22,t9_22,t10_22,
                            t1_23
                            ], axis=0)

# print(t_concatenated)

df_summary= df_concatenated.info()
print(df_summary)
df = df_concatenated

### Verifichiamo la presenza di valori duplicati:
print(df.duplicated())
# Remove duplicates:
df = df.drop_duplicates()


### Verifichiamo la presenza di valori anomali quali NA e NaN
print(df.isna().sum())
#ELIMINIAMO QUELLE VARIABILI CHE NON RISULTANO UTILI AI FINI DELL'ANALISI E PRESENTANO VALORI ANOMALI (NaN)
df.drop(["PMCID"],axis=1, inplace=True)
df.drop(["DOI"],axis=1, inplace=True)
df.drop(["NIHMS ID"],axis=1, inplace=True)
df.drop(["Create Date"],axis=1, inplace=True)
# print(df)

#Ci assicuriamo di eliminare le righe che presentano eventuali valori nulli restanti
print(df.isna().sum())
df = df.dropna()
print(df.isna().sum())

# ################################# SELEZIONE E EXPORT #########################################
#Ci assicuriamo di analizzare gli articoli effettivamente pubblicati nel periodo o anno desiderato:
#df_selected = df.query('`Publication Year` >= 2000 and `Publication Year` <= 2019')
df_selected = df.query('`Publication Year` == 2020')

# ####Esporta il dataframe in un file CSV
####df_selected.to_csv('Dataset_Corona_2023_GENERALE.csv', index=False)
#esporta il DataFrame in un file Excel
df_selected.to_excel('Dataset_Corona_2020_GENERALE.xlsx', index=False, sheet_name='Sheet1', startrow=0, startcol=0)

# apre il file Excel appena creato
os.startfile('Dataset_Corona_2020_GENERALE.xlsx')

