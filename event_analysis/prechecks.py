'''
Event prescout to identify past performance and things that are interesting to judges.

TODO: Stub out function flow
'''
import tbaUtils
import pandas as pd
from pprint import pprint
from icecream import ic
from datetime import date

YEAR = str(date.today().year)
TODAY = str(date.today())


def prescout_event(event, year=YEAR):
    raise NotImplementedError

    # TODO set filename for output
    # TODO get team list
    # TODO get team locations
    # TODO get team award/event history
    # TODO get award dictionary and output sequence list
    # TODO generate list of WFFAs
    # TODO create sorted dataframes for printing
    # TODO Normalize Award Names in Award History
    # TODO write output file including:
    # TODO Event location statistics
    # TODO WFFA List
    # TODO Team Name Location Current-season-events-by-week
    # TODO Current season awards by team
    # TODO Award count for current team members (restrict to 4 years including current year)
    # TODO Award count, all time


def getCCACandidate():
    raise NotImplementedError


def __Main__():
    print('1) Prescout Event\n2) Gather CCA candidate information\n')
    selection = input('Choose analysis type: ')
    if selection == 1:
        event = input('Enter event code i.e. ksla: ')
        getyear = input('Enter year to check (enter for current year)')
        if isdigit(getyear):
            prescout_event(event, getyear)
        else:
            prescout_event(event)
    elif selection == 2:
        getCCACandidate()
