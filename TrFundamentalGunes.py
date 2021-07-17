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
df = df[12:63]
df = df.reset_index(drop=False)


start = pd.to_datetime('2017-01-01')
end = pd.to_datetime('2021-04-01')
rng = pd.date_range(start, end, freq='H')
len(rng)
rng = rng[0:-1]
len(rng)
rng = pd.DataFrame(rng)
rng = rng.set_axis(['DateTime'], axis=1, inplace=False)
rng = rng.set_index('DateTime')

# lisanssiz = yekdem.lisanssiz_uevm(baslangic_tarihi='2017-01-01', bitis_tarihi='2021-03-31')
# lisanssiz['DateTime'] = pd.to_datetime(lisanssiz.Tarih) + lisanssiz.Saat.astype('timedelta64[h]')
# lisanssiz = pd.merge(lisanssiz, rng, how="outer", on=["DateTime", "DateTime"])
# lisanssiz = lisanssiz.set_index('DateTime')
# lisanssiz = lisanssiz.drop('Tarih', axis = 1)
# lisanssiz = lisanssiz.drop('Saat', axis = 1)
# lisanssiz = pd.DataFrame(lisanssiz['Güneş'])
# # lisanssiz = lisanssiz.replace(np.nan, 0)
# lisanssiz.sort_values(by='DateTime', ascending = True, inplace=True)


# uretim1 = uretim.__gerceklesen(baslangic_tarihi='2017-01-01', bitis_tarihi='2021-03-31')
# uretim1['DateTime'] = pd.to_datetime(uretim1.Tarih) + uretim1.Saat.astype('timedelta64[h]')
# uretim1 = pd.merge(uretim1, rng, how="outer", on=["DateTime", "DateTime"])
# uretim1 = uretim1.set_index('DateTime')
# uretim1 = uretim1.drop('Tarih', axis = 1)
# uretim1 = uretim1.drop('Saat', axis = 1)
# uretim1 = pd.DataFrame(uretim1['Güneş'])
# # uretim1 = uretim1.replace(np.nan, 0)
# uretim1.sort_values(by='DateTime', ascending = True, inplace=True)

# uretim1['Güneş'] = uretim1['Güneş'] + lisanssiz['Güneş']

# uretim1 = uretim1.reset_index(drop=False)
# uretim1['year'] = pd.DatetimeIndex(uretim1['DateTime']).year
# uretim1['month'] = pd.DatetimeIndex(uretim1['DateTime']).month

# uretim1['Güneş'].isnull().values.any()
# uretim1['Güneş'].isnull().sum()

# uretim1.to_excel('trfundamentalgunes.xlsx')

#%% VERİ OKUMA

uretim1 = pd.read_excel('trfundamentalgunes.xlsx',parse_dates=True)

uretim1['hour'] = pd.DatetimeIndex(uretim1['DateTime']).hour
uretim1['day'] = pd.DatetimeIndex(uretim1['DateTime']).day
uretim1['dayofyear'] = pd.DatetimeIndex(uretim1['DateTime']).dayofyear
uretim1['Hour_of_Year'] = (pd.DatetimeIndex(uretim1['DateTime']).dayofyear - 1) * 24 + pd.DatetimeIndex(uretim1['DateTime']).hour


#%% MODEL
minGunes = uretim1.groupby(['year','month'], as_index=False)['Güneş'].min()
totalGunes = uretim1.groupby(['year','month'], as_index=False)['Güneş'].sum()
maxGunes = uretim1.groupby(['year','month'], as_index=False)['Güneş'].max()

minGunes1 = uretim1.groupby(['month'], as_index=False)['Güneş'].min()
maxGunes1 = uretim1.groupby(['month'], as_index=False)['Güneş'].max()


totalGunes['numdays'] = np.zeros(len(totalGunes))

