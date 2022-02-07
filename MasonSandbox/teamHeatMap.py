# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 19:29:25 2019

@author: bob the builder from starwars 
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
import seaborn as sb


def getArrayFromCSV(dfVar, df, team):
#    for i in range(len(df.loc[[team], [dfVar]])):
    teamdf = df.loc[[team], [dfVar]]
    newArray = teamdf[dfVar].tolist()
                       
    return newArray

def heatMapWithAllBaseVars():    
    for col in heatMapdf.columns:
        yVars.append(col)
    
    for match in df.loc[[team], ["matchNo"]].values:
        matchNum.append(match[0])

    for i in heatMapdf.columns:
        heatMapList.append(getArrayFromCSV(i, heatMapdf, team))
        
#def getTeamArray(team):
#    for match in range(len(heatMapdf.loc[team])):
        
        
def picklistHeatmap():
#    print(df.columns)
#    heatMapdf['avgScored'] = (heatMapdf['telecargo']*3)
#    heatMapdf['avgScored'] += (heatMapdf['sandcargo']*3 + heatMapdf['sandhatch']*5 + heatMapdf['telehatch']*2)
    for col in heatMapdf.columns:
        yVars.append(col)
    
    for teams in df['team']:
        matchNum.append(teams)
        
    for i  in heatMapdf.columns:
        heatMapList.append(df[i])

##    


def heatMapWithTotalVars():
    piecesMath(df)
    advdf = df.loc[[team], ['telecargo','sandcargo', 'telehatch', 'sandhatch', 'totalscored', 'teletotal', 'sandtotal', 'totalcargo', 'totalhatch' ]]
#    print(df.loc[[team], ['totalscored']])
    for col in advdf.columns:
        yVars.append(col)
        
    for match in df.loc[[team], ["matchNo"]].values:
#        print(match)
        matchNum.append(match[0])
        
    for i in advdf.columns:
        heatMapList.append(getArrayFromCSV(i, advdf, team))
    
def TeamStats(TeamDf):
    '''
    Takes full dataframe, and creates per match calculated values. Creates a pivot
    dataframe with overall team statistics
    '''
    # Normalize column names
    # Database renamed match and team to matchNo and teamNo.  We put back.
    TeamDf.rename(columns = {'teamNo':'team', 'matchNo': 'match'}, inplace = True)
    
    TeamDf.set_index('team', inplace=True)
    
    # Calculate cube usage
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
    
    TeamDf['teleTotal'] = TeamDf['telecargo'] + TeamDf['telehatch']
    
    TeamDf['sandTotal'] = TeamDf['sandcargo'] + TeamDf['sandhatch'] 
    
    TeamDf['totalcargo'] = TeamDf['telecargo'] + TeamDf['sandcargo']
    
    TeamDf['totalhatch'] = TeamDf['telehatch'] + TeamDf['sandhatch']
  
    tempDf = TeamDf[['team', 'reachLvl1','reachLvl2','reachLvl3']]
    climbDf = pd.pivot_table(tempDf,values=['reachLvl1','reachLvl2','reachLvl3'],index=['team'],
                             columns=['reachLvl1', 'reachLvl2', 'reachLvl3'], aggfunc=len, fill_value=0)
    print(climbDf)
    climbDf.reset_index(inplace = True)
    
    #TeamDf['PostiveComments'] = TeamDf['postCommentsPro'] 
    
    TeamDf['totalmatches'] = 1
    
    AvgTeamPivot = pd.pivot_table(TeamDf, values = ['telecargo', 'sandcargo', 'telehatch', 'sandhatch', 'totalscored', 'totalcargo', 'totalhatch'], index = 'team', aggfunc = np.average)
    MatchCount = pd.pivot_table(TeamDf, values = ['totalmatches', 'reachLvl1', 'reachLvl2', 'reachLvl3'], index = 'team', aggfunc = np.count_nonzero)
    #Comments = pd.pivot_table(TeamDf, values = ['PositiveComments'], index = 'team', aggfunc = lambda x: ' '.join(x))
    
    AvgTeamPivot.reset_index(inplace = True)
    MatchCount.reset_index(inplace = True)
    #Comments.reset_index(inplace = True)
                                                                               
    TeamPivot = pd.merge(AvgTeamPivot, MatchCount, on = 'team')
    
    TeamPivot = pd.merge(TeamPivot, climbDf, on = 'team')
    
    
    TeamPivot.rename(columns = {"Did not Try": 'noAttempt', "Attempt Level One Climb": 'attemptLvl1', 
                                "Climbed Level One": 'reachLvl1', "Attempt Level Two Climb": 'attemptLvl2',
                                "Climbed Level Two": 'reachLvl2', "Attempt Level Three Climb": 'attemptLvl3',
                                "Climbed Level Three": 'reachLvl3', "Deployed Ramps": 'deployedRamps', 
                                "Attempted Deploying Ramps": 'attemptDeployedRamps', "Used Another Robot": 'usedAnotherRobot',
                                "Lifted Another Robot": 'lift', "Attempted Lifting Another Robot": 'attemptLift'}, inplace = True)
    
    return TeamPivot   
    
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



selection = input('Enter 0 to generate a team heatmap, enter anything else to generate picklist heatmap:')
if selection == '0':    
    team = int(input('Enter Which Team you want to heatmap a graph for:'))
heatMapList=[]
matchNum = []        
yVars = []


if selection == '0':
    dropLS = ['id', 'teamNUM', 'matchNo', 'startPOS', 'startLeft', 'Comments', 'scoutName', 'startRight']
    df = pd.read_csv(filedialog.askopenfilename(title = 'select data file'), sep = '|')
    heatMapdf = df.drop(dropLS, axis = 1)
    df.set_index("teamNo", inplace = True)
    heatMapWithTotalVars()
   
else:
    dropLS = ['team', '(0, 0, 0)', '(0, 0, 1)', '(0, 1, 0)', '(1, 0, 0)', '(1, 0, 1)', '(1, 1, 0)', 'totalmatches','Unnamed: 0']
    df = pd.read_csv(filedialog.askopenfilename(title = 'select analyzed data file'), sep = ',')
    print(df.columns)
    heatMapdf = df.drop(dropLS, axis = 1)
    picklistHeatmap()
    plt.figure(figsize=(50,3))


heat_map = sb.heatmap(heatMapList, cmap="YlGn", annot=True, yticklabels=yVars, xticklabels=matchNum)
savethatsSaved = heat_map.get_figure()

plt.show()

if selection == '0':
   savethatsSaved.savefig(r'/Users/Mason/Desktop/heatmap for ' + str(team) +'.pdf', bbox_inches='tight')
#    plt.openfig('heatmap.fig')
#    
#    'C:\\Users\\Mason\\Desktop' +
else:
    savethatsSaved.savefig(r'/Users/Mason/Desktop/heatmap picklist at ' + input('Enter which event you want to display in the file name here:') +'.pdf', bbox_inches='tight')
    print('heatmap saved')