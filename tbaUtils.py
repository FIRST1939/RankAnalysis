# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 23:12:28 2016

"""

import urllib.request
import json
from time import sleep
from datetime import date

URL = 'http://www.thebluealliance.com/api/v3/'

THISYEAR = date.today().year

'''
X-TBA-App-Id is required by the blue alliance api for tracking
Default User-Agent value causes 403 Forbidden so I pretend to be a browser.
'''
REQHEADERS = {'X-TBA-Auth-Key': 'noZ6Q6W3YhLxNHL7IQzCxTTDzSfCzeOPbcNN7lsRoUFyYbkfnoQXnFrGYM9Ecoeo',
              'User-Agent': 'Mozilla/5.0'}


def get_request(fullurl):
    request = urllib.request.Request(fullurl, headers=REQHEADERS)
    response = urllib.request.urlopen(request)
    jsonified = json.loads(response.read().decode("utf-8"))
    return jsonified


def get_team(team_num):
    '''
    @param team_num: int
    @return: dict containing basic team overview information

    {'address': None,
    'city': 'Kansas City',
    'country': 'USA',
    'gmaps_place_id': None,
    'gmaps_url': None,
    'key': 'frc1939',
    'lat': None,
    'lng': None,
    'location_name': None,
    'motto': None,
    'name': 'The Barstow School&THE BARSTOW SCHOOL',
    'nickname': 'THE KUHNIGITS',
    'postal_code': '64114',
    'rookie_year': 2006,
    'school_name': 'THE BARSTOW SCHOOL',
    'state_prov': 'Missouri',
    'team_number': 1939,
    'website': 'https://www.frcteam1939.com'}
    '''
    fullurl = URL + 'team/frc' + str(team_num)
    result = get_request(fullurl)
    return result


def get_team_bots(team_num):
    '''
    @param team_num:
    @return: list of dicts containing key ('frc1939_2015'), robot name, team_key, and year
    '''
    fullurl = URL + 'team/frc' + str(team_num) + '/robots'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_team_history(team_num):
    '''

    @param team_num:
    @return: list of eventcodes
    '''
    fullurl = URL + 'team/frc' + str(team_num) + '/events/keys'
    print(fullurl)
    result = get_request(fullurl)
    sleep(0.25)
    return result


def get_award_history(team_num):
    '''
    @param team_num:
    @return: list of award dicts each containing award_type, event key, name, recipient_list, and year

     {'award_type': 29,
     'event_key': '2022mokc',
     'name': 'Innovation in Control Award',
     'recipient_list': [{'awardee': None, 'team_key': 'frc1939'}],
     'year': 2022},
    {'award_type': 3,
     'event_key': '2022mokc',
     'name': 'Woodie Flowers Finalist Award',
     'recipient_list': [{'awardee': 'Brandon Huizenga', 'team_key': 'frc1939'}],
     'year': 2022}]
    '''
    fullurl = URL + 'team/frc' + str(team_num) + '/awards'
    print(fullurl)
    result = get_request(fullurl)
    sleep(0.25)
    return result


def get_team_year(team_num, year):
    '''

    @param team_num:
    @param year:
    @return: list of event dicts each containing location information, eventdates, event type (code and string),
             time zone, week number, webcast locations, and host website.
    '''
    fullurl = URL + 'team/frc' + str(team_num) + '/events/' + str(year)
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_list(year=THISYEAR):
    '''

    @param year:
    @return: list of event dicts each containing location information, eventdates, event type (code and string),
             time zone, week number, webcast locations, and host website.
    '''
    fullurl = URL + 'events/' + str(year)
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_year_keys(year=THISYEAR):
    '''

    @param year:
    @return:list of event keys
    '''
    fullurl = URL + 'events/' + str(year) + '/keys'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_teams(event, year=THISYEAR):
    '''

    @param event:
    @param year:
    @return: schema
         [
          {
            "key": "string",
            "team_number": 0,
            "nickname": "string",
            "name": "string",
            "school_name": "string",
            "city": "string",
            "state_prov": "string",
            "country": "string",
            "address": "string",
            "postal_code": "string",
            "gmaps_place_id": "string",
            "gmaps_url": "string",
            "lat": 0,
            "lng": 0,
            "location_name": "string",
            "website": "string",
            "rookie_year": 0,
            "motto": "string",
            "home_championship": {}
          }
        ]
    '''
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/teams'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_teams_simple(event, year=THISYEAR):
    '''

    @param event:
    @param year:
    @return: schema
            [
              {
                "key": "string",
                "team_number": 0,
                "nickname": "string",
                "name": "string",
                "city": "string",
                "state_prov": "string",
                "country": "string"
              }
            ]
    '''
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/teams/simple'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_matches(event, year=THISYEAR):
    '''

    @param event:
    @param year:
    @return: schema
    [
      {
        "key": "string",
        "comp_level": "qm",
        "set_number": 0,
        "match_number": 0,
        "alliances": {
          "red": {
            "score": 0,
            "team_keys": [
              "string"
            ],
            "surrogate_team_keys": [
              "string"
            ],
            "dq_team_keys": [
              "string"
            ]
          },
          "blue": {
            "score": 0,
            "team_keys": [
              "string"
            ],
            "surrogate_team_keys": [
              "string"
            ],
            "dq_team_keys": [
              "string"
            ]
          }
        },
        "winning_alliance": "red",
        "event_key": "string",
        "time": 0,
        "actual_time": 0,
        "predicted_time": 0,
        "post_result_time": 0,
        "score_breakdown": {},
        "videos": [
          {
            "type": "string",
            "key": "string"
          }
        ]
      }
    ]
    '''
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/matches'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_one_match(key):
    fullurl = URL + 'match/' + key
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_insights(event, year=THISYEAR):
    # OPR, DPR, CCWM
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/insights'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_awards(event, year=THISYEAR):
    '''

    @param event:
    @param year:
    @return:
    [
      {
        "name": "string",
        "award_type": 0,
        "event_key": "string",
        "recipient_list": [
          {
            "team_key": "string",
            "awardee": "string"
          }
        ],
        "year": 0
      }
    ]
    '''
    # www.thebluealliance.com/api/v2/event/<event key>/awards
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/awards'
    print(fullurl)
    result = get_request(fullurl)
    return result


def get_event_rankings(event, year=THISYEAR):
    '''

    @param event:
    @param year:
    @return:
    {'extra_stats_info': [{'name': 'Total Ranking Points', 'precision': 0}],
     'rankings': [{'dq': 0,
                   'extra_stats': [36],
                   'matches_played': 12,
                   'qual_average': None,
                   'rank': 1,
                   'record': {'losses': 2, 'ties': 0, 'wins': 10},
                   'sort_orders': [3.0, 69.08, 19.08, 21.66, 0.0, 0.0],
                   'team_key': 'frc1825'},...],
                   'sort_order_info': [{'name': 'Ranking Score', 'precision': 2},
                                        {'name': 'Avg Match', 'precision': 2},
                                        {'name': 'Avg Hangar', 'precision': 2},
                                        {'name': 'Avg Taxi + Auto Cargo', 'precision': 2}]}
    '''
    # OPR, DPR, CCWM
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/rankings'
    print(fullurl)
    result = get_request(fullurl)
    return result

def get_event_oprs(event, year=THISYEAR):
    event_key = str(year) + event
    fullurl = URL + 'event/' + event_key + '/oprs'
    print(fullurl)
    result = get_request(fullurl)
    return result
    
def make_eventweekmtx(year=THISYEAR):
    eventlist = get_event_list(year)

    matrix = {}
    for event in eventlist:
        matrix[event['event_code']] = event['week']

    weeklist = {}
    for event in matrix:
        if matrix[event] is None:
            week = 0
        else:
            week = matrix[event] + 1

        if week not in weeklist:
            weeklist[week] = []

        weeklist[week].append(event)

    return matrix, weeklist
