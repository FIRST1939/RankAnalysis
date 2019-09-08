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

for col in heatMapdf.columns:
    yVars.append(col)
    
for match in df.loc[[team], ["matchNo"]]:
    matchNum.append(match)

for i in heatMapdf.columns:
    heatMapList.append(getArrayFromCSV(i, heatMapdf, team))

#print(heatMapdf)
print(yVars)
#print(heatMapList)
#print(heatMapList)
#print(df.loc[[team], ["matchNo"]])
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

# Loop over data dimensions and create text annotations.
for i in range(len(yVars)):
    for j in range(len(matchNum)):
        text = ax.text(j, i, heatMapList[i, j],
                       ha="center", va="center", color="w")


ax.set_title(team)
fig.tight_layout()
plt.show()