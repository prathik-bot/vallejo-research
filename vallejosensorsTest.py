import requests

API_KEY = '9A211F43-55E7-11F0-81BE-42010A80001F'


latitude = 38.1041
longitude = -122.2560
radius_meters = 10000

url = 'https://api.purpleair.com/v1/sensors'

headers = {
    'X-API-Key': API_KEY
}

params = {
    'fields': 'sensor_index,name,latitude,longitude,pm2.5',
    'location_type': 0,  # outdoor sensors
    'max_age': 3600,     # only sensors updated in the last hour
    'nwlng': -122.3,     # bounding box west-longitude
    'nwlat': 38.15,      # bounding box north-latitude
    'selng': -122.2,     # bounding box east-longitude
    'selat': 38.05       # bounding box south-latitude
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("Found", len(data.get("data", [])), "sensors:")
    fields = data["fields"]
    for sensor in data["data"]:
        sensor_data = dict(zip(fields, sensor))
        print(sensor_data)
else:
    print("Error:", response.status_code, response.text)
