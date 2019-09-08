# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 19:29:25 2019

@author: Mason
"""

import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog


def getArrayFromCSV(dfVar, df, team):
#    for i in range(len(df.loc[[team], [dfVar]])):
    teamdf = df.loc[[team], [dfVar]]
    newArray = teamdf[dfVar].tolist()
                       
    return newArray

def heatMapWithAllBaseVars():    
    for col in heatMapdf.columns:
        yVars.append(col)
    
    for match in df.loc[[team], ["matchNo"]]:
        matchNum.append(match)

    for i in heatMapdf.columns:
        heatMapList.append(getArrayFromCSV(i, heatMapdf, team))
    


def heatMapWithTotalVars():
    piecesMath(df)
    advdf = df.loc[[team], ['telecargo','sandcargo', 'telehatch', 'sandhatch', 'totalscored', 'teletotal', 'sandtotal', 'totalcargo', 'totalhatch' ]]
#    print(advdf)
    for col in advdf.columns:
        yVars.append(col)
        
    for match in df.loc[[team], ["matchNo"]]:
        matchNum.append(match)
        
    for i in advdf.columns:
        heatMapList.append(getArrayFromCSV(i, advdf, team))
    
    
    
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

df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = '|')
df.set_index("teamNo", inplace = True)


dropLS = ['id', 'teamNUM', 'matchNo', 'startPOS', 'startLeft', 'Comments', 'scoutName', 'startRight']

heatMapdf = df.drop(dropLS, axis = 1)
#df.drop(labels=dropLS)
print(df.drop(dropLS, axis=1))

team = 1939
heatMapList=[]
matchNum = []        
yVars = []


#print(heatMapdf)
#print(yVars)
#print(heatMapList)
#print(heatMapList)
#print(df.loc[[team], ["matchNo"]])
#heatMapWithAllBaseVars()
heatMapWithTotalVars()
fig, ax = plt.subplots()
im = ax.imshow(heatMapList)

ax.set_xticks(np.arange(len(matchNum)))
ax.set_yticks(np.arange(len(yVars)))
# ... and label them with the respective list entries
#print(farmers)
ax.set_xticklabels(matchNum)
ax.set_yticklabels(yVars)
    
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

ax.set_title(team)
fig.tight_layout()
plt.show()