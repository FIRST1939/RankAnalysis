# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:33:57 2019

@author: Mason
"""

import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt

def piecesMath(TeamDf):
    TeamDf['telecargo'] = TeamDf['teleCargoCargo'] + TeamDf['TeleCargoHRocketCargo'] 
    TeamDf['telecargo'] += TeamDf['TeleCargoMRocketCargo'] 
    TeamDf['telecargo'] += TeamDf['TeleCargoLRocketCargo']
  
    TeamDf['sandcargo'] = TeamDf['SSCargoCargo'] + TeamDf['SSCargoSSHRocketCargo']
    TeamDf['sandcargo'] += TeamDf['SSCargoSSMRocketCargo']
    TeamDf['sandcargo'] += TeamDf['SSCargoSSLRocketCargo']
    
    TeamDf['telehatch'] = TeamDf['teleCargoHatch'] + TeamDf['TeleHatchHRocketHatch']
    TeamDf['telehatch'] += TeamDf['TeleHatchMRocketHatch']
    TeamDf['telehatch'] += TeamDf['TeleHatchLRocketHatch']
    
    TeamDf['sandhatch'] = TeamDf['SSCargoHatch'] + TeamDf['SSCargoSSHRocketHatch']
    TeamDf['sandhatch'] += TeamDf['SSCargoSSMRocketHatch']
    TeamDf['sandhatch'] += TeamDf['SSCargoSSLRocketHatch']
    
    TeamDf['teletotal'] = TeamDf['telecargo'] + TeamDf['telehatch']
    
    TeamDf['sandtotal'] = TeamDf['sandcargo'] + TeamDf['sandhatch']
    
    TeamDf['totalcargo'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    
    TeamDf['totalhatch'] = TeamDf['telehatch'] + TeamDf['sandhatch']
    
    TeamDf['totalscored'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    TeamDf['totalscored'] += TeamDf['telehatch']
    TeamDf['totalscored'] += TeamDf['sandhatch']


df = pd.read_csv(filedialog.askopenfilename(title = 'select unfiltered data file'), sep = '|')
df = df.sort_values('teamNo', ascending=True)
piecesMath(df)
teamList = df['teamNo'].drop_duplicates()
df.set_index('teamNo', inplace = True)
piecesMath(df)
data = []
dataArr = []
k=0
greatestLength = 0

for team in teamList:
#    print(team)
    data.append(df.loc[[team], ['totalscored']].get_values())
#    print(df.loc[[team], ['totalscored']].get_values())


for i in data:
    dataArr.append([])
#    if len(i) > greatestLength:
#        greatestLength = len(i)
    for j in i:
        dataArr[k].append(j[0])
#        print(j[0])
        
#    print(' ')
#    print(k)
    k+=1
#print(dataArr)

fig = plt.figure(1, figsize=(30, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(dataArr)
ax.set_xticklabels(teamList.get_values())
plt.grid(True, axis='x')
plt.savefig('Big Boxplot Boi.pdf', bbox_inches='tight')
plt.show()
#plt.savefig('Big Boxplot Boi.png')

#junk = [['tom', 10, 4161, 145, 14, 15, 4 ,15, 15, 14, 41, 51, 561, 41, 41516, 45, 6543, 552, 52, 2, 52, 52, 51, 1, 81557, 651, 41, 4151, 416516, 415163, 651032, 165032, 6513026, 1563, 5132, 41321, 6548, 561, 5332, 153648, 897465, 142, 48651, 1536, 6531, 5631, 32114, 1320, 3120, 
#         465, 84651, 4115, 4651, 451, 4865, 48751, 21354, 31564]]
  
# Create the pandas DataFrame 
#pivotDf = pd.DataFrame(dataArr, columns = teamList) 
#print(pivotDf)
#print(data)
#print(data)