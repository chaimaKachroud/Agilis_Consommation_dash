import pandas as pd
from datetime import timedelta

file_transaction = './data/transactions.xlsx'
sheet_name = 'All'
skip_rows = 0
namesMonth ={1:"Janvier" ,2:"Février" ,3:"Mars" ,4:"Avril" ,5:"Mai" ,6:"Juin" ,7:"Juillet" ,8:"Août",9:"Septembre" ,10:"Octobre" ,11:"Novembre" ,12:"Décembre" }
distanceMaxAControler = 8000
limiteConso = 20

data = pd.read_excel(file_transaction , sheet_name= sheet_name, engine="openpyxl" , skiprows=skip_rows)

data.rename(columns={'Quantit�': 'quantite'}, inplace=True)
data.rename(columns={'Type transaction': 'transaction'}, inplace=True)
data.rename(columns={'Numéro carte': 'ncarte'}, inplace=True)
data.rename(columns={'Type Tpe': 'tpe'}, inplace=True)
data.rename(columns={'Date': 'date'}, inplace=True)
data.rename(columns={'Station': 'station'}, inplace=True)
data.rename(columns={'Porteur': 'porteur'}, inplace=True)
data.rename(columns={'Montant': 'cout'}, inplace=True)
data.rename(columns={'Produit': 'produit'}, inplace=True)
data.rename(columns={'Véhicule': 'vehicule'}, inplace=True)
data.rename(columns={'Chauffeur': 'chauffeur'}, inplace=True)
data.rename(columns={'Ticket': 'ticket'}, inplace=True)
data['cout'] = data['cout'].str.replace(r' TND', '')
data['quantite'] = data['quantite'].str.replace(r' L', '')
data['kilometrage'] = data['kilometrage'].str.replace(r' Km', '')
data['cout'] = data['cout'].str.replace(r',', '.')
data['cout'] = data['cout'].str.replace(r' ', '')
data['cout'] = data[['cout']].astype(float)
data['quantite'] = data['quantite'].str.replace(r',', '.')
data['quantite'] = data['quantite'].str.replace(r' ', '')
data['quantite'] = data[['quantite']].astype(float)
data['kilometrage'] = data['kilometrage'].str.replace(r',', '.')
data['kilometrage'] = data['kilometrage'].str.replace(r' ', '')
data['kilometrage'] = data[['kilometrage']].astype(float)
# Filter
achat = data[(data.transaction == "Achat PR")]
# & (data.Porteur == 11149475)
# input data
list_of_dates = achat['date']

df = pd.DataFrame({'date': pd.to_datetime(list_of_dates, dayfirst=True)})

# define list of attributes required    
L = ['year', 'month', 'day', 'quarter'] # we can add also 'dayofweek', 'dayofyear', 'weekofyear'

# define generator expression of series, one for each attribute
date_gen = (getattr(df['date'].dt, i).rename(i) for i in L)

# concatenate results and join to original dataframe
achat = achat.join(pd.concat(date_gen, axis=1))
achat['mois'] = pd.to_datetime(achat['date']).dt.strftime('%Y%m')
achat['prixUnitaire']= (achat.cout / achat.quantite).round(decimals=3)

mois =getattr(max(achat['date']), 'month')
annee =getattr(max(achat['date']), 'year')
anneeMois =max(achat['mois'])

quantiteProduitMois = pd.pivot_table(achat, index='produit', columns='mois', values=['quantite'], aggfunc='sum', margins=True, margins_name='Total')


# Consommation 

anneeMoisAnterieur = quantiteProduitMois['quantite'].columns[-3]
anneeAnterieur , moisAnterieur = int(anneeMoisAnterieur[0:4]), int(anneeMoisAnterieur[4:])

quantiteProduitMois = pd.pivot_table(achat, index='produit', columns='mois', values=['quantite'], aggfunc='sum', margins=True, margins_name='Total')
# quantiteProduitMois = pd.DataFrame(quantiteProduitMois.to_dict())

quantiteProduitDuMois = round(quantiteProduitMois['quantite'][anneeMois], 3)
quantiteProduitDuMoisAnt = round(quantiteProduitMois['quantite'][anneeMoisAnterieur], 3)

varQteMensuelle = 100 * round( quantiteProduitDuMois.Total / quantiteProduitDuMoisAnt.Total ,2)

# pour un graphique camanbert

total = quantiteProduitDuMois['Total']
pourcentageGasoil = round( 100 * quantiteProduitDuMois['Gasoil']/total , 2)
pourcentageGasoilss = round( 100 * quantiteProduitDuMois['Gasoil sans soufre']/total , 2)
pourcentageSS = round( 100 * quantiteProduitDuMois['Super SP']/total , 2)



consoDistance = pd.DataFrame(achat.pivot_table(index=['porteur', 'date'], values=['station' , 'quantite', 'cout' , 'kilometrage']).to_records())

b = consoDistance.groupby(['porteur']).diff()

consoDistance['distance'] = b['kilometrage'].shift(-1)
consoDistance['conso'] =  100 * consoDistance['quantite'] / consoDistance['distance']

list_of_dates = consoDistance['date']
df = pd.DataFrame({'date': pd.to_datetime(list_of_dates, dayfirst=True)})
L = ['year', 'month'] # we can add also 'dayofweek', 'dayofyear', 'weekofyear'

# define generator expression of series, one for each attribute
date_gen = (getattr(df['date'].dt, i).rename(i) for i in L)

# concatenate results and join to original dataframe
consoDistance = consoDistance.join(pd.concat(date_gen, axis=1))
consoDistance['mois'] = pd.to_datetime(consoDistance['date']).dt.strftime('%Y%m')

listErronee = consoDistance[(consoDistance.distance <=0) | (consoDistance.distance >=distanceMaxAControler) | (consoDistance.conso >= limiteConso)]
listVerifier = consoDistance[(consoDistance.distance >0) & (consoDistance.distance <=distanceMaxAControler) & (consoDistance.conso < limiteConso)]

# Top Consommation du mois
listTop10 = pd.DataFrame(listVerifier.pivot_table(index='porteur' , columns=['mois'] , values= 'conso' , aggfunc='mean').round(2).to_records())

listTop10.drop(listTop10.columns[1:-2], inplace=True, axis=1)
# inverser la consom
listTop10[anneeMoisAnterieur] = - (listTop10[anneeMoisAnterieur].fillna(0))

top10Vehi = (listTop10.sort_values(by=[listTop10.columns[-1]], ascending=False, inplace=False, kind="quicksort", na_position="last")[:10]['porteur']).to_list()
top10Conso = listTop10.sort_values(by=[listTop10.columns[-1]], ascending=False, inplace=False, kind="quicksort", na_position="last")[:10][anneeMois].to_list()
top10consoAnterieur = listTop10.sort_values(by=[listTop10.columns[-1]], ascending=False, inplace=False, kind="quicksort", na_position="last")[:10][anneeMoisAnterieur].to_list()
