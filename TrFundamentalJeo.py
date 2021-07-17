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

# day_of_year = datetime.now().timetuple().tm_yday

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]


def capacityfactorplot(a):
    x = np.arange(0, 12)
    ax = plt.figure().add_subplot(111)
    ax.plot(a, color="red", label="Random Values")
    ax.plot(meanJeototalJeo['CF'], color="yellow", label="Average Values")
    ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minJeototalJeo['month']]
    ax.fill_between(x, minJeototalJeo['CF'], maxJeototalJeo['CF'], color="gray")
    ax.set_title("JEOTERMAL CAPACITY FACTOR", fontsize=10)
    ax.set_xlabel('Months', fontsize=12)
    ax.set_ylabel('Capacity Factor', fontsize=12)
    ax.legend(loc="best", prop={'size': 8})
    ax.grid(True)
    ax.set_xticks(np.arange(0,12))
    ax.set_xticklabels(ticklabels)
    return a

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

#%% VERİ ÇEKME
# uretim1 = uretim.__gerceklesen(baslangic_tarihi='2016-01-01', bitis_tarihi='2021-04-30')
# uretim1['DateTime'] = pd.to_datetime(uretim1.Tarih) + uretim1.Saat.astype('timedelta64[h]')
# uretim1 = pd.merge(uretim1, rng, how="outer", on=["DateTime", "DateTime"])
# uretim1 = uretim1.set_index('DateTime')
# uretim1 = uretim1.drop('Tarih', axis = 1)
# uretim1 = uretim1.drop('Saat', axis = 1)
# uretim1 = pd.DataFrame(uretim1['Jeo Termal'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Jeo Termal'].isnull().values.any()
# uretim1['Jeo Termal'].isnull().sum()
# uretim1['Jeo Termal'] = uretim1['Jeo Termal'].interpolate(method='pad', limit=6)
# uretim1['Jeo Termal'].iloc[2068] = uretim1['Jeo Termal'].iloc[2067]

# uretim1.to_excel('trfundamentaljeo.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentaljeo.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minJeo = uretim1.groupby(['year','month'], as_index=False)['Jeo Termal'].min()
totalJeo = uretim1.groupby(['year','month'], as_index=False)['Jeo Termal'].sum()
maxJeo = uretim1.groupby(['year','month'], as_index=False)['Jeo Termal'].max()

minJeo1 = uretim1.groupby(['month'], as_index=False)['Jeo Termal'].min()
maxJeo1 = uretim1.groupby(['month'], as_index=False)['Jeo Termal'].max()


totalJeo['numdays'] = np.zeros(len(totalJeo))

