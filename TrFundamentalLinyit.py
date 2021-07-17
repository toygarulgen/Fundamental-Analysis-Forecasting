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
# uretim1 = pd.DataFrame(uretim1['Linyit'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Linyit'].isnull().values.any()
# uretim1['Linyit'].isnull().sum()
# uretim1['Linyit'] = uretim1['Linyit'].interpolate(method='pad', limit=6)
# uretim1['Linyit'].iloc[2068] = uretim1['Linyit'].iloc[2067]

# uretim1.to_excel('trfundamentallinyit.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentallinyit.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minLin = uretim1.groupby(['year','month'], as_index=False)['Linyit'].min()
totalLin = uretim1.groupby(['year','month'], as_index=False)['Linyit'].sum()
maxLin = uretim1.groupby(['year','month'], as_index=False)['Linyit'].max()

minLin1 = uretim1.groupby(['month'], as_index=False)['Linyit'].min()
maxLin1 = uretim1.groupby(['month'], as_index=False)['Linyit'].max()


totalLin['numdays'] = np.zeros(len(totalLin))

for i in range(len(totalLin)):
    year1 = totalLin['year'][i]
    month1 = totalLin['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalLin['numdays'][i] = total
    
df1 = df['LİNYİT']
totalLin = pd.concat([totalLin, df1], axis=1).reindex(maxLin.index)

totalLin['CF'] = totalLin.LİNYİT / (totalLin.numdays * 24 * totalLin.LİNYİT)
    
minLintotalLin = totalLin.groupby(['month'], as_index=False)['CF'].min()
maxLintotalLin = totalLin.groupby(['month'], as_index=False)['CF'].max()

meanLintotalLin = totalLin.groupby(['month'], as_index=False)['CF'].mean()


cf = np.zeros(len(maxLintotalLin))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)

for iteration2 in range(len(maxLintotalLin)):  
    number = random.uniform(minLintotalLin['CF'][iteration2], maxLintotalLin['CF'][iteration2])
    cf['CF'][iteration2] = number


x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red", label="Random Values")
ax.plot(meanLintotalLin['CF'], color="yellow", label="Average Values")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minLintotalLin['month']]
ax.fill_between(x, minLintotalLin['CF'], maxLintotalLin['CF'], color="gray")
ax.set_title("LIGNITE CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minLinyitkütlesaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Linyit'].min()
totalLinyitsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Linyit'].sum()
maxLinyitsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Linyit'].max()


totalLinyitsaatlik['numdays'] = np.zeros(len(totalLinyitsaatlik))

for i in range(len(totalLinyitsaatlik)):
    year1 = totalLinyitsaatlik['year'][i]
    month1 = totalLinyitsaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalLinyitsaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalLinyitsaatlik['kurulu guc'] = np.zeros(len(totalLinyitsaatlik))
count = 0
for iteration3 in range(len(totalLinyitsaatlik)):
    if totalLinyitsaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalLinyitsaatlik['month'][iteration3] == df['Month'][count]:
        totalLinyitsaatlik['kurulu guc'][iteration3] = df['LİNYİT'][count]

totalLinyitsaatlik['CF'] = totalLinyitsaatlik['Linyit'] / (totalLinyitsaatlik['kurulu guc'])

totalLinyitsaatlik = pd.concat([totalLinyitsaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxLinyitsaatlik.index)


minnn = totalLinyitsaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalLinyitsaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalLinyitsaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalLinyitsaatlik = totalLinyitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalLinyitsaatlik = totalLinyitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalLinyitsaatlik = totalLinyitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalLinyitsaatlik),randomnumber))

for iteration2 in range(len(mintotalLinyitsaatlik)): 
    number = np.random.uniform(mintotalLinyitsaatlik['CF'][iteration2], maxtotalLinyitsaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcflinyit.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalLinyitsaatlik['CF'], maxtotalLinyitsaatlik['CF'], color="gray")
ax.set_title("LIGNITE CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)


