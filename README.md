# NOAH Building Footprint Evaluator

## Given

- A geojson file containing multipolygons that plot building footprints.
- [Mapbox Tilequery API](https://docs.mapbox.com/api/maps/tilequery/)
  - Given a latitude-longitude pair, a buffer and a tileset(s) uploaded in mapbox, the tilequery API evaluates the intersection of the given.
- NOAH hazard maps within the Philippines for floods, storm surges, landlides, debris flow and alluvial fan, and unstable slopes

## Output

- The list of buildings grouped according to hazard level for each hazard type, e.g.

**Flood: 100-year**
- High (3)
  - Araneta Coliseum
  - SM North EDSA
  - Capitol Medical Center
- Medium (1)
  - UP Diliman
- Low (2)
  - QC Memorial Shrine
  - Farmer's Plaza

## Methodology

1. Find the centroid of each polygon. This will serve as the latitude-longitude pair that we'll supply in the tilequery API
2. Find the longest segment from the centroid to any of the vertices (coordinates). This will serve as the buffer that we'll supply in the tilequery API.
3. Evaluate the hazard susceptibility of each building given the values in (1), (2), and the combined list of tilesets currently uploaded in the official UPRI Mapbox account. Only use the maximum of each
4. Group the list according to type and level.



## Sample Call

https://api.mapbox.com/v4/upri-noah.ph_fh_100yr_tls,upri-noah.ph_ssh_ssa4_tls,upri-noah.ph_lh_lh1_tls,upri-noah.ph_lh_lh2_tls,upri-noah.ph_lh_lh3_tls/tilequery/124.9992568778667,10.861302203625186.json?radius=50&limit=20&access_token={access_token}

- Note: supply your own mapbox account's access token

## Sample Output

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 168738011794748,
      "geometry": {
        "type": "Point",
        "coordinates": [124.9992568778667, 10.861302203625186]
      },
      "properties": {
        "Var": 2,
        "tilequery": {
          "distance": 0,
          "geometry": "polygon",
          "layer": "PH080000000_FH_100yr"
        }
      }
    },
    {
      "type": "Feature",
      "id": 3373746208329549,
      "geometry": {
        "type": "Point",
        "coordinates": [124.9992568778667, 10.861302203625186]
      },
      "properties": {
        "HAZ": 3,
        "tilequery": {
          "distance": 0,
          "geometry": "polygon",
          "layer": "PH080000000_SSH_ssa4"
        }
      }
    }
  ]
}
```
