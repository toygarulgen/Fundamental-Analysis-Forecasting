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
from calendar import monthrange
import matplotlib.ticker as ticker
import datetime

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
# uretim1 = pd.DataFrame(uretim1['Taş Kömür'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Taş Kömür'].isnull().values.any()
# uretim1['Taş Kömür'].isnull().sum()
# uretim1['Taş Kömür'] = uretim1['Taş Kömür'].interpolate(method='pad', limit=6)
# uretim1['Taş Kömür'].iloc[2068] = uretim1['Taş Kömür'].iloc[2067]

# uretim1.to_excel('trfundamentaltaskomur.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentaltaskomur.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minTas = uretim1.groupby(['year','month'], as_index=False)['Taş Kömür'].min()
totalTas = uretim1.groupby(['year','month'], as_index=False)['Taş Kömür'].sum()
maxTas = uretim1.groupby(['year','month'], as_index=False)['Taş Kömür'].max()

minTas1 = uretim1.groupby(['month'], as_index=False)['Taş Kömür'].min()
maxTas1 = uretim1.groupby(['month'], as_index=False)['Taş Kömür'].max()


totalTas['numdays'] = np.zeros(len(totalTas))

for i in range(len(totalTas)):
    year1 = totalTas['year'][i]
    month1 = totalTas['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalTas['numdays'][i] = total
    
df1 = df['TAŞ KÖMÜR']
totalTas = pd.concat([totalTas, df1], axis=1).reindex(maxTas.index)

totalTas['CF'] = totalTas['Taş Kömür'] / (totalTas.numdays * 24 * totalTas['TAŞ KÖMÜR'])
    
minTastotalTas = totalTas.groupby(['month'], as_index=False)['CF'].min()
maxTastotalTas = totalTas.groupby(['month'], as_index=False)['CF'].max()

meanTastotalTas = totalTas.groupby(['month'], as_index=False)['CF'].mean()


cf = np.zeros(len(maxTastotalTas))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)

for iteration2 in range(len(maxTastotalTas)):  
    number = random.uniform(minTastotalTas['CF'][iteration2], maxTastotalTas['CF'][iteration2])
    cf['CF'][iteration2] = number


x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red", label="Random Values")
ax.plot(meanTastotalTas['CF'], color="yellow", label="Average Values")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minTastotalTas['month']]
ax.fill_between(x, minTastotalTas['CF'], maxTastotalTas['CF'], color="gray")
ax.set_title("TAŞ KÖMÜR CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minTasKomursaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Taş Kömür'].min()
totalTasKomursaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Taş Kömür'].sum()
maxTasKomursaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Taş Kömür'].max()


totalTasKomursaatlik['numdays'] = np.zeros(len(totalTasKomursaatlik))

for i in range(len(totalTasKomursaatlik)):
    year1 = totalTasKomursaatlik['year'][i]
    month1 = totalTasKomursaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalTasKomursaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalTasKomursaatlik['kurulu guc'] = np.zeros(len(totalTasKomursaatlik))
count = 0
for iteration3 in range(len(totalTasKomursaatlik)):
    if totalTasKomursaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalTasKomursaatlik['month'][iteration3] == df['Month'][count]:
        totalTasKomursaatlik['kurulu guc'][iteration3] = df['TAŞ KÖMÜR'][count]

totalTasKomursaatlik['CF'] = totalTasKomursaatlik['Taş Kömür'] / (totalTasKomursaatlik['kurulu guc'])

totalTasKomursaatlik = pd.concat([totalTasKomursaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxTasKomursaatlik.index)


minnn = totalTasKomursaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalTasKomursaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalTasKomursaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalTasKomursaatlik = totalTasKomursaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalTasKomursaatlik = totalTasKomursaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()

meantotalTasKomursaatlik = totalTasKomursaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalTasKomursaatlik),randomnumber))

for iteration2 in range(len(mintotalTasKomursaatlik)): 
    number = np.random.uniform(mintotalTasKomursaatlik['CF'][iteration2], maxtotalTasKomursaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcftaskomur.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalTasKomursaatlik['CF'], maxtotalTasKomursaatlik['CF'], color="gray")
ax.set_title("TAŞ KÖMÜR CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)


