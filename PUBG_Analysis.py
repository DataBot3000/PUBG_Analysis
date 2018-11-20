# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:43:56 2018
Kaggle Competition for PUBG video game analysis
taken from: https://www.kaggle.com/deffro/eda-is-fun/notebook

@author: jlewin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

train = pd.read_csv("C:\\Users\\Jlewin\\Downloads\\train_V2.csv")
train.info()
train.head()


#Now that we have an understanding of the data, lets explore it 
#The Killers
print("The average person kills {:.4f} players, 99% of people have {} kills or less, while the most kills ever recorded is {}".format(train['kills'].mean(),train['kills'].quantile(0.99), train['kills'].max()))
#Lets plot the kill counts to visualize
data = train.copy()
data.loc[data['kills'] > data['kills'].quantile(0.99)] = '8+'
plt.figure(figsize=(15,10))
sns.countplot(data['kills'].astype('str').sort_values())
plt.title("Kill Count", fontsize=15)
plt.show

#Majority of people can't even make a single kill, what about damage? 
data = train.copy()
plt.figure(figsize=(10,5))
plt.title("Damage Dealt by 0 killers", fontsize=10)
sns.distplot(data['damageDealt'])
plt.show()
#most don't even do any damage 

print("{} players ({:.4f}%) have won without a single kill!".format(len(data[data['winPlacePerc']==1]), 
      100*len(data[data['winPlacePerc']==1])/len(train)))
data1 = train[train['damageDealt']==0].copy()
print("{} players ({:.4f}%) have won without dealing damage!".format(len(data1[data1['winPlacePerc']==1]), 100*len(data1[data1['winPlacePerc']==1])/len(train)))

#Let's plot win placement percentage vs kills
# GETTING ISSUE DISPLAYING CHART PROPERLY
#sns.jointplot(x="winPlacePerc", y="kills", data=train, height=10, ratio=3, color="r")
#plt.show()


kills = train.copy()
kills['killsCategories'] = pd.cut(kills['kills'], [-1, 0, 2, 5, 10, 60], labels=['0_kills', '1-2_kills', '3-5_kills', '6-10_kills', '10+_kills'])

plt.figure(figsize=(10,5))
sns.boxplot(x="killsCategories", y="winPlacePerc", data=kills)
plt.show()

# What is the distribution of game types: solo, duo, squads?
solos = train[train['numGroups']>50]
duos = train[(train['numGroups']>25) & (train['numGroups']<=50)]
squads = train[train['numGroups']<=25]
print("There are {} ({:.2f}%) solo games, {} ({:.2f}%) duo games and {} ({:.2f}%) squad games.".format(len(solos), 100*len(solos)/len(train),
      len(duos), 100*len(duos)/len(train), len(squads), 100*len(squads)/len(train),))
# looks like 16% are solo, 74% are duo, and 10% are squads 

# What does the distribution of kills across team types look like?
f,ax1 = plt.subplots(figsize =(10,5))
sns.pointplot(x='kills',y='winPlacePerc',data=solos,color='black',alpha=0.8)
sns.pointplot(x='kills',y='winPlacePerc',data=duos,color='#CC0000',alpha=0.8)
sns.pointplot(x='kills',y='winPlacePerc',data=squads,color='#3399FF',alpha=0.8)
plt.text(37,0.6,'Solos',color='black',fontsize = 17,style = 'italic')
plt.text(37,0.55,'Duos',color='#CC0000',fontsize = 17,style = 'italic')
plt.text(37,0.5,'Squads',color='#3399FF',fontsize = 17,style = 'italic')
plt.xlabel('Number of kills',fontsize = 15,color='blue')
plt.ylabel('Win Percentage',fontsize = 15,color='blue')
plt.title('Solo vs Duo vs Squad Kills',fontsize = 20,color='blue')
plt.grid()
plt.show()

#interestingly the solos and duos teams seem to behave normally with a higher chance of winning the more kills you have
# but the squads team seems to have a high volitility of win percentage after 7 kills

#lets look at the correlation of variables 
f,ax = plt.subplots(figsize=(15, 15))
sns.heatmap(train.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()
#seems like boosts, walkdistance and weaponsAcquired have a higher correlation with winpercentage
# lets zoom in on the top 5 most positive correlations

k = 5 
f,ax = plt.subplots(figsize=(11,11))
cols = train.corr().nlargest(k, 'winPlacePerc')['winPlacePerc'].index
cm = np.corrcoef(train[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()