for i in range(len(totalJeo)):
    year1 = totalJeo['year'][i]
    month1 = totalJeo['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalJeo['numdays'][i] = total
    
df1 = df['JEOTERMAL']
totalJeo = pd.concat([totalJeo, df1], axis=1).reindex(maxJeo.index)

totalJeo['CF'] = totalJeo['Jeo Termal'] / (totalJeo.numdays * 24 * totalJeo.JEOTERMAL)
    
minJeototalJeo = totalJeo.groupby(['month'], as_index=False)['CF'].min()
maxJeototalJeo = totalJeo.groupby(['month'], as_index=False)['CF'].max()
meanJeototalJeo = totalJeo.groupby(['month'], as_index=False)['CF'].mean()

mintotalkuruluguc = totalJeo.groupby(['month'], as_index=False)['JEOTERMAL'].min()
maxtotalkuruluguc = totalJeo.groupby(['month'], as_index=False)['JEOTERMAL'].max()
meantotalkuruluguc = totalJeo.groupby(['month'], as_index=False)['JEOTERMAL'].mean()

randomnumber = 10

randomcf = np.zeros((len(maxJeototalJeo),randomnumber))

for iteration2 in range(len(maxJeototalJeo)): 
    number = np.random.uniform(minJeototalJeo['CF'][iteration2], maxJeototalJeo['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    randomcf[iteration2] = number 

cf = np.mean(randomcf, axis=1)
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)
capacityfactorplot(randomcf)

cf['month'] = maxJeototalJeo['month']




#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minJeosaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Jeo Termal'].min()
totalJeosaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Jeo Termal'].sum()
maxJeosaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Jeo Termal'].max()


totalJeosaatlik['numdays'] = np.zeros(len(totalJeosaatlik))

for i in range(len(totalJeosaatlik)):
    year1 = totalJeosaatlik['year'][i]
    month1 = totalJeosaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalJeosaatlik['numdays'][i] = total


#%% CF EKLEME

# totalJeosaatlik['CF'] = np.zeros(len(totalJeosaatlik))
# count = 0
# for iteration3 in range(len(totalJeosaatlik)):
#     if totalJeosaatlik['month'][iteration3] != cf['month'][count]:
#         count = count + 1        
#     elif totalJeosaatlik['month'][iteration3] == cf['month'][count]:
#         totalJeosaatlik['CF'][iteration3] = cf['CF'][count]
#     if iteration3 == 46727:
#         break
#     if totalJeosaatlik['year'][iteration3] != totalJeosaatlik['year'][iteration3+1]:
#         count = 0
        
#%% MIN KURULU GÜÇ EKLEME

# totalJeosaatlik['min kurulu guc'] = np.zeros(len(totalJeosaatlik))
# count = 0
# for iteration3 in range(len(totalJeosaatlik)):
#     if totalJeosaatlik['month'][iteration3] != mintotalkuruluguc['month'][count]:
#         count = count + 1        
#     elif totalJeosaatlik['month'][iteration3] == mintotalkuruluguc['month'][count]:
#         totalJeosaatlik['min kurulu guc'][iteration3] = mintotalkuruluguc['JEOTERMAL'][count]
#     if iteration3 == 46727:
#         break
#     if totalJeosaatlik['year'][iteration3] != totalJeosaatlik['year'][iteration3+1]:
#         count = 0
# #%% MAX KURULU GÜÇ EKLEME

# totalJeosaatlik['max kurulu guc'] = np.zeros(len(totalJeosaatlik))
# count = 0
# for iteration3 in range(len(totalJeosaatlik)):
#     if totalJeosaatlik['month'][iteration3] != maxtotalkuruluguc['month'][count]:
#         count = count + 1        
#     elif totalJeosaatlik['month'][iteration3] == maxtotalkuruluguc['month'][count]:
#         totalJeosaatlik['max kurulu guc'][iteration3] = maxtotalkuruluguc['JEOTERMAL'][count]
#     if iteration3 == 46727:
#         break
#     if totalJeosaatlik['year'][iteration3] != totalJeosaatlik['year'][iteration3+1]:
#         count = 0

#%% KURULU GÜÇ EKLEME

totalJeosaatlik['kurulu guc'] = np.zeros(len(totalJeosaatlik))
count = 0
for iteration3 in range(len(totalJeosaatlik)):
    if totalJeosaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalJeosaatlik['month'][iteration3] == df['Month'][count]:
        totalJeosaatlik['kurulu guc'][iteration3] = df['JEOTERMAL'][count]

totalJeosaatlik['CF'] = totalJeosaatlik['Jeo Termal'] / (totalJeosaatlik['kurulu guc'])

totalJeosaatlik = pd.concat([totalJeosaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxJeosaatlik.index)


minnn = totalJeosaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalJeosaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalJeosaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalJeosaatlik = totalJeosaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalJeosaatlik = totalJeosaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalJeosaatlik = totalJeosaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalJeosaatlik),randomnumber))

for iteration2 in range(len(mintotalJeosaatlik)): 
    number = np.random.uniform(mintotalJeosaatlik['CF'][iteration2], maxtotalJeosaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcfjeothermal.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalJeosaatlik['CF'], maxtotalJeosaatlik['CF'], color="gray")
ax.set_title("JEOTERMAL CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)


# 10 tane oluştur random sayı CF'den, random sayılardan her biri için 
# kurulu güçleri çarp, aylık kaynak bazlı üretim tahminim olacak.

