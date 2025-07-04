from flask import Blueprint, jsonify
from app.services.purpleair import PurpleAirService
from datetime import datetime, timedelta
import random

sensors_bp = Blueprint('sensors', __name__)
service = PurpleAirService()

@sensors_bp.route('/sensors')
def get_sensors():
    data = service.get_sensors_in_area(
        center_lat=38.1041,
        center_lng=-122.2560,
        radius_km=5
    )
    return jsonify(data)

def generate_mock_sensors(num_sensors=5, center_lat=38.1, center_lng=-122.25, radius=0.02):
    sensors = []
    for i in range(num_sensors):
        lat = center_lat + random.uniform(-radius, radius)
        lng = center_lng + random.uniform(-radius, radius)
        pm25 = round(random.uniform(0, 50), 1)  # PM2.5 between 0-50
        sensors.append({
            "sensor_id": 1000 + i,
            "name": f"Mock Sensor {i+1}",
            "latitude": lat,
            "longitude": lng,
            "pm2_5": pm25,
            "last_seen": (datetime.utcnow() - timedelta(minutes=random.randint(0, 60))).isoformat() + "Z"
        })
    return sensors

@sensors_bp.route('/mock-sensors')
def get_mock_sensors():
    mock_data = generate_mock_sensors()
    return jsonify({"sensors": mock_data})
