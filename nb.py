#!/usr/bin/env Python
'''
Library for parsing nextbus's public XML feed
Eventually I plan to create this as an API using flask
'''

from xml.etree import ElementTree as et
import requests, os, json
from fuzzywuzzy import process

class NB():
  '''
  handles all API calls for a given agency
  '''

  def __init__(self, agency, force_reload = False):
    '''
    checks to see if a file called [.agency] exists. If it does, then we load
    data from that file *unless* force_reload is specified as True. If force_reload is True
    or if we don't find [.agency], then we load the data from the nextbus api
    '''
    load = False if force_reload else os.path.exists("."+agency)
    if load:
      #load from JSON file
      with open("."+agency) as f:
        _jsonfile = json.loads(f.read())
      pass
    self.agency = agency
    self.SOURCE_URL = _jsonfile['SOURCE_URL'] if load else 'http://webservices.nextbus.com/service/publicXMLFeed?a=actransit'
    self.routes = _jsonfile['routes'] if load else self.get_routes()
    self.stops = _jsonfile['stops'] if load else self.get_stops(self.routes)
    _jsonfile = ['SOURCE_URL','routes','stops']
    if not load:
      with open("."+agency, 'w') as f:
        d = {}
        for key in _jsonfile:
          d[key] = getattr(self,key)
        f.write(json.dumps(d))

  def get_stop(self, string):
    '''
    returns the closest matching stop from the input string.
    We query from a list of stops we know exist
    '''
    #get significant words out of the stop names by eliminating
    # st, av, blvd, &, dr
    stop_names = map(lambda stop:
               (' '+stop+' ').lower().replace(' st ',' ')
                                    .replace(' av ',' ')
                                    .replace(' blvd ',' ')
                                    .replace(' & ',' ')
                                    .replace(' dr ',' ').strip()
               , self.stops.keys()
                    )
    match = process.extractOne(string, stop_names)
    #stop name
    return self.stops.keys()[stop_names.index(match[0])]
    
  def get_routes(self):
    '''
    Returns a list of all routes for the agency
    '''
    routes = []
    ROUTE_LIST_URL = self.SOURCE_URL+'&command=routeList'
    #get html
    html = requests.get(ROUTE_LIST_URL).text
    #get XML tree structure
    xml = et.XML(html)
    for child in xml.getchildren():
      routes.append(child.get('title'))
    return routes

  def get_stops(self, routes):
    '''
    Return dict of all stops for all [routes] of format:
    {
     'stop name': {'stopID': id number, 'routes':list of routes for this stop}
     ...
    }
    '''
    STOP_LIST_URL = self.SOURCE_URL+"&command=routeConfig&r="
    stop_dict = {}
    for route in self.routes:
      #route is a string e.g. 'B'
      html = requests.get(STOP_LIST_URL+route).text
      #get XML tree structure
      xml = et.XML(html)
      #get list of stops
      stops = [child for child in xml.getchildren()[0].getchildren() if child.tag == 'stop']
      for stop in stops:
        stopName = stop.get('title')
        stopID = stop.get('stopId')
        if stopName not in stop_dict.keys():
          stop_dict[stopName] = {'stopID':stopID, 'routes': [route]} 
        else:
          stop_dict[stopName]['routes'].append(route)
    return stop_dict

  def get_prediction(self, stop, maxList=3):
    '''
    Input the *full* name of the stop, gives sorted list of arriving buses (defaults to top 3)
    '''
    stopID = self.stops[stop]['stopID']
    PREDICTION_URL = self.SOURCE_URL+"&command=predictions&stopId="+stopID+"&r="
    predictions = []
    for route in self.stops[stop]['routes']:
      html = requests.get(PREDICTION_URL+route).text
      xml = et.XML(html).getchildren()[0].getchildren()[0]
      predictions_route = xml.getchildren()
      for p in predictions_route:
        predictions.append( (p.get('minutes'), route) )
    #sort by minutes
    sorted_predictions = sorted(predictions, key = lambda p: p[0] )
    return sorted_predictions[:min(maxList, len(sorted_predictions))]
