import random
import json
from datetime import datetime, timedelta

def generate_mock_sensors(num_sensors=5, center_lat=38.1, center_lng=-122.25, radius=0.02):
    """
    Generate mock sensor data around a center coordinate with random PM2.5 values.
    Args:
        num_sensors (int): Number of mock sensors to generate
        center_lat (float): Center latitude
        center_lng (float): Center longitude
        radius (float): Max deviation from center for lat/lng
    Returns:
        List of dicts with sensor info
    """
    sensors = []
    for i in range(num_sensors):
        lat = center_lat + random.uniform(-radius, radius)
        lng = center_lng + random.uniform(-radius, radius)
        pm25 = round(random.uniform(0, 50), 1)  # PM2.5 value between 0 and 50
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
