# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 10:20:33 2018

2015 Scouting Rank Analysis Tools

Starting with 2015 because there ranking scores didn't include any ranking 
points other than for WLT.  More recent years with bonus RP for specific 
actions are going to be harder to model.  Can't do 2014 because component score
data isn't available on TBA.
"""

'''
Seeding 

1. Qualification Average
2. Cumulative sum of Coop
3. Cumulative sum of AUTO
4. Cumulative sum of Container
5. Cumulative sum of Tote
6. Cumulative sum of Litter (Container + Landfull + unprocessed)
7. Random FMS

'''

from pprint import pprint
import pandas as pd
import tbaUtils as tba

YEAR = 2015

def maketeamlist(event='mokc'):
    teamdf = pd.DataFrame(tba.get_event_teams(event,YEAR))
    
    #print(teamdf)
    
    return(teamdf.team_number)    
    

def makematchlist(event='mokc'):
    '''
    This JSON response includes nested dictionaries, so it doesn't pandas
    directly well.  Going to deparse it a bit.
    
    Basic strategy is to take the nested levels from a single match and 
    move them into a single-level dictionary, then append them to a new list of
    matches.
    
    After finishing, I force the matches into a pandas DataFrame using the 
    match key formatted like '2015mokc_qm64' as the index.
    '''
    matchlist = tba.get_event_matches(event,YEAR)
    
    #pprint(matchlist[0:5])
    
    
    # Initialize variables then iterate over the matches
    flatmatchlist = []    
    key = []
    for match in matchlist:
        #Start empty for each match
        flatmatch = {}
        
        #Add the key to the dictionary and to the list of keys
        flatmatch['key'] = match['key']
        key.append(match['key'])
        
        #Pick up the basic information
        flatmatch['matchtype'] = match['comp_level']
        flatmatch['matchnum'] = match['match_number']
        
        # Convert the lists of teams to individual positions
        # Change'frc2164' -> '2164' as I go to match the team list
        flatmatch['blue1'] = match['alliances']['blue']['teams'][0][3:] 
        flatmatch['blue2'] = match['alliances']['blue']['teams'][1][3:]
        flatmatch['blue3'] = match['alliances']['blue']['teams'][2][3:]
        flatmatch['red1'] = match['alliances']['red']['teams'][0][3:]
        flatmatch['red2'] = match['alliances']['red']['teams'][1][3:]
        flatmatch['red3'] = match['alliances']['red']['teams'][2][3:]
        
        # Make a list of the teams that don't get seeding points for this match
        flatmatch['ineligible'] = []
        
        if len(match['alliances']['blue']['dqs']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['blue']['dqs'])
        if len(match['alliances']['blue']['surrogates']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['blue']['surrogates'])
        if len(match['alliances']['red']['dqs']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['red']['dqs'])        
        if len(match['alliances']['red']['surrogates']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['red']['surrogates'])
            
        if len(flatmatch['ineligible']) > 0:
            print(flatmatch['ineligible'])
        
        # Pick up all the items in the scoring breakdown that matter for seeding
        flatmatch['cooppts'] = match['score_breakdown']['coopertition_points']
        flatmatch['bluescore'] = match['alliances']['blue']['score']
        flatmatch['blueautopts'] = match['score_breakdown']['blue']['auto_points']
        flatmatch['bluecontainerpts'] = match['score_breakdown']['blue']['container_points']
        flatmatch['bluetotepts'] = match['score_breakdown']['blue']['tote_points']
        flatmatch['bluelitterpts'] = match['score_breakdown']['blue']['litter_points']
        flatmatch['redscore'] = match['alliances']['red']['score']
        flatmatch['redautopts'] = match['score_breakdown']['red']['auto_points']
        flatmatch['redcontainerpts'] = match['score_breakdown']['red']['container_points']
        flatmatch['redtotepts'] = match['score_breakdown']['red']['tote_points']
        flatmatch['redlitterpts'] = match['score_breakdown']['red']['litter_points']        
        
        #Take the complete match and add it to the match list
        flatmatchlist.append(flatmatch)

    key = pd.Series(key, name='key')
    flatmatchdf = pd.DataFrame(flatmatchlist, index=key)        
    return flatmatchdf
        
def calc_seed(matchdf, teamlist):        
    '''
    Take a match results dataframe and a list of teams and create a dataframe
    that contains the seeding rank of each team match by match as the event
    progresses
    '''
    pass #This command does nothing and makes the stub compile cleanly
    

def strip_elims(matchdf):
    '''
    Remove matches that are not qualification matches from the match dataframe.
    Change the key to the match number so they will sort better.
    '''

    print(matchdf[matchdf.matchtype == 'qm'])
        