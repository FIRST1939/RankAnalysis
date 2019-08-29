# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:11 2019

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
    
    TeamDf['totalscored'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    TeamDf['totalscored'] += TeamDf['telehatch']
    TeamDf['totalscored'] += TeamDf['sandhatch']
    
    TeamDf['teletotal'] = TeamDf['telecargo'] + TeamDf['telehatch']
    
    TeamDf['sandtotal'] = TeamDf['sandcargo'] + TeamDf['sandhatch']
    
    TeamDf['totalcargo'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    
    TeamDf['totalhatch'] = TeamDf['telehatch'] + TeamDf['sandhatch']
#import numpy

team = int(input('Enter Which Team you want to generate a graph for:'))
print('Enter 0 to generate a total pieces graph')
print('Enter 1 to generate a sandstorm graph')
print('Enter 2 to generate a tele graph')
selection = input('Enter your selection here: ')

df = pd.read_csv(filedialog.askopenfilename(title = 'select MatchList file'), sep = '|')
df.set_index("teamNo", inplace = True)

piecesMath(df)

print(df.loc[[team], ["matchNo"]])
#print(df.loc[[team], ["totalscored"]])
#print(df.loc[[team], ["totalCargo"]])
#print(df.loc[[team], ["totalHatch"]])

if selection == "0":
    plt.figure()
    
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Pieces')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalscored"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalcargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["totalhatch"]], color="red")
    plt.ylabel('HP')
    
if selection == "1":
    plt.figure()
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Sand')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandtotal"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Sand Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandcargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Sand Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["sandhatch"]], color="red")
    plt.ylabel('HP')

if selection == "2":
    plt.figure()
    plt.subplots(sharey = 'col')

    plt.subplot(311)
    plt.title('Total Tele Pieces')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["teletotal"]])
    plt.ylabel('Total Objects')
    
    plt.subplot(312)
#    plt.title('Total Tele Cargo')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["telecargo"]], color="green")
    plt.ylabel('Cargo')

    plt.subplot(313)
#    plt.title('Total Tele Hatch')
    plt.scatter(df.loc[[team], ["matchNo"]], df.loc[[team], ["telehatch"]], color="red")
    plt.ylabel('HP')

