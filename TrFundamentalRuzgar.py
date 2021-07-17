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
# uretim1 = pd.DataFrame(uretim1['Rüzgar'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Rüzgar'].isnull().values.any()
# uretim1['Rüzgar'].isnull().sum()
# uretim1['Rüzgar'] = uretim1['Rüzgar'].interpolate(method='pad', limit=6)
# uretim1['Rüzgar'].iloc[2068] = uretim1['Rüzgar'].iloc[2067]

# uretim1.to_excel('trfundamentalruzgar.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentalruzgar.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minRuzgar = uretim1.groupby(['year','month'], as_index=False)['Rüzgar'].min()
totalRuzgar = uretim1.groupby(['year','month'], as_index=False)['Rüzgar'].sum()
maxRuzgar = uretim1.groupby(['year','month'], as_index=False)['Rüzgar'].max()

minRuzgar1 = uretim1.groupby(['month'], as_index=False)['Rüzgar'].min()
maxRuzgar1 = uretim1.groupby(['month'], as_index=False)['Rüzgar'].max()


totalRuzgar['numdays'] = np.zeros(len(totalRuzgar))

for i in range(len(totalRuzgar)):
    year1 = totalRuzgar['year'][i]
    month1 = totalRuzgar['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalRuzgar['numdays'][i] = total
    
df1 = df['RÜZGAR']
totalRuzgar = pd.concat([totalRuzgar, df1], axis=1).reindex(maxRuzgar.index)

totalRuzgar['CF'] = totalRuzgar.Rüzgar / (totalRuzgar.numdays * 24 * totalRuzgar.RÜZGAR)
    
minRuzgartotalRuzgar = totalRuzgar.groupby(['month'], as_index=False)['CF'].min()
maxRuzgartotalRuzgar = totalRuzgar.groupby(['month'], as_index=False)['CF'].max()

meanRuzgartotalRuzgar = totalRuzgar.groupby(['month'], as_index=False)['CF'].mean()


cf = np.zeros(len(maxRuzgartotalRuzgar))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)


for iteration2 in range(len(maxRuzgartotalRuzgar)):  
    number = random.uniform(minRuzgartotalRuzgar['CF'][iteration2], maxRuzgartotalRuzgar['CF'][iteration2])
    cf['CF'][iteration2] = number


x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red")
ax.plot(meanRuzgartotalRuzgar['CF'], color="yellow")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minRuzgartotalRuzgar['month']]
ax.fill_between(x, minRuzgartotalRuzgar['CF'], maxRuzgartotalRuzgar['CF'], color="gray")
ax.set_title("WIND CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minRüzgarsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Rüzgar'].min()
totalRüzgarsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Rüzgar'].sum()
maxRüzgarsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Rüzgar'].max()


totalRüzgarsaatlik['numdays'] = np.zeros(len(totalRüzgarsaatlik))

for i in range(len(totalRüzgarsaatlik)):
    year1 = totalRüzgarsaatlik['year'][i]
    month1 = totalRüzgarsaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalRüzgarsaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalRüzgarsaatlik['kurulu guc'] = np.zeros(len(totalRüzgarsaatlik))
count = 0
for iteration3 in range(len(totalRüzgarsaatlik)):
    if totalRüzgarsaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalRüzgarsaatlik['month'][iteration3] == df['Month'][count]:
        totalRüzgarsaatlik['kurulu guc'][iteration3] = df['RÜZGAR'][count]

totalRüzgarsaatlik['CF'] = totalRüzgarsaatlik['Rüzgar'] / (totalRüzgarsaatlik['kurulu guc'])

totalRüzgarsaatlik = pd.concat([totalRüzgarsaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxRüzgarsaatlik.index)


minnn = totalRüzgarsaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalRüzgarsaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalRüzgarsaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalRüzgarsaatlik = totalRüzgarsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalRüzgarsaatlik = totalRüzgarsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalRüzgarsaatlik = totalRüzgarsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalRüzgarsaatlik),randomnumber))

for iteration2 in range(len(mintotalRüzgarsaatlik)): 
    number = np.random.uniform(mintotalRüzgarsaatlik['CF'][iteration2], maxtotalRüzgarsaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcfwind.xlsx')



x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalRüzgarsaatlik['CF'], maxtotalRüzgarsaatlik['CF'], color="gray")
ax.set_title("WIND CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)








