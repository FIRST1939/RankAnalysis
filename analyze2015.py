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
    
    teamseries = teamdf.team_number
    
    answer = pd.Series.tolist(teamseries)
    
    print(type(answer[0]))
    
    return(answer)    
    

def makematchlist(event='mokc'):
    '''
    This JSON response includes nested dictionaries, so it doesn't pandas
    directly well.  Going to deparse it a bit.
    
    Basic strategy is to take the nested levels from a single match and 
    move them into a single-level dictionary, then append them to a new list of
    matches.  Also calculating ranking points for each alliance and fixing types.
    
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
        flatmatch['matchnum'] = int(match['match_number'])
        
        # Convert the lists of teams to individual positions
        # Change'frc2164' -> '2164' as I go to match the team list
        flatmatch['blue1'] = int(match['alliances']['blue']['team_keys'][0][3:])
        flatmatch['blue2'] = int(match['alliances']['blue']['team_keys'][1][3:])
        flatmatch['blue3'] = int(match['alliances']['blue']['team_keys'][2][3:])
        flatmatch['red1'] = int(match['alliances']['red']['team_keys'][0][3:])
        flatmatch['red2'] = int(match['alliances']['red']['team_keys'][1][3:])
        flatmatch['red3'] = int(match['alliances']['red']['team_keys'][2][3:])
        
        # Make a list of the teams that don't get seeding points for this match
        flatmatch['ineligible'] = []
        
        if len(match['alliances']['blue']['dq_team_keys']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['blue']['dq_team_keys'])
        if len(match['alliances']['blue']['surrogate_team_keys']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['blue']['surrogate_team_keys'])
        if len(match['alliances']['red']['dq_team_keys']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['red']['dq_team_keys'])        
        if len(match['alliances']['red']['surrogate_team_keys']) > 0:
            flatmatch['ineligible'].extend(match['alliances']['red']['surrogate_team_keys'])
            
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
        
        # Calculate RP for red and blue based on match winner

        if flatmatch['bluescore'] > flatmatch['redscore']:
            flatmatch['bluerp'] = 2
            flatmatch['redrp'] = 0
        elif flatmatch['bluescore'] < flatmatch['redscore']:
            flatmatch['bluerp'] = 0
            flatmatch['redrp'] = 2
        else: #tied
            flatmatch['bluerp'] = 1
            flatmatch['redrp'] = 1
        
        #Take the complete match and add it to the match list
        flatmatchlist.append(flatmatch)

    key = pd.Series(key, name='key')
    flatmatchdf = pd.DataFrame(flatmatchlist, index=key)        
    return flatmatchdf
        
def team_seedpts(matchdf):        
    '''
    Take a match results dataframe and create a dataframe
    that contains the seeding points to be applied to each team match by match
    as the event progresses
    '''
    
    bluecolumns = ['bluescore', 'bluerp', 'cooppts', 'blueautopts',
                   'bluecontainerpts', 'bluetotepts', 'bluelitterpts',
                   'ineligible']
    redcolumns = ['redscore', 'redrp', 'cooppts', 'redautopts',
                  'redcontainerpts', 'redtotepts', 'redlitterpts',
                  'ineligible']
                  
    columns = ['matchnum', 'team', 'score', 'rp', 'cooppts', 'autopts',
               'containerpts', 'totepts', 'litterpts', 'ineligible']
                  
    # For each blue team, make a dataframe with their correct columns                  

    blue1df = matchdf.reset_index().set_index(['matchnum', 'blue1'])[bluecolumns]
    blue2df = matchdf.reset_index().set_index(['matchnum', 'blue2'])[bluecolumns]
    blue3df = matchdf.reset_index().set_index(['matchnum', 'blue3'])[bluecolumns]

    # Merge the tables together, then fix the headers to a generic
    blues = [blue1df, blue2df, blue3df]
    bluedf = pd.concat(blues)
    
    bluedf.reset_index(inplace = True)
    
    bluedf.columns = columns
    
    # Same again, but for red
    
    red1df = matchdf.reset_index().set_index(['matchnum', 'red1'])[redcolumns]
    red2df = matchdf.reset_index().set_index(['matchnum', 'red2'])[redcolumns]
    red3df = matchdf.reset_index().set_index(['matchnum', 'red3'])[redcolumns]
    
    reds = [red1df, red2df, red3df]
    
    reddf = pd.concat(reds)
    
    reddf.reset_index(inplace = True)
    
    reddf.columns = columns
    
    # Now that the columns are aligned, glue red and blue together 
    
    fulldf = pd.concat([reddf,bluedf])
    
           
    print(fulldf[fulldf['team'] == 1939])
    
    # Going to need to fix this later to delete row if ineligible.
    
    return fulldf
    

def strip_elims(matchdf):
    '''
    Remove matches that are not qualification matches from the match dataframe.
    Change the key to the match number so they will sort better.
    '''

    newdf = matchdf[matchdf.matchtype == 'qm']
    
    newdf.set_index('matchnum', inplace = True)
    
    #print(newdf.head())
    
    return newdf
    
def matchmtx(teamPts, teamlist):
    '''
    Take the points for each match and apply them to the teams
    '''
    print(teamPts[teamPts['matchnum'] == 1])
    
    print('Matches Played', max(teamPts['matchnum']))
    
    maxmatch = max(teamPts['matchnum'])
    
    teamPtsByMatch = []
    for team in teamlist:
        shortdf = teamPts[teamPts['team'] == team]
        #print(shortdf)
        rp = [0] #at match 0, you have 0 RP
        coop = [0]
        auto = [0]
        cont = [0]
        tote = [0]
        litter = [0]
        
        for match in range(1, maxmatch+1):            
            if shortdf[shortdf['matchnum'] == match].empty:
                rpts = rp[match - 1]
                cpts = coop[match - 1]
                apts = auto[match - 1]
                ctpts = cont[match - 1]
                tpts = tote[match - 1]
                lpts = litter[match - 1]
            else:
                #print(shortdf[shortdf['matchnum'] == match]['rp'])
                rpts = rp[match - 1] + shortdf[shortdf['matchnum']== match]['rp'].iloc[0]
                cpts = coop[match - 1] + shortdf[shortdf['matchnum']== match]['cooppts'].iloc[0]
                apts = auto[match - 1] + shortdf[shortdf['matchnum']== match]['autopts'].iloc[0]
                ctpts = cont[match - 1] + shortdf[shortdf['matchnum']== match]['containerpts'].iloc[0]
                tpts = tote[match - 1] + shortdf[shortdf['matchnum']== match]['totepts'].iloc[0]
                lpts = litter[match - 1] + shortdf[shortdf['matchnum']== match]['litterpts'].iloc[0]
            rp.append(rpts)
            coop.append(cpts)
            auto.append(apts)
            cont.append(ctpts)
            tote.append(tpts)
            litter.append(lpts)
         
        print(team, cont, tote, litter)
        teamPtsByMatch.append({'team': team, 'rp': rp, 'coop': coop, 'auto': auto,
                               'container': cont, 'tote':tote, 'litter': litter})
        
        
            
            
        
    
    
    
def Main():
    '''
    Runs functions in correct order to generate the rankings
    '''
    print('Getting team list\n')
    teamlist = maketeamlist()
    
    print('Making match list and stripping elim rounds\n')
    matchdf = strip_elims(makematchlist())
    
    print('Calculating seeding points\n')
    
    teamSeedPts = team_seedpts(matchdf)
    
    print('Calculating seeding points over time\n')
    
    matchseedmtx = matchmtx(teamSeedPts, teamlist)


Main()        