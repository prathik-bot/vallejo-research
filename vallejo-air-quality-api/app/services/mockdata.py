import random
import json
from datetime import datetime, timedelta

# Define a few different "neighborhood" centers in Vallejo
centers = [
    (38.1025, -122.2561),  # Downtown
    (38.1071, -122.2495),  # Vallejo High
    (38.1391, -122.2356),  # Discovery Kingdom
    (38.0843, -122.2157),  # Glen Cove
    (38.1029, -122.2675),  # Ferry Terminal
]

def generate_mock_sensors(num_sensors=10, radius=0.01):
    sensors = []
    for i in range(num_sensors):
        center_lat, center_lng = random.choice(centers)  # randomly choose a base location
        lat = center_lat + random.uniform(-radius, radius)
        lng = center_lng + random.uniform(-radius, radius)
        pm25 = round(random.uniform(0, 50), 1)  # PM2.5 value
        sensors.append({
            "sensor_id": 1000 + i,
            "name": f"Mock Sensor {i+1}",
            "latitude": lat,
            "longitude": lng,
            "pm2_5": pm25,
            "last_seen": (datetime.utcnow() - timedelta(minutes=random.randint(0, 60))).isoformat() + "Z"
        })
    return sensors

if __name__ == "__main__":
    mock_data = generate_mock_sensors()
    print(json.dumps(mock_data, indent=2))
