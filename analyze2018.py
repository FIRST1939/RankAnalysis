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
    

    
    
qual_model()
