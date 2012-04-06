#PyNextBus

This is an attempt to provide a simple, human-accessible API for nextbus that doesn't involve the end-user having to parse XML or navigate drop-down menus on the nextbus.com website to find the information they need.

##Requirements
* requests (http://docs.python-requests.org/en/latest/index.html)
* fuzzywuzzy (https://github.com/seatgeek/fuzzywuzzy)

Included in Python:
* xml.etree
* os
* json

##Usage

In python interpreter
```python
import nb
n = nb.NB('actransit') #or shortname of another agency
stop = n.get_stop('hearst arch') #uses fuzzy string matching
n.get_prediction(stop)
=> [('1', u'65'), ('13', u'52')] #this means the 65 line is arriving in 1 minute
                                 #and the 52 line is arriving in 13 minutes
```

