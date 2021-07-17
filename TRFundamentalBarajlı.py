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
# uretim1 = pd.DataFrame(uretim1['Barajlı'])
# uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Barajlı'].isnull().values.any()
# uretim1['Barajlı'].isnull().sum()
# uretim1['Barajlı'] = uretim1['Barajlı'].interpolate(method='pad', limit=6)
# uretim1['Barajlı'].iloc[2068] = uretim1['Barajlı'].iloc[2067]

# uretim1.to_excel('trfundamentalbarajlı.xlsx')


#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentalbarajlı.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minBarajlı = uretim1.groupby(['year','month'], as_index=False)['Barajlı'].min()
totalBarajlı = uretim1.groupby(['year','month'], as_index=False)['Barajlı'].sum()
maxBarajlı = uretim1.groupby(['year','month'], as_index=False)['Barajlı'].max()

meanBarajlı = uretim1.groupby(['year','month'], as_index=False)['Barajlı'].mean()


minBarajlı1 = uretim1.groupby(['month'], as_index=False)['Barajlı'].min()
maxBarajlı1 = uretim1.groupby(['month'], as_index=False)['Barajlı'].max()



totalBarajlı['numdays'] = np.zeros(len(totalBarajlı))

for i in range(len(totalBarajlı)):
    year1 = totalBarajlı['year'][i]
    month1 = totalBarajlı['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalBarajlı['numdays'][i] = total
    
BarajlıKuruluGuc = df['BARAJLI']
totalBarajlı = pd.concat([totalBarajlı, BarajlıKuruluGuc], axis=1).reindex(maxBarajlı.index)

totalBarajlı['CF'] = totalBarajlı.Barajlı / (totalBarajlı.numdays * 24 * totalBarajlı.BARAJLI)
    

minBarajlıtotalBarajlı = totalBarajlı.groupby(['month'], as_index=False)['CF'].min()
maxBarajlıtotalBarajlı = totalBarajlı.groupby(['month'], as_index=False)['CF'].max()

meanBarajlıtotalBarajlı = totalBarajlı.groupby(['month'], as_index=False)['CF'].mean()

cf = np.zeros(len(maxBarajlıtotalBarajlı))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)


for iteration2 in range(len(maxBarajlıtotalBarajlı)):  
    number = random.uniform(minBarajlıtotalBarajlı['CF'][iteration2], maxBarajlıtotalBarajlı['CF'][iteration2])
    cf['CF'][iteration2] = number
    
x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red", label="Random Values")
ax.plot(meanBarajlıtotalBarajlı['CF'], color="yellow", label="Average Values")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minBarajlıtotalBarajlı['month']]
ax.fill_between(x, minBarajlıtotalBarajlı['CF'], maxBarajlıtotalBarajlı['CF'], color="gray")
ax.set_title("BARAJLI CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)


#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minBarajlısaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Barajlı'].min()
totalBarajlısaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Barajlı'].sum()
maxBarajlısaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Barajlı'].max()


totalBarajlısaatlik['numdays'] = np.zeros(len(totalBarajlısaatlik))

for i in range(len(totalBarajlısaatlik)):
    year1 = totalBarajlısaatlik['year'][i]
    month1 = totalBarajlısaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalBarajlısaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalBarajlısaatlik['kurulu guc'] = np.zeros(len(totalBarajlısaatlik))
count = 0
for iteration3 in range(len(totalBarajlısaatlik)):
    if totalBarajlısaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalBarajlısaatlik['month'][iteration3] == df['Month'][count]:
        totalBarajlısaatlik['kurulu guc'][iteration3] = df['BARAJLI'][count]

totalBarajlısaatlik['CF'] = totalBarajlısaatlik['Barajlı'] / (totalBarajlısaatlik['kurulu guc'])

totalBarajlısaatlik = pd.concat([totalBarajlısaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxBarajlısaatlik.index)


minnn = totalBarajlısaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalBarajlısaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalBarajlısaatlik.groupby(['year','month'], as_index=False)['CF'].max()

totalBarajlısaatlik = totalBarajlısaatlik.drop(totalBarajlısaatlik.index[0:17544])
totalBarajlısaatlik = totalBarajlısaatlik.reset_index(drop=True)
totalBarajlısaatlik = totalBarajlısaatlik.drop(totalBarajlısaatlik.index[8760:17520])

mintotalBarajlısaatlik2 = totalBarajlısaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalBarajlısaatlik2 = totalBarajlısaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalBarajlısaatlik2 = totalBarajlısaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 100

random2 = np.zeros((len(maxtotalBarajlısaatlik2),randomnumber))

for iteration2 in range(len(mintotalBarajlısaatlik2)): 
    number = np.random.uniform(mintotalBarajlısaatlik2['CF'][iteration2], maxtotalBarajlısaatlik2['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

randombarajli = pd.DataFrame(random2)
randombarajli.to_excel('randombarajli.xlsx')


saatlikcfbarajlı = np.mean(random2, axis=1)
saatlikcfbarajlı = pd.DataFrame(saatlikcfbarajlı)
saatlikcfbarajlı = saatlikcfbarajlı.set_axis(['CF'], axis=1, inplace=False)
saatlikcfbarajlı.to_excel('saatlikcfbarajlı.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcfbarajlı, color="red", label="Random Values")
ax.fill_between(x, mintotalBarajlısaatlik2['CF'], maxtotalBarajlısaatlik2['CF'], color="gray")
ax.set_title("BARAJLI CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)

randombarajli = randombarajli * 23213
randombarajli.to_excel('randombarajli.xlsx')

# x = np.arange(0, len(meanBarajlı))
# ax = plt.figure().add_subplot(111)
# ax.plot(totalBarajlı['Barajlı'].iloc[0:12].values, color="gray", label="2016")
# ax.plot(totalBarajlı['Barajlı'].iloc[12:24].values, color="red", label="2017")
# ax.plot(totalBarajlı['Barajlı'].iloc[24:36].values, color="yellow", label="2018")
# ax.plot(totalBarajlı['Barajlı'].iloc[36:48].values, color="black", label="2019")
# ax.plot(totalBarajlı['Barajlı'].iloc[48:60].values, color="purple", label="2020")
# ax.plot(totalBarajlı['Barajlı'].iloc[60:65].values, color="orange", label="2021")
# ax.plot(toplam.values, color="pink", label="Ortalaması")
# # ax.set_title("TOTAL PRODUCTİON MONTHLY ", fontsize=10)
# ax.set_xlabel('Months', fontsize=12)
# ax.set_ylabel('Production', fontsize=12)
# ax.legend(loc="best", prop={'size': 8})
# ax.grid(True)

#2018 ile 2020 ortalamsı alınacak.
