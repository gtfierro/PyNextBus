#!/usr/bin/env Python
'''
Flask API for nb.py
'''

import nb
from flask import Flask
app = Flask(__name__)

@app.route('/<stopstring>')
def get_predictions(stopstring):
  stopstring = stopstring.replace(':',' ')
  s = n.get_stop(stopstring)
  return str(n.get_prediction(s))

if __name__=="__main__":
  n = nb.NB('actransit')
  app.debug = True
  app.run()
