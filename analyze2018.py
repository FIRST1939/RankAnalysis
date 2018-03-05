# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 10:22:32 2018

Models 2018 game and ranking movement
"""

from pprint import pprint
import pandas as pd
import tbaUtils as tba
import matplotlib




def qual_model():
    autoticks = 15
    teleticks = 135
    autorun = 5
    autoscaleown = 2
    autoscaletick = 2
    autoswitchown = 2
    autoswitchtick = 2
    telescaleown = 1
    telescaletick = 1
    teleswitchown = 1
    teleswitchtick = 1
    boosttickbonus = 1 #that is one extra point per tick
    boosttime = 10
    vaultcube = 5
    maxcube = 9
    park = 5
    climb = 30
    
    fbrp = 1
    aqrp = 1
    winrp = 2
    tierp = 1
    
    #Per team update 1, the scale has to tip for a full second to establish
    #Ownership, so removing the tick 0 points for ownership    
    
    maxautoscale = autoscaletick * autoticks 
    maxautoswitch = autoswitchtick * autoticks
    maxautoscore = autorun * 3 + maxautoscale + maxautoswitch
    
    maxtelescale = telescaletick * teleticks
    maxteleswitch = teleswitchtick * teleticks
    maxvault = vaultcube * maxcube
    maxclimb = 3 * climb
    maxboost = boosttickbonus * boosttime
    
    #maxboost is doubled here because we're boosting the scale and switch    
    maxtelescore = maxtelescale + maxteleswitch + maxvault + maxclimb + maxboost * 2
    
    maxscore = maxtelescore + maxautoscore
    
    print('Qualification Match Model')
                   
    print('Max scores:', maxautoscore, maxtelescore, maxscore)
    
    maxscalepoints = maxautoscale + maxtelescale + maxboost
    
    print('Scale points:', maxscalepoints)
    
    chokescore = maxscore - (maxscalepoints / 2)
    '''
    Chokehold threshold - if you score every possible point without the scale,
    and your opponent does the same, and you also score more than half the 
    available scale points, it is no longer possible for them to win.
    '''
    
    print('Chokehold Score:', chokescore)
    
    print('Max points without scale:', maxscore - maxscalepoints)
    
    print('Max points without climbing:', maxscore - maxclimb + 3 * park)
    

def interesting_stats(event):
    '''
    Get the raw data required to calculate
    Percentage of successful climb attempts
    Percentage of auto-move
    Percentage of Quest RP
    Percentage of Boss RP
    Percentage decided by fouls
    Average number of power-ups used (by both alliances (max 6))
    '''
    
    eventdata = get_event_matches(event)
    
    results = {'qm': {'mp': 0, 'climbs': [], 'autorun': [], 'quests': [], 'boss': [], 'fv': [], 'pu': []}, 
               'qf': {'mp': 0, 'climbs': [], 'autorun': [], 'quests': [], 'boss': [], 'fv': [], 'pu': []}, 
               'sf': {'mp': 0, 'climbs': [], 'autorun': [], 'quests': [], 'boss': [], 'fv': [], 'pu': []}, 
               'f': {'mp': 0, 'climbs': [], 'autorun': [], 'quests': [], 'boss': [], 'fv': [], 'pu': []}}
    
    for event in eventdata:
        climbs = 0
        autorun = 0
        quests = 0
        boss = 0
        penalties = []
        scores = []
        pu = []
        
        if event['actual_time'] != None:
        
            for alliance in ['red', 'blue']:
                for bot in ['Robot1', 'Robot2', 'Robot3']:
                    #print(event['score_breakdown'][alliance])
                    #print(alliance, bot)
                    #print(event['score_breakdown'][alliance]['endgame' + bot])
                    if event['score_breakdown'][alliance]['endgame' + bot] == 'Climbing':
                        climbs += 1
                    if event['score_breakdown'][alliance]['auto' + bot] == 'AutoRun':
                        autorun += 1
                if event['score_breakdown'][alliance]['autoQuestRankingPoint']:
                    quests += 1
                if event['score_breakdown'][alliance]['faceTheBossRankingPoint']:
                    boss += 1
                    if boss > 2:
                        print('\nSomething is weird here\n')
                        pprint(event)
                for item in ['Boost', 'Force', 'Levitate']:
                    pu.append(event['score_breakdown'][alliance]['vault'+item+'Played'])
                penalties.append(event['score_breakdown'][alliance]['foulPoints'])
                scores.append(event['alliances'][alliance]['score'])
                
            margin = abs(scores[0] - scores[1])
            if scores[0] > scores[1]: #red victory
                if margin < (penalties[0] - penalties[1]):
                    #Red received more foul points than the margin
                    results[event['comp_level']]['fv'].append(1)
                else:
                    results[event['comp_level']]['fv'].append(0)
            elif scores[0] < scores[1]: #blue victory
                if margin < (penalties[1] - penalties[0]):
                    #Blue received more foul points than the margin
                    results[event['comp_level']]['fv'].append(1)
                else:
                    results[event['comp_level']]['fv'].append(0)
            else: #tie
                if penalties[1] != penalties[0]:
                    #Tied because of penalty points
                    results[event['comp_level']]['fv'].append(1)
                else:
                    results[event['comp_level']]['fv'].append(0)
            
            results[event['comp_level']]['mp'] += 1
            results[event['comp_level']]['climbs'].append(climbs)
            results[event['comp_level']]['autorun'].append(autorun)
            results[event['comp_level']]['quests'].append(quests)
            results[event['comp_level']]['boss'].append(boss)
            results[event['comp_level']]['pu'].append(pu)
    
    return results
        
            
def prop_bets(event):
    raw = interesting_stats(event)
    
    cooked = {}
    
    for complvl in raw:
        cooked[complvl] = {}
        
        if raw[complvl]['mp'] != 0:
            cooked[complvl]['autorun'] = sum(raw[complvl]['autorun']) / raw[complvl]['mp']
            cooked[complvl]['boss'] = sum(raw[complvl]['boss']) / raw[complvl]['mp']
            cooked[complvl]['quests'] = sum(raw[complvl]['quests']) / raw[complvl]['mp']
            cooked[complvl]['climbs'] = sum(raw[complvl]['climbs']) / raw[complvl]['mp']
            cooked[complvl]['foulvictory'] = sum(raw[complvl]['fv']) / raw[complvl]['mp']
            
            cooked[complvl]['powerUp'] = {}
            cooked[complvl]['powerUp']['Boost'] = [0, 0, 0, 0] #Total, L1, L2, L3
            cooked[complvl]['powerUp']['Force'] = [0, 0, 0, 0]
            cooked[complvl]['powerUp']['Levitate'] = 0
                    
            for match in raw[complvl]['pu']:
                if match[0] == 1:
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][1] += 1
                elif match[0] == 2:                
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][2] += 1
                elif match[0] == 3:                
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][3] += 1                
            
                if match[3] == 1:
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][1] += 1
                elif match[3] == 2:                
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][2] += 1
                elif match[3] == 3:                
                    cooked[complvl]['powerUp']['Boost'][0] += 1
                    cooked[complvl]['powerUp']['Boost'][3] += 1                
    
                if match[1] == 1:
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][1] += 1
                elif match[1] == 2:                
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][2] += 1
                elif match[1] == 3:                
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][3] += 1                
    
                if match[4] == 1:
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][1] += 1
                elif match[4] == 2:                
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][2] += 1
                elif match[4] == 3:                
                    cooked[complvl]['powerUp']['Force'][0] += 1
                    cooked[complvl]['powerUp']['Force'][3] += 1         
                
                if match[2] == 3:
                    cooked[complvl]['powerUp']['Levitate'] += 1
                if match[5] == 3:
                    cooked[complvl]['powerUp']['Levitate'] += 1
                
            putot = cooked[complvl]['powerUp']['Boost'][0] 
            putot += cooked[complvl]['powerUp']['Force'][0]
            putot += cooked[complvl]['powerUp']['Levitate']
            
            cooked[complvl]['puavg'] = putot /  raw[complvl]['mp']
            
            cooked[complvl]['mp'] = raw[complvl]['mp']
    
    return cooked
    
def prop_bets_week(week):
    scratch, eventmtx = make_eventweekmtx()
    
    eventlist = eventmtx[week]
    
    props = {}
    
    for event in eventlist:
        print(event)
        props[event] = prop_bets(event)['qm']
    
    pprint(props)
    
    propdf = pd.DataFrame(props).transpose()
    
    cols = propdf.columns.tolist()
    
    #cols = ['autorun', 'boss', 'climbs', 'foulvictory', 'mp', 'powerUp', 'puavg', 'quests']
    cols = ['mp', 'foulvictory', 'autorun', 'quests', 'climbs', 'boss', 'puavg', 'powerUp']
    
    propdf = propdf[cols]
    print(propdf)
    
    propdf.to_excel('prop_bets.xlsx')
                    

            
            
    