for i in range(len(totalGunes)):
    year1 = totalGunes['year'][i]
    month1 = totalGunes['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalGunes['numdays'][i] = total
    
df1 = df['GÜNEŞ']
totalGunes = pd.concat([totalGunes, df1], axis=1).reindex(maxGunes.index)

totalGunes['CF'] = totalGunes.Güneş / (totalGunes.numdays * 24 * totalGunes.GÜNEŞ)
    
minGunestotalGunes = totalGunes.groupby(['month'], as_index=False)['CF'].min()
maxGunestotalGunes = totalGunes.groupby(['month'], as_index=False)['CF'].max()

meanGunestotalGunes = totalGunes.groupby(['month'], as_index=False)['CF'].mean()

cf = np.zeros(len(maxGunestotalGunes))
cf = pd.DataFrame(cf)
cf = cf.set_axis(['CF'], axis=1, inplace=False)

for iteration2 in range(len(maxGunestotalGunes)):  
    number = random.uniform(minGunestotalGunes['CF'][iteration2], maxGunestotalGunes['CF'][iteration2])
    cf['CF'][iteration2] = number

x = np.arange(0, 12)
ax = plt.figure().add_subplot(111)
ax.plot(cf, color="red", label="Random Values")
ax.plot(meanGunestotalGunes['CF'], color="yellow", label="Average Values")
ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in minGunestotalGunes['month']]
ax.fill_between(x, minGunestotalGunes['CF'], maxGunestotalGunes['CF'], color="gray")
ax.set_title("SOLAR CAPACITY FACTOR", fontsize=12)
ax.set_xlabel('Months', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)
ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels)

#%%########################################################

#############        SAATLİK MODEL        #################

###########################################################

minGunessaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Güneş'].min()
totalGunessaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Güneş'].sum()
maxGunessaatlik = uretim1.groupby(['year','month','day','hour'], as_index=False)['Güneş'].max()


totalGunessaatlik['numdays'] = np.zeros(len(totalGunessaatlik))

for i in range(len(totalGunessaatlik)):
    year1 = totalGunessaatlik['year'][i]
    month1 = totalGunessaatlik['month'][i]
    total = number_of_days_in_month(year=year1, month=month1)
    totalGunessaatlik['numdays'][i] = total


#%% KURULU GÜÇ EKLEME

totalGunessaatlik['kurulu guc'] = np.zeros(len(totalGunessaatlik))
count = 0
for iteration3 in range(len(totalGunessaatlik)):
    if totalGunessaatlik['month'][iteration3] != df['Month'][count]:
        count = count + 1        
    if totalGunessaatlik['month'][iteration3] == df['Month'][count]:
        totalGunessaatlik['kurulu guc'][iteration3] = df['GÜNEŞ'][count]

totalGunessaatlik['CF'] = totalGunessaatlik['Güneş'] / (totalGunessaatlik['kurulu guc'])

totalGunessaatlik = pd.concat([totalGunessaatlik, uretim1['Hour_of_Year']], axis=1).reindex(maxGunessaatlik.index)


minnn = totalGunessaatlik.groupby(['year','month'], as_index=False)['CF'].min()
meannn = totalGunessaatlik.groupby(['year','month'], as_index=False)['CF'].mean()
maxxx = totalGunessaatlik.groupby(['year','month'], as_index=False)['CF'].max()


mintotalGunessaatlik = totalGunessaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].min()
maxtotalGunessaatlik = totalGunessaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].max()
meantotalGunessaatlik = totalGunessaatlik.groupby(['Hour_of_Year'], as_index=False)['CF'].mean()


randomnumber = 50

random2 = np.zeros((len(maxtotalGunessaatlik),randomnumber))

for iteration2 in range(len(mintotalGunessaatlik)): 
    number = np.random.uniform(mintotalGunessaatlik['CF'][iteration2], maxtotalGunessaatlik['CF'][iteration2],randomnumber).reshape(randomnumber,1)
    number = np.transpose(number)
    random2[iteration2] = number 

# random2 = pd.DataFrame(random2)
# random2.to_excel('random2.xlsx')


saatlikcf = np.mean(random2, axis=1)
saatlikcf = pd.DataFrame(saatlikcf)
saatlikcf = saatlikcf.set_axis(['CF'], axis=1, inplace=False)
saatlikcf.to_excel('saatlikcfsolar.xlsx')


x = np.arange(0, 8784)
ax = plt.figure().add_subplot(111)
ax.plot(saatlikcf, color="red", label="Random Values")
ax.fill_between(x, mintotalGunessaatlik['CF'], maxtotalGunessaatlik['CF'], color="gray")
ax.set_title("SOLAR CAPACITY FACTOR", fontsize=10)
ax.set_xlabel('Hours of Year', fontsize=12)
ax.set_ylabel('Capacity Factor', fontsize=12)
ax.legend(loc="best", prop={'size': 8})
ax.grid(True)