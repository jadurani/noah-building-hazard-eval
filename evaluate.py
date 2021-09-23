#!/usr/bin/python

import json
import math

f = open('sample-file.json',)

data = json.load(f)

def findCentroid(coordsList):
  aveLng = sum([x[0] for x in coordsList]) / len(coordsList)
  aveLat = sum([y[1] for y in coordsList]) / len(coordsList)
  return [aveLng, aveLat]



def computeDistanceBetweenPoints(x1, x2, y1, y2):
  x = (x2 - x1)**2
  y = (y2 - y1)**2
  return math.sqrt(x + y)

def findLongestSegment(coordsList, centroid):
  distances = [computeDistanceBetweenPoints(coordsPair[0], centroid[0], coordsPair[1], centroid[1]) for coordsPair in coordsList]
  return max(distances) * 100000


for i in data['features']:
  print(i['properties']['name'])
  # 1. Find centroid
  coordsList = i['geometry']['coordinates'][0][0]
  centroid = findCentroid(coordsList)
  print('centroid', centroid)
  # 2. Find the longest segment
  radius = findLongestSegment(coordsList, centroid)
  print(radius)
  # 3. Evaluate hazard susceptibility
  # 4. Group the list accoding to type and level


  # print(i['geometry']['coordinates'])

f.close()