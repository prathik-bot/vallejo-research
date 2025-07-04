import requests
from datetime import datetime, timedelta
from functools import lru_cache
from app.utils.config import PURPLEAIR_API_KEY
from app.utils.helpers import calculate_bounding_box
import json


class PurpleAirService:
    """
    Service layer for interacting with PurpleAir API
    Handles data fetching, caching, and error recovery
    """

    BASE_URL = "https://api.purpleair.com/v1/sensors"
    CACHE_TTL = timedelta(minutes=5)  # Cache for 5 minutes

    def __init__(self):
        self.last_fetch = None
        self.last_data = None

    @lru_cache(maxsize=32)
    def _make_api_request(self, params_json):
        """Core API request with error handling"""
        params = json.loads(params_json)
        try:
            response = requests.get(
                self.BASE_URL,
                headers={"X-API-Key": "9A211F43-55E7-11F0-81BE-42010A80001F"},
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            return None

    def get_sensors_in_area(self, center_lat, center_lng, radius_km=5):
        """
        Get sensors within a geographic area
        Args:
            center_lat: Latitude of center point
            center_lng: Longitude of center point
            radius_km: Search radius in kilometers
        Returns:
            {
                "sensors": [list of sensor dicts],
                "stats": {
                    "pm2.5": {"min": x, "max": y, "avg": z},
                    "last_updated": iso_timestamp
                }
            }
        """
        bbox = calculate_bounding_box(center_lat, center_lng, radius_km)

        params = {
            "fields": "sensor_index,name,latitude,longitude,pm2.5,last_seen",
            "location_type": 0,  # Outdoor sensors only
            "max_age": 3600,  # 1 hour max data age
            "nwlng": bbox['nw']['lng'],
            "nwlat": bbox['nw']['lat'],
            "selng": bbox['se']['lng'],
            "selat": bbox['se']['lat']
        }

        # Convert params to JSON string for caching
        params_json = json.dumps(params, sort_keys=True)
        data = self._make_api_request(params_json)
        if not data or 'data' not in data:
            return None

        sensors = []
        pm_values = []

        for sensor in data['data']:
            sensor_data = dict(zip(data['fields'], sensor))
            if sensor_data.get('pm2.5') is not None:
                pm_values.append(float(sensor_data['pm2.5']))

            sensors.append({
                "id": sensor_data['sensor_index'],
                "name": sensor_data['name'],
                "location": {
                    "lat": sensor_data['latitude'],
                    "lng": sensor_data['longitude']
                },
                "pm2_5": sensor_data.get('pm2.5'),
                "last_seen": datetime.fromtimestamp(sensor_data['last_seen']).isoformat()
            })

        stats = {
            "pm2.5": {
                "min": min(pm_values) if pm_values else None,
                "max": max(pm_values) if pm_values else None,
                "avg": sum(pm_values) / len(pm_values) if pm_values else None
            },
            "sensor_count": len(sensors),
            "active_count": len(pm_values),
            "last_updated": datetime.utcnow().isoformat()
        }

        return {
            "sensors": sensors,
            "stats": stats,
            "bounding_box": bbox
        }

    def get_sensor_by_id(self, sensor_id):
        """Get detailed data for a specific sensor"""
        params = {
            "fields": "sensor_index,name,latitude,longitude,pm2.5,last_seen,"
                      "humidity,temperature,pressure,confidence",
            "sensor_index": sensor_id
        }

        # Convert params to JSON string for caching
        params_json = json.dumps(params, sort_keys=True)
        data = self._make_api_request(params_json)
        if not data or not data.get('data'):
            return None

        sensor = dict(zip(data['fields'], data['data'][0]))
        return {
            "id": sensor['sensor_index'],
            "name": sensor['name'],
            "location": {
                "lat": sensor['latitude'],
                "lng": sensor['longitude']
            },
            "measurements": {
                "pm2_5": sensor.get('pm2.5'),
                "humidity": sensor.get('humidity'),
                "temperature": sensor.get('temperature'),
                "pressure": sensor.get('pressure')
            },
            "confidence": sensor.get('confidence', 0),
            "last_seen": datetime.fromtimestamp(sensor['last_seen']).isoformat()
        }