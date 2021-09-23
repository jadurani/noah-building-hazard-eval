#!/usr/bin/python

import json

f = open('sample-file.json',)

data = json.load(f)

for i in data['features']:
  print(i['properties']['name'])
  # print(i['geometry']['coordinates'])

f.close()