#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:38:26 2021

@author: toygar
"""
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from seffaflik.elektrik import uretim
# from sklearn.linear_model import LinearRegression
from calendar import monthrange

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

df = pd.read_excel('KURULUGUC2016-2021.xlsx',parse_dates=True)


start = pd.to_datetime('2016-01-01')
end = pd.to_datetime('2021-05-01')
rng = pd.date_range(start, end, freq='H')
len(rng)
rng = rng[0:-1]
len(rng)
rng = pd.DataFrame(rng)
rng = rng.set_axis(['DateTime'], axis=1, inplace=False)
rng = rng.set_index('DateTime')


# uretim1 = uretim.__gerceklesen(baslangic_tarihi='2016-01-01', bitis_tarihi='2021-04-30')
# uretim1['DateTime'] = pd.to_datetime(uretim1.Tarih) + uretim1.Saat.astype('timedelta64[h]')
# uretim1 = pd.merge(uretim1, rng, how="outer", on=["DateTime", "DateTime"])
# uretim1 = uretim1.set_index('DateTime')
# uretim1 = uretim1.drop('Tarih', axis = 1)
# uretim1 = uretim1.drop('Saat', axis = 1)
# uretim1 = pd.DataFrame(uretim1['Akarsu'])
# uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Akarsu'].isnull().values.any()
# uretim1['Akarsu'].isnull().sum()
# uretim1['Akarsu'] = uretim1['Akarsu'].interpolate(method='pad', limit=6)
# uretim1['Akarsu'].iloc[2068] = uretim1['Akarsu'].iloc[2067]

# uretim1.to_excel('trfundamentalakarsu.xlsx')


#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentalakarsu.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minAkarsu = uretim1.groupby(['year','month'], as_index=False)['Akarsu'].min()
totalAkarsu = uretim1.groupby(['year','month'], as_index=False)['Akarsu'].sum()
maxAkarsu = uretim1.groupby(['year','month'], as_index=False)['Akarsu'].max()

minAkarsu1 = uretim1.groupby(['month'], as_index=False)['Akarsu'].min()
maxAkarsu1 = uretim1.groupby(['month'], as_index=False)['Akarsu'].max()



totalAkarsu['numdays'] = np.zeros(len(totalAkarsu))

for i in range(len(totalAkarsu)):
    year1 = totalAkarsu['year'][i]
    month1 = totalAkarsu['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalAkarsu['numdays'][i] = total
    
AkarsuKuruluGuc = df['AKARSU']
totalAkarsu = pd.concat([totalAkarsu, AkarsuKuruluGuc], axis=1).reindex(maxAkarsu.index)

totalAkarsu['CF'] = totalAkarsu.Akarsu / (totalAkarsu.numdays * 24 * totalAkarsu.AKARSU)
    

minRuzgartotalAkarsu = totalAkarsu.groupby(['month'], as_index=False)['CF'].min()
maxRuzgartotalAkarsu = totalAkarsu.groupby(['month'], as_index=False)['CF'].max()



cf = np.zeros(len(maxRuzgartotalAkarsu))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)


for iteration2 in range(len(maxRuzgartotalAkarsu)):  
    number = random.uniform(minRuzgartotalAkarsu['CF'][iteration2], maxRuzgartotalAkarsu['CF'][iteration2])
    cf['CF'][iteration2] = number
    
cf.to_excel('CFAKARSU.xlsx')

        
ax = np.arange(0, 12)
plt.figure(figsize=(8,5))
plt.fill_between(ax, minRuzgartotalAkarsu['CF'], maxRuzgartotalAkarsu['CF'], color="gray")
plt.plot(cf, color="red")
plt.title("AKARSU CAPACITY FACTOR")
plt.grid(True)
plt.legend(loc=0)
plt.show()

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minAkarsusaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Akarsu'].min()
totalAkarsusaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Akarsu'].sum()
maxAkarsusaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Akarsu'].max()


totalAkarsusaatlik['numdays'] = np.zeros(len(totalAkarsusaatlik))

for i in range(len(totalAkarsusaatlik)):
    year1 = totalAkarsusaatlik['year'][i]
    month1 = totalAkarsusaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalAkarsusaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalAkarsusaatlik['kurulu guc'] = np.zeros(len(totalAkarsusaatlik))
count = 0
for iteration3 in range(len(totalAkarsusaatlik)):
    if totalAkarsusaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalAkarsusaatlik['month'][iteration3] == df['Month'][count]:
        totalAkarsusaatlik['kurulu guc'][iteration3] = df['AKARSU'][count]

totalAkarsusaatlik['CF'] = totalAkarsusaatlik['Akarsu'] / (totalAkarsusaatlik['kurulu guc'])

totalAkarsusaatlik = pd.concat([totalAkarsusaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxAkarsusaatlik.index)


minnn = totalAkarsusaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalAkarsusaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalAkarsusaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalAkarsusaatlik = totalAkarsusaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalAkarsusaatlik = totalAkarsusaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalAkarsusaatlik = totalAkarsusaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalAkarsusaatlik),randomnumber))

for iteration2 in range(len(mintotalAkarsusaatlik)): 
    number = np.random.uniform(mintotalAkarsusaatlik['CF'][iteration2], maxtotalAkarsusaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcfakarsu.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalAkarsusaatlik['CF'], maxtotalAkarsusaatlik['CF'], color="gray")
ax.set_title("AKARSU CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)




