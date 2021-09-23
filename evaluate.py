#!/usr/bin/python

import json
from math import radians, cos, sin, asin, sqrt
import requests


def findCentroid(coordsList):
  aveLng = sum([x[0] for x in coordsList]) / len(coordsList)
  aveLat = sum([y[1] for y in coordsList]) / len(coordsList)
  return [aveLng, aveLat]

def computeDistanceBetweenPoints(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    resultInKM = (c * r)
    resultInMeters = resultInKM * 1000
    return resultInMeters


def findLongestSegment(coordsList, centroid):
  distances = [computeDistanceBetweenPoints(coordsPair[0], centroid[0], coordsPair[1], centroid[1]) for coordsPair in coordsList]
  return max(distances)

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

hazardNames = {
  'flood': 'Flood',
  'landslide': 'Landslide',
  'stormSurge': 'Storm Surge',
}

hazardLevelName = {
  0: 'Little to none',
  1: 'Low',
  2: 'Medium',
  3: 'High'
}

def groupToEvalObj(buildingName, hazardValues):
  for hazardName in hazardValues:
    hazardValue = hazardValues[hazardName]
    evalObj[hazardName][hazardValue].append(buildingName)

def printEvalObjToList():
  outputFile = open("output.txt", 'w')

  for hazardName in evalObj:
    outputFile.write('- ' + hazardNames[hazardName] + ':')
    outputFile.write('\n')
    for hazardLevel in evalObj[hazardName]:
      buildingCount = len(evalObj[hazardName][hazardLevel])
      outputFile.write('  - ' + hazardLevelName[hazardLevel] + ' (' +  str(buildingCount) + '):')
      outputFile.write('\n')
      if buildingCount == 0:
        outputFile.write('    - (None)')
        outputFile.write('\n')
      for buildingName in evalObj[hazardName][hazardLevel]:
        outputFile.write('    - ' + buildingName)
        outputFile.write('\n')

  outputFile.close()


def processData(data):
  print('Evaluating ' + str(len(data)) + ' buildings in Quezon City...')
  for index, feature in enumerate(data['features']):
    buildingName = feature['properties']['name']

    if index % 1000 == 0:
      print(index,buildingName)

    # 1. Find centroid
    coordsList = feature['geometry']['coordinates'][0][0]
    centroid = findCentroid(coordsList)
    # print('centroid', centroid)

    # 2. Find the longest segment
    radius = findLongestSegment(coordsList, centroid)
    # print(radius)

    # 3. Evaluate hazard susceptibility
    hazardValues = evaluateBuilding(centroid, radius)
    # print(hazardValues)

    # 4. Group the list accoding to type and level
    groupToEvalObj(buildingName, hazardValues)

  printEvalObjToList()


blueprintsFile = open('sample-file.json',)
data = json.load(blueprintsFile)
processData(data)
blueprintsFile.close()