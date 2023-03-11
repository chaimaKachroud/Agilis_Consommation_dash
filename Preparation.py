import pandas as pd
#---- load data
data = pd.read_excel('transaction 2022.xlsx', sheet_name='All', engine="openpyxl")
#---- Pretraitement
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

