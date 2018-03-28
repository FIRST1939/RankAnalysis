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

MASTERKEYS = {0: 'RCA/CCA',1: 'Winner',2: 'Finalist',3: 'WFFA/WFA',4: 'DLFA',
              5: 'Volunteer of the Year',9: 'REI/EI',10: 'Rookie All-Star',
              11: 'Gracious Professionalism',12: 'Coopertition',13: 'Judges',
              14: 'Highest Rookie Seed',15: 'Rookie Inspiration',16: 'GM Industrial Design',
              17: 'Quality',18: 'Safety',19: 'Sportsmanship',20: 'Creativity',
              21: 'Excellence in Engineering',22: 'Entrepreneurship',
              23: 'Autodesk Excellence in Design',26: 'Delphi Driving Tomorrows Technology',
              27: 'Imagery',29: 'Innovation in Control',30: 'Team Spirit',
              31: 'Website',32: 'Autodesk Visualization',
              34: 'FIRST Future Innovator', 38: 'Leadership in Controls',
              39: '#1 Seed',40: 'Incredible Play Award',43: 'Best Offensive Round',
              47: 'Outstanding Defense',51: 'Chairmans Award Finalist',
              68: 'Wildcard'}
              
AWDSEQ = ['RCA/CCA', 'Chairmans Award Finalist', 'REI/EI', 'Winner', 'Finalist',
          'Wildcard', 'Excellence in Engineering', 'GM Industrial Design', 
          'Innovation in Control', 'Quality', 'Creativity', 
          'WFFA/WFA', 'DLFA', 'Volunteer of the Year', 'FIRST Future Innovator',
          'Entrepreneurship',
          'Gracious Professionalism', 'Team Spirit', 'Imagery', 'Judges', 'Safety',
          'Rookie All-Star', 'Highest Rookie Seed', 'Rookie Inspiration',
          'Coopertition', 'Sportsmanship', 'Autodesk Excellence in Design',
          'Delphi Driving Tomorrows Technology', 'Website',
          'Autodesk Visualization', 'Leadership in Controls',
          '#1 Seed', 'Incredible Play Award',
          'Best Offensive Round', 'Outstanding Defense']


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
def teamweekmtx(teamdict):
    '''(dict) -> dict
    Take entries like 935: ['2018mokc2', '2018mokc'] and convert to
    935: {2: '2018mokc2', 3: '2018mokc'}
    '''
    
    junk, weeklist = make_eventweekmtx()
    
    result = {}
    
    for team in teamdict:
        result[team] = {}
        for week in weeklist:
            for event in teamdict[team]:                
                if event[4:] in weeklist[week]:                    
                    result[team][week] = event
    
    #print('\nTeam Week Matrix?')
    
    return pd.DataFrame(result).transpose().fillna(value = '')
    
def wrestleawds(awdmatrix, awdkeys):
    masterkeys = MASTERKEYS
    #pprint(masterkeys)
    
    print()
    for i in awdkeys:
        if i not in masterkeys:
            print('Missing Award:', i, awdkeys[i])
            masterkeys[i] = awdkeys[i][0]
    
    #print('\nMaster Keys')
    #pprint(masterkeys)
    currentyear = {}
    allyears = {}
    
    for key in awdmatrix:
        aname = masterkeys[key]
        currentyear[aname] = {}
        allyears[aname] = {}
        
        for team in awdmatrix[key]:
            currentyear[aname][team] = []
            allyears[aname][team] = []
            
            for award in awdmatrix[key][team]:
                if award[0:4] == YEAR:
                    currentyear[aname][team].append(award)
                allyears[aname][team].append(award)

            if len(currentyear[aname][team]) == 0:
                del currentyear[aname][team]
        if len(currentyear[aname]) == 0:
            del currentyear[aname]
        if len(allyears[aname]) == 0:
            del allyears[aname]

    print()
    #print('All')
    #pprint(allyears)

    currentyeardf = pd.DataFrame(currentyear)
    allyearsdf = pd.DataFrame(allyears)
    
    return currentyeardf, allyearsdf
            
def awdcounter(awdmtxdf):
    '''
    Take the award matrix and do a count by team by award.
    Also do a count by team by award for the most recent 4 years (i.e. the
    window in which the same student might have been on the team Freshman to 
    Senior)
    '''
    tgtyears = [YEAR, str(int(YEAR)-1), str(int(YEAR)-2), str(int(YEAR)-3)]
    
    awdmtxdf.fillna(value='0', inplace=True)        
    
    mtx = awdmtxdf.to_dict()    
    
    allcnt = {}
    past4 = {}
    
    for awd in mtx:
        allcnt[awd] = {}
        past4[awd] = {}
        for team in mtx[awd]:
            if mtx[awd][team] == '0':
                allcnt[awd][team] = 0
                past4[awd][team] = 0
            else:               
                for item in mtx[awd][team]:                   
                    if team not in past4[awd]:
                        allcnt[awd][team] = 0
                        past4[awd][team] = 0
                    year = item[0:4]
                    if year in tgtyears:
                        past4[awd][team] += 1
                    allcnt[awd][team] += 1                                        

    past4df = pd.DataFrame(past4)
    allcntdf = pd.DataFrame(allcnt)
                                
    return past4df, allcntdf    
    
    
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
   
    #print('\nKeys')
    #pprint(awdkeys)
  
    print('Team locations:')
    pprint(locations)
    
    curmtx = teamweekmtx(current)    
    teamdf = pd.DataFrame(teamlist).transpose()
    
    #pprint(awdmx)
    
    curawddf, awdmtxdf = wrestleawds(awdmx, awdkeys)
    
    past4cntdf, allawdcntdf = awdcounter(awdmtxdf)
    
    #print(awdmtxdf.head())
    
    with pd.ExcelWriter(xlfile) as writer:
        teamdf.to_excel(writer, 'Team List')
        curmtx.to_excel(writer, 'Team Schedule')
        curawddf.to_excel(writer, 'Current Awards')
        awdmtxdf.to_excel(writer, 'Full Award Matrix')
        past4cntdf.to_excel(writer, 'Awd Count Current Team')
        allawdcntdf.to_excel(writer, 'All Award Count')
        
        
    