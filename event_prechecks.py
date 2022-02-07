# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 21:58:47 2018


Event prescout with emphasis on past performance and interesting judging
things.

TODO: Move master keys and sorted award list to an external file and import
TODO: Replace diagnostic print statements with ic
TODO: Refactor everything


"""
import tbaUtils
import pandas as pd
from pprint import pprint
from icecream import ic
from datetime import date

YEAR = str(date.today().year)

MASTERKEYS = {0: 'RCA/CCA', 1: 'Winner', 2: 'Finalist', 3: 'WFFA/WFA', 4: 'DLFA',
              5: 'Volunteer of the Year', 9: 'REI/EI', 10: 'Rookie All-Star',
              11: 'Gracious Professionalism', 12: 'Coopertition', 13: 'Judges',
              14: 'Highest Rookie Seed', 15: 'Rookie Inspiration', 16: 'GM Industrial Design',
              17: 'Quality', 18: 'Safety', 19: 'Sportsmanship', 20: 'Creativity',
              21: 'Excellence in Engineering', 22: 'Entrepreneurship',
              23: 'Autodesk Excellence in Design', 24: 'Excellence in Design Award sponsored by Autodesk (3D CAD)',
              25: 'Championship - Excellence in Design Award sponsored by Autodesk (Animation)',
              26: 'Delphi Driving Tomorrows Technology',
              27: 'Imagery', 28: 'Media and Technology Award sponsored by Comcast',
              29: 'Innovation in Control', 30: 'Team Spirit',
              31: 'Website', 32: 'Autodesk Visualization', 33: 'Autodesk Inventor Award',
              34: 'FIRST Future Innovator', 38: 'Leadership in Controls',
              39: '#1 Seed', 40: 'Incredible Play Award', 41: "People's Choice Animation Award",
              42: 'Autodesk Rising Star Visualization Award', 43: 'Best Offensive Round',
              44: 'Best Play of the Day Award', 45: 'Featherweight in the Finals',
              46: 'Most Photogenic', 47: 'Outstanding Defense',
              48: 'Delphi "Power to Simplify" Award', 49: 'Against All Odds Award',
              51: 'Chairmans Award Finalist', 53: 'Honorable Mention-Technical Execution',
              54: 'Autodesk Award for Realization', 56: 'Autodesk Design your Future Award',
              57: 'Autodesk Design your Future Award Honorable Mentions:',
              58: 'Autodesk Special Recognition for Distinctive Work in the Area of Character Animation:',
              59: 'High Score', 60: 'Teacher Pioneer Award',
              61: 'Best Craftsmanship/Ultimate Keeper Award', 62: 'Best Defensive Match',
              64: 'Programming',
              65: 'Professionalism Award', 67: 'Most Improved Team', 68: 'Wildcard',
              69: "Chairman's Award Finalist", 70: 'Most Improved Robot',
              71: 'Autonomous Award sponsored by Ford'}

AWDSEQ = ['Chairman\'s Award Finalist', 'RCA/CCA', 'REI/EI', 'Winner', 'Finalist',
          'Wildcard', 'Excellence in Engineering', 'GM Industrial Design',
          'Innovation in Control', 'Quality', 'Creativity',
          'Autonomous Award sponsored by Ford', 'Entrepreneurship',
          'Gracious Professionalism', 'Team Spirit', 'Imagery', 'Judges', 'Safety',
          'Rookie All-Star', 'Rookie Inspiration', 'Highest Rookie Seed',
          'WFFA/WFA', 'DLFA', 'Volunteer of the Year', 'FIRST Future Innovator',
          'Coopertition', 'Sportsmanship', 'Professionalism Award',
          'Delphi Driving Tomorrows Technology',
          'Website', 'Leadership in Controls', '#1 Seed', 'High Score',
          'Incredible Play Award', 'Against All Odds Award',
          'Best Play of the Day Award', 'Best Offensive Round',
          'Best Defensive Match', 'Best Craftsmanship/Ultimate Keeper Award'
                                  'Outstanding Defense', 'Featherweight in the Finals',
          'Most Improved Team', 'Most Photogenic',
          'Programming', 'Most Improved Robot',
          'Media and Technology Award sponsored by Comcast',
          'Teacher Pioneer Award',
          'Delphi "Power to Simplify" Award',
          'Autodesk Excellence in Design',
          'Excellence in Design Award sponsored by Autodesk (3D CAD)',
          'Autodesk Rising Star Visualization Award',
          'Autodesk Visualization', 'Autodesk Inventor Award',
          'Autodesk Award for Realization',
          'Autodesk Design your Future Award',
          'Autodesk Design your Future Award Honorable Mentions:']


def maketeamlist(event):
    '''
    Pull big list, strip out the interesting parts, and return as a dict.
    '''

    raw = tbaUtils.get_event_teams(event)

    result = {}

    for entry in raw:
        teamnum = entry['team_number']
        name = entry['nickname']
        if entry['country'] == 'USA':
            state = entry['state_prov']
        else:
            state = entry['country']
        school = entry['name'].split('&')[-1]

        # print(teamnum, name, state, school)
        result[teamnum] = {'name': name, 'state': state, 'school': school}

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
        allevents[team] = tbaUtils.get_team_history(team)

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
        allawds[team] = tbaUtils.get_award_history(team)

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

    junk, weeklist = tbaUtils.make_eventweekmtx()

    result = {}

    for team in teamdict:
        result[team] = {}
        for week in weeklist:
            for event in teamdict[team]:
                if event[4:] in weeklist[week]:
                    result[team][week] = event

    # print('\nTeam Week Matrix?')

    return pd.DataFrame(result).transpose().fillna(value='')


def wrestleawds(awdmatrix, awdkeys):
    masterkeys = MASTERKEYS
    # pprint(masterkeys)

    print()
    for i in awdkeys:
        if i not in masterkeys:
            print('Missing Award:', i, awdkeys[i])
            masterkeys[i] = awdkeys[i][0]

    # print('\nMaster Keys')
    # pprint(masterkeys)
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
    # print('All')
    # pprint(allyears)

    currentyeardf = pd.DataFrame(currentyear)
    allyearsdf = pd.DataFrame(allyears)

    # resequence this mess
    actuals = currentyeardf.columns.tolist()
    possibles = AWDSEQ.copy()

    for item in AWDSEQ:
        if item not in actuals:
            possibles.remove(item)

    currentyeardf = currentyeardf[possibles]

    actuals2 = allyearsdf.columns.tolist()
    possibles2 = AWDSEQ.copy()
    for item in AWDSEQ:
        if item not in actuals2:
            possibles2.remove(item)
    allyearsdf = allyearsdf[possibles2]

    return currentyeardf, allyearsdf


def awdcounter(awdmtxdf):
    '''
    Take the award matrix and do a count by team by award.
    Also do a count by team by award for the most recent 4 years (i.e. the
    window in which the same student might have been on the team Freshman to 
    Senior)
    '''
    tgtyears = [YEAR, str(int(YEAR) - 1), str(int(YEAR) - 2), str(int(YEAR) - 3)]

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

    # TODO resequence this mess
    actuals = past4df.columns.tolist()
    possibles = AWDSEQ.copy()
    for item in AWDSEQ:
        if item not in actuals:
            possibles.remove(item)
    past4df = past4df[possibles]

    actuals = allcntdf.columns.tolist()
    possibles = AWDSEQ.copy()
    for item in AWDSEQ:
        if item not in actuals:
            possibles.remove(item)
    allcntdf = allcntdf[possibles]

    return past4df, allcntdf


def wffanator(allawds):
    '''
    Take the all awards list, find the WFFA entries, and print/return a list
    of the recipients
    '''
    wffas = []

    for team in allawds:
        for award in allawds[team]:

            if award['award_type'] == 3:
                # print(award['event_key'], award['recipient_list'][0]['awardee'], team)
                if award['event_key'] == '2009co':
                    wffas.append([award['event_key'], 'Kevin Schimpf', team])
                else:
                    wffas.append([award['event_key'], award['recipient_list'][0]['awardee'], team])

    wffas.sort()
    print('\nWFFA count is:', len(wffas))
    ic(wffas)
    return wffas


def prescout_event(event):
    '''
    Combine commands together, write to a file.
    '''

    xlfile = 'Prescout-' + YEAR + '-' + event + '.xlsx'
    scratchfile = 'Prescout-' + YEAR + '-' + event + '-notes.txt'

    teamlist = maketeamlist(event)
    ic(teamlist)
    locations = locstats(teamlist)
    current, fullhist = eventmtx(teamlist)
    allawds, awdkeys, awdmx = awdmtx(teamlist)

    wffas = wffanator(allawds)
    '''    
    with open(scratchfile, 'w') as file:
        file.write('Team List\n')
        print(teamlist)
        file.write(str(teamlist))
        file.write('\n\nLocation Stats\n')
        file.write(str(locations))
        file.write('\n\nCurrent Events\n')
        file.write(str(current))
        file.write('\n\nAward List\n')
        file.write(str(allawds))
        file.write('\n\nAward Keys\n')
        file.write(str(awdkeys))
    '''
    # print('\nKeys')
    # pprint(awdkeys)

    print('Team locations:')
    pprint(locations)

    curmtx = teamweekmtx(current)
    teamdf = pd.DataFrame(teamlist).transpose()
    #covidRkdf = covidrookie(teamdf)
    #ic(covidRkdf)

    eventteamdf = pd.merge(teamdf, curmtx, left_index=True, right_index=True)
    # pprint(awdmx)

    curawddf, awdmtxdf = wrestleawds(awdmx, awdkeys)

    past4cntdf, allawdcntdf = awdcounter(awdmtxdf)

    # print(awdmtxdf.head())

    with pd.ExcelWriter(xlfile) as writer:
        eventteamdf.to_excel(writer, 'Team Events')
        curawddf.to_excel(writer, 'Current Awards')
        awdmtxdf.to_excel(writer, 'Full Award Matrix')
        past4cntdf.to_excel(writer, 'Awd Count Current Team')
        allawdcntdf.to_excel(writer, 'All Award Count')


def makeEventList(year=YEAR):
    '''
    List event code, event name, competition level
    '''

    eventlist = tbaUtils.get_event_list(year)

    result = []

    for event in eventlist:
        key = event['key']
        name = event['name']
        level = event['event_type_string']

        result.append([key, level])

    return result


def covidrookie(teamdf):
    '''
    Parameters:
        teamdf: pdDataframe containing Team, Nickname, State

    Returns:
        coviddf: pd.Dataframe containing Team, 2020Events

        2020Events is a boolean indicating whether the team attended a 2020 event that was not cancelled.
    TODO:This thing doesn't work at all yet
    '''
    good2020 = ['2020arli', '2020award', '2020bcvi', '2020cadm', '2020cala', '2020caln', '2020cass', '2020cmpmi',
                '2020cmptx', '2020ctnct', '2020ctwat', '2020facc', '2020gadal', '2020gagai', '2020gzrs', '2020ilch',
                '2020inblo', '2020isde1', '2020isde2', '2020mabri', '2020mdbet', '2020mijac', '2020mike2', '2020miket',
                '2020mikng', '2020mimcc', '2020mimil', '2020misjo', '2020misou', '2020mitvc', '2020mndu', '2020mndu2',
                '2020mnwcw', '2020mokc', '2020mxmo', '2020ncpem', '2020ncwak', '2020ndgf', '2020nhgrs', '2020nyrra',
                '2020ohmv', '2020onbar', '2020onosh', '2020onto3', '2020orore', '2020pahat', '2020qcsh', '2020scmb',
                '2020srrc', '2020taiw', '2020taiw2', '2020tuis', '2020tuis2', '2020txcha', '2020txdel', '2020txdri',
                '2020txgre', '2020txpla', '2020utwv', '2020vagle', '2020vahay', '2020wasno', '2020waspo', '2020week0',
                '2020wiss']
    ic(teamdf.head())
    ic(tbaUtils.get_team_history('1706'))

    teamdf[events] = tbaUtils.get_team_history(teamdf[team_num])
    ic(teamdf.head())


def eventLeveler(eventlist):
    '''
    Take a list of eventcodes and return them by level [CMP, REG, DCMP, DIS]
    '''
    result = [[], [], [], []]

    cmpdivs = ['carv', 'gal', 'hop', 'new', 'roe', 'tur',
               'arc', 'cars', 'cur', 'dal', 'dar', 'tes',
               'cmp', 'cmptx', 'cmpmo', 'cmpmi']

    mi = ['dt', 'dt1', 'gg', 'grl', 'gt', 'mi', 'oc', 'oc1', 'swm', 'wc', 'ww']

    for event in eventlist:
        shortclli = event[4:]
        el = len(shortclli)
        year = int(event[:4])

        print(event, shortclli, el)

        if shortclli in cmpdivs:
            result[0].append(event)
        elif year > 2012:  # Naming convention standardized
            if el == 5:
                if shortclli[2:] == 'cmp':
                    result[2].append(event)
                elif shortclli[-1].isdigit():
                    result[1].append(event)
                else:
                    result[3].append(event)
            elif el == 4:
                result[1].append(event)
        elif year > 2008:  # Michigan has districts, still on oldformat names
            if shortclli == 'gl':  # micmp
                result[2].append(event)
            elif shortclli in mi:
                result[3].append(event)
            else:
                result[1].append(event)
        else:  # No districts exist, and we've already ruled out CMP divisions
            result[1].append(event)

    return result


def cmpscout(cmp):
    if cmp == 'hou':
        divisions = ['carv', 'gal', 'hop', 'new', 'roe', 'tur']
    else:
        divisions = ['arc', 'cars', 'cur', 'dal', 'dar', 'tes']


def matchlistformo(event, year=YEAR):
    matchdictlist = tbaUtils.get_event_matches(event, year)

    qualteams = []

    for match in matchdictlist:
        if match['comp_level'] == 'qm':
            matchnum = match['match_number']
            blue = match['alliances']['blue']['team_keys']
            red = match['alliances']['red']['team_keys']

            for i in [0, 1, 2]:
                j = str(i + 1)
                qualteams.append([matchnum, 'Red' + j, red[i]])
                qualteams.append([matchnum, 'Blue' + j, blue[i]])

    qualdf = pd.DataFrame(qualteams, columns=['Match', 'Position', 'Team'])

    qualdf.to_excel('MO Matchlist - ' + event + '.xlsx', index=False)


#thisevent = input('Enter event to check: ')
#assert thisevent.isalnum()
#prescout_event(thisevent)