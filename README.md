#PyNextBus

This is an attempt to provide a simple, human-accessible API for nextbus that doesn't involve the end-user having to parse XML or navigate drop-down menus on the nextbus.com website to find the information they need.

##Requirements
* requests (http://docs.python-requests.org/en/latest/index.html)
* fuzzywuzzy (https://github.com/seatgeek/fuzzywuzzy)
* flask (http://flask.pocoo.org/)

Included in Python:

* xml.etree
* os
* json

##Features
* indexing by stop (NextBus.com only indexes by the name of the line!)
* caching of the stop index
* fuzzy string matching, so instead of "Hearst Av. & Le Roy Av." you can just type "hearst leroy"
* really basic web API
  Go ahead and leave the spaces in!
* caching of user input strings...lessens the lookup time!

##Functions

####get_routes()
Returns list of available routes for the provided agency (defaults to 'actransit')

####get_stops(routes)
Returns a dict for all the routes provided as input. This is easily convertable to JSON.

```
{ 
  'full stop name':
  {
   'stopID': id number,
   'routes': [list, of, routes, for, this, stop]
  }
}
```

####get_stop(string)
Returns the (official) full stop name. Uses fuzzy string matching to find the closest match. Use the returned
full stop name to index into the ```stops``` dict (if you're using the interpreter).

####get_prediction(stop, maxList=3)
Returns a dict of the predictions for the given stop (returns the min of ```maxList``` and how many
predictions are available). Highest level keys assist in the ordering (0 is the closest bus, 1 is the next closest bus, etc).

```
{
  '0':
    {
      'route': name of route,
      'arrives': ETA in minutes
    }
  '1':
    ...
}
```


##Example

In python interpreter:

```
import nb
n = nb.NB('actransit') 
stop = n.get_stop('hearst arch') 
n.get_prediction(stop)
```

*or*

Run ```python app.py```

In web browser (or via command line):

* "/prediction/name of stop" >> top 3 predictions for bus arrivals at "name of stop"
* "/name/name of stop" >> returns the closest matching stop name for your input string
* "/stops/name of route" >> returns a list of stops for the route matching "name of route"
