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
* *really* basic web interface: just type ```python web.py``` and go to ```localhost:5000/stop I want predictions for```.
  Go ahead and leave the spaces in!

##Usage

In python interpreter

```
import nb
n = nb.NB('actransit') 
stop = n.get_stop('hearst arch') 
n.get_prediction(stop)
=> [('1', u'65'), ('13', u'52')]
```

