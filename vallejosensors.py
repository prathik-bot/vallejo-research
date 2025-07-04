# Version 1
import requests
import folium

API_KEY = '9A211F43-55E7-11F0-81BE-42010A80001F'

# Bounding box around Vallejo, CA
# parameters for the API request
params = {
    'fields': 'sensor_index,name,latitude,longitude,pm2.5',
    'location_type': 0,  # makes sure its outdoors
    'max_age': 3600,  # active in the last hour
    'nwlng': -122.3,
    'nwlat': 38.15,
    'selng': -122.2,
    'selat': 38.05
}

headers = {
    'X-API-Key': API_KEY
}

# sends a get request to purpleair's api w/ paramters and headers
url = 'https://api.purpleair.com/v1/sensors'
response = requests.get(url, headers=headers, params=params)

# Initialize map centered on Vallejo
map_center = [38.1041, -122.2560]
sensor_map = folium.Map(location=map_center, zoom_start=12)


# Decides what color to use based on PM2.5 value
def get_color(pm):
    try:
        pm = float(pm)
        if pm <= 12:
            return 'green'
        elif pm <= 35.4:
            return 'orange'
        else:
            return 'red'
    except:
        return 'gray'


if response.status_code == 200: #checks if the api request was successful
    data = response.json()
    fields = data["fields"]
    # prints
    print(f"Found {len(data['data'])} sensors")

    for sensor in data["data"]:
        # creates dictionary w data from each sensor
        sensor_data = dict(zip(fields, sensor))

        # takes values from the sensor dictionary
        name = sensor_data.get("name", "Unnamed Sensor")
        lat = sensor_data.get("latitude")
        lng = sensor_data.get("longitude")
        pm25 = sensor_data.get("pm2.5", "N/A")

        popup = f"<b>{name}</b><br>PM2.5: {pm25} µg/m³"
        color = get_color(pm25) #fcn defined earlier

        folium.Marker(
            location=[lat, lng],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(sensor_map)

    # Save map to HTML
    sensor_map.save("vallejo_pm25_map.html")
    print("Map saved to vallejo_pm25_map.html")
else:
    print("Error fetching data:", response.status_code, response.text)
