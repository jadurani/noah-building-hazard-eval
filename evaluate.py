#!/usr/bin/python

import json
import math
import requests
import sys


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

def evaluateBuilding(centroid, radius):
  URL = "https://api.mapbox.com/v4/upri-noah.ph_fh_100yr_tls,upri-noah.ph_ssh_ssa4_tls,upri-noah.ph_lh_lh1_tls,upri-noah.ph_lh_lh2_tls,upri-noah.ph_lh_lh3_tls/tilequery/" + str(centroid[0]) + "," + str(centroid[1]) + ".json?radius=" + str(radius) + "&limit=20&access_token=pk.eyJ1IjoiamFkdXJhbmkiLCJhIjoiY2tsZ245OGx3MHltbTJwcWwxbGpubjY1cyJ9.lqNLH1nne4ddBcXvWsP9YQ"
  response = requests.get(URL)
  features = response.json()['features']
  hazardValues = {
    'flood': 0,
    'landslide': 0,
    'stormSurge': 0,
  }

  for f in features:
    properties = f['properties']
    print(properties)
    if 'Var' in properties and hazardValues['flood'] < properties['Var']:
      hazardValues['flood'] = properties['Var']
    if 'HAZ' in properties and hazardValues['stormSurge'] < properties['HAZ']:
      hazardValues['stormSurge'] = properties['HAZ']
    if 'LH' in properties and hazardValues['landslide'] < properties['LH']:
      hazardValues['landslide'] = properties['LH']

  return hazardValues


evalObj = {
  'flood': {
    0: [],
    1: [],
    2: [],
    3: [],
  },
  'landslide': {
    0: [],
    1: [],
    2: [],
    3: [],
  },
  'stormSurge': {
    0: [],
    1: [],
    2: [],
    3: [],
  }
}

def groupToEvalObj(buildingName, hazardValues):
  for hazardName in hazardValues:
    hazardValue = hazardValues[hazardName]
    evalObj[hazardName][hazardValue].append(buildingName)


def processData(data):
  for i in data['features']:
    buildingName = i['properties']['name']

    # 1. Find centroid
    coordsList = i['geometry']['coordinates'][0][0]
    centroid = findCentroid(coordsList)
    print('centroid', centroid)

    # 2. Find the longest segment
    radius = findLongestSegment(coordsList, centroid)
    print(radius)

    # 3. Evaluate hazard susceptibility
    hazardValues = evaluateBuilding(centroid, radius)
    print(hazardValues)

    # 4. Group the list accoding to type and level
    groupToEvalObj(buildingName, hazardValues)
  print(json.dumps(evalObj, indent=2))

blueprintsFile = open('sample-file.json',)
data = json.load(blueprintsFile)
processData(data)
blueprintsFile.close()