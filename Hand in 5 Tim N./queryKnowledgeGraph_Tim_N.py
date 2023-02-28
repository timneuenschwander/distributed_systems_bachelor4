import requests
import urllib.parse
from SPARQLWrapper import SPARQLWrapper, JSON


#definitions:
url_base = "https://graphdb.interactions.ics.unisg.ch/repositories/assignment5"
username = 'students'
password = 'assignment5isFun!'
file = (open("getThingsAffordances.rq", "r"))
queryString = file.read()

#executions:
sparql = SPARQLWrapper(url_base)
sparql.setQuery(queryString)
sparql.setCredentials(username, password)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)

#Objects
"""
8 Objectgs:
Airconditioner,
bathtub,
coffee machine,
diffuser,
standing lamp,
toaster,
vacuum cleaner,
watering can.
"""
#Property and Action Affordances
"""
1*Property Affardance
3*Action Affordance
"""

/var/folders/p4/qlfr3dj53bzc4mcslg32lr_h0000gn/T/TemporaryItems/NSIRD_screencaptureui_7r4Ds7/Screenshot 2021-07-01 at 11.29.12.png
