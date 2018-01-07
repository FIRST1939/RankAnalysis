# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 10:20:33 2018

2015 Scouting Rank Analysis Tools

Starting with 2015 because there ranking scores didn't include any ranking 
points other than for WLT.  More recent years with bonus RP for specific 
actions are going to be harder to model.  Can't do 2014 because component score
data isn't available on TBA.
"""

from pprint import pprint
import pandas as pd
import tbaUtils as tba

YEAR = 2015

def maketeamlist(event='mokc'):
    teamdf = pd.DataFrame(tba.get_event_teams(event,YEAR))
    
    print(teamdf)
    
    return(teamdf.team_number)    
    

def makematchlist(event='mokc'):
    '''
    This JSON response includes nested dictionaries, so it doesn't pandas
    directly well.  Going to deparse it a bit.
    '''
    matchlist = tba.get_event_matches(event,YEAR)
    
    pprint(matchlist[0:5])
    
