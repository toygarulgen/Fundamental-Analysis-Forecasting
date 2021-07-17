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
# uretim1 = pd.DataFrame(uretim1['Asfaltit Kömür'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Asfaltit Kömür'].isnull().values.any()
# uretim1['Asfaltit Kömür'].isnull().sum()
# uretim1['Asfaltit Kömür'] = uretim1['Asfaltit Kömür'].interpolate(method='pad', limit=6)
# uretim1['Asfaltit Kömür'].iloc[2068] = uretim1['Asfaltit Kömür'].iloc[2067]

# uretim1.to_excel('trfundamentalasfaltit.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentalasfaltit.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minAsf = uretim1.groupby(['year','month'], as_index=False)['Asfaltit Kömür'].min()
totalAsf = uretim1.groupby(['year','month'], as_index=False)['Asfaltit Kömür'].sum()
maxAsf = uretim1.groupby(['year','month'], as_index=False)['Asfaltit Kömür'].max()

minAsf1 = uretim1.groupby(['month'], as_index=False)['Asfaltit Kömür'].min()
maxAsf1 = uretim1.groupby(['month'], as_index=False)['Asfaltit Kömür'].max()


totalAsf['numdays'] = np.zeros(len(totalAsf))

for i in range(len(totalAsf)):
    year1 = totalAsf['year'][i]
    month1 = totalAsf['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalAsf['numdays'][i] = total
    
df1 = df['ASFALTİT']
totalAsf = pd.concat([totalAsf, df1], axis=1).reindex(maxAsf.index)

totalAsf['CF'] = totalAsf['Asfaltit Kömür'] / (totalAsf.numdays * 24 * totalAsf.ASFALTİT)
    
minAsftotalAsf = totalAsf.groupby(['month'], as_index=False)['CF'].min()
maxAsftotalAsf = totalAsf.groupby(['month'], as_index=False)['CF'].max()

meanAsftotalAsf = totalAsf.groupby(['month'], as_index=False)['CF'].mean()


cf = np.zeros(len(maxAsftotalAsf))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)

for iteration2 in range(len(maxAsftotalAsf)):  
    number = random.uniform(minAsftotalAsf['CF'][iteration2], maxAsftotalAsf['CF'][iteration2])
    cf['CF'][iteration2] = number


x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red", label="Random Values")
ax.plot(meanAsftotalAsf['CF'], color="yellow", label="Average Values")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minAsftotalAsf['month']]
ax.fill_between(x, minAsftotalAsf['CF'], maxAsftotalAsf['CF'], color="gray")
ax.set_title("ASFALTİT KÖMÜR CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minAsfaltitsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Asfaltit Kömür'].min()
totalAsfaltitsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Asfaltit Kömür'].sum()
maxAsfaltitsaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Asfaltit Kömür'].max()


totalAsfaltitsaatlik['numdays'] = np.zeros(len(totalAsfaltitsaatlik))

for i in range(len(totalAsfaltitsaatlik)):
    year1 = totalAsfaltitsaatlik['year'][i]
    month1 = totalAsfaltitsaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalAsfaltitsaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalAsfaltitsaatlik['kurulu guc'] = np.zeros(len(totalAsfaltitsaatlik))
count = 0
for iteration3 in range(len(totalAsfaltitsaatlik)):
    if totalAsfaltitsaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalAsfaltitsaatlik['month'][iteration3] == df['Month'][count]:
        totalAsfaltitsaatlik['kurulu guc'][iteration3] = df['ASFALTİT'][count]

totalAsfaltitsaatlik['CF'] = totalAsfaltitsaatlik['Asfaltit Kömür'] / (totalAsfaltitsaatlik['kurulu guc'])

totalAsfaltitsaatlik = pd.concat([totalAsfaltitsaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxAsfaltitsaatlik.index)


minnn = totalAsfaltitsaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalAsfaltitsaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalAsfaltitsaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalAsfaltitsaatlik = totalAsfaltitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalAsfaltitsaatlik = totalAsfaltitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()

meantotalAsfaltitsaatlik = totalAsfaltitsaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalAsfaltitsaatlik),randomnumber))

for iteration2 in range(len(mintotalAsfaltitsaatlik)): 
    number = np.random.uniform(mintotalAsfaltitsaatlik['CF'][iteration2], maxtotalAsfaltitsaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcfasfaltit.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalAsfaltitsaatlik['CF'], maxtotalAsfaltitsaatlik['CF'], color="gray")
ax.set_title("ASFALTİT KÖMÜR CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)

#JEO:1624
#BIO:1144
#SOL:6999
#ROR:8122
#WIN:9294

#LIN:10120
#ASF:405
#TAS:811
