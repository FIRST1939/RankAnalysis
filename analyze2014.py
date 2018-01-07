# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 10:20:33 2018

2014 Scouting Rank Analysis Tools

Starting with 2014 because there ranking scores didn't include any ranking 
points other than for WLT.  More recent years with bonus RP for specific 
actions are going to be harder to model.
"""

from pprint import pprint
import pandas as pd
import tbaUtils as tba

pprint(tba.get_event_list(2014))