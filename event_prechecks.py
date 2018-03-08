# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 21:58:47 2018


Event prescout with emphasis on past performance and interesting judging
things.

Fix list:

Fix the scratchfile write
Make a week by week matrix of who is playing when this year
Pull the Key Codex from the file
Replace the award numbers with names from the codex
Fix the excel write
Who won what last year and write to teh excel
Do a breakdown on the bad awards by level (CCA/RCA/DCA using the event codes)
"""
import tbaUtils
import pandas as pd
from pprint import pprint

YEAR = '2018'


def maketeamlist(event):
    '''
    Pull big list, strip out the interesting parts, and return as a dict.
    '''
    
    raw = get_event_teams(event)
    
    result = {}
    
    for entry in raw:
        teamnum = entry['team_number']
        name = entry['nickname']
        state = entry['state_prov']
        school = entry['name'].split('&')[-1]
        
        #print(teamnum, name, state, school)
        result[teamnum] = {'name': name, 'state':state, 'school':school}
        
    return result        

def locstats(teamdict):
    '''
    Where are the teams from, generally speaking.
    '''
    locgrid = {}    
    
    for team in teamdict:
        state = teamdict[team]['state']
        if state not in locgrid:
            locgrid[state] = 0
        
        locgrid[state] += 1
        
    return locgrid
    
def eventmtx(teamlist):
    '''
    Take each team, get their event history (which includes this years).
    Make two dicts, one with everything, one with just this year.
    '''
    allevents = {}
    currentevents = {}    
    
    
    for team in teamlist:
        allevents[team] = get_team_history(team)
        
        currentevents[team] = []
        
        for event in allevents[team]:
            if YEAR in event:
                currentevents[team].append(event)
                
    return currentevents, allevents
    
def awdmtx(teamlist):
    '''
    Take each team, get their award history.
    '''
    
    allawds = {}
    
    awdkeys = {}
    awdmtx = {}
    
    for team in teamlist:
        allawds[team] = get_award_history(team)
              
        for awddict in allawds[team]:
            
            atype = awddict['award_type']
            aname = awddict['name']
            aevent = awddict['event_key']
            
            # Make a matrix of all the type number to award name mappings
            if atype not in awdkeys:
                awdkeys[atype] = []
            if aname not in awdkeys[atype]:
                awdkeys[atype].append(aname)
            
            # Make a matrix of award key to team to event mappings
            if atype not in awdmtx:
                awdmtx[atype] = {}
            
            if team not in awdmtx[atype]:
                awdmtx[atype][team] = []
            
            awdmtx[atype][team].append(aevent)
                           
            
    return allawds, awdkeys, awdmtx
    
def prescout_event(event):
    '''
    Combine commands together, write to a file.
    '''
    
    xlfile = 'Prescout-' + YEAR + '-' + event + '.xlsx'
    scratchfile = 'Prescout-' + YEAR + '-' + event + '-notes.txt'
        
    teamlist = maketeamlist(event)        
    locations = locstats(teamlist)        
    current, fullhist = eventmtx(teamlist)
    allawds, awdkeys, awdmx = awdmtx(teamlist)
    
    with open(scratchfile, 'w') as file:
        file.write('Team List\n')
        file.write(str(teamlist))
        file.write('\n\nLocation Stats\n')
        file.write(str(locations))
        file.write('\n\nCurrent Events\n')
        file.write(str(current))
        file.write('\n\nAward List\n')
        file.write(str(allawds))
        file.write('\n\nAward Keys\n')
        file.write(str(awdkeys))
   
    awdmtxdf = pd.DataFrame(awdmx)
    pprint(current)        
    
    pprint(awdkeys)

    print()    
    teamdf = pd.DataFrame(teamlist)
    #currdf = pd.DataFrame(current)
    #awdkeydf = pd.DataFrame(awdkeys)
    
    
    
    with pd.ExcelWriter(xlfile) as writer:
        awdmtxdf.to_excel(writer, 'Award Matrix')
        teamdf.to_excel(writer, 'Team List', index=False)