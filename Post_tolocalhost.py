# -*- coding: utf-8 -*-
# coding=utf8
"""
Created on Thu May 17 03:18:32 2018

@author: Homepc
"""

import requests
import json
import sys

url = "http://127.0.0.1:5001/add_record"
payload = {"company": "ENI",
           "site": "Kværner", 
           "date":"April 2017", 
           "model": "Contractor", 
           "place": "Crane", 
           "activity": "Lifting",
           "event_type":"Near miss", 
           "incident_classification":"Unsåfe act", 
           "incident_description":"Unsafe act", 
           "remidial_actions": "Training", 
           "reoccurance_potential":"High"}


headers = {"Content-Type": "application/json;charset=utf-8",
           "accept-encoding": "gzip",
           'Accept': 'text/plain'}

post = requests.post(url, json=(payload), headers=headers)

#post = requests.post(url, data=json.dumps(payload), headers=headers)

