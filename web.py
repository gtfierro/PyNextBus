#!/usr/bin/env Python
'''
Flask API for nb.py
'''

import nb
import os
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/prediction/<stopstring>')
def get_predictions(stopstring):
  stopstring = stopstring.replace(':',' ')
  s = n.get_stop(stopstring)
  return jsonify(n.get_prediction(s))

@app.route('/name/<stopstring>')
def get_full_name(stopstring):
  stopstring = stopstring.replace(':',' ')
  s = n.get_stop(stopstring)
  return jsonify(s)

@app.route('/stops/<route>')
def get_stops_for_route(route):
  return jsonify(n.get_stops_for_route(route))

if __name__=="__main__":
  n = nb.NB('actransit')
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
