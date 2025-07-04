# tests/test_purpleair.py
from datetime import datetime
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from app.services.purpleair import PurpleAirService


def test_purpleair_service():
    print("\n=== Testing PurpleAir Service ===")

    service = PurpleAirService()

    # Test 1: Get sensors in Vallejo area
    print("\n[Test 1] Fetching sensors in Vallejo...")
    vallejo_data = service.get_sensors_in_area(
        center_lat=38.1041,
        center_lng=-122.2560,
        radius_km=5
    )

    if vallejo_data:
        print(f"Found {vallejo_data['stats']['sensor_count']} sensors")
        print(f"PM2.5 Stats: Min={vallejo_data['stats']['pm2.5']['min']} "
              f"Max={vallejo_data['stats']['pm2.5']['max']} "
              f"Avg={vallejo_data['stats']['pm2.5']['avg']}")

        # Test 2: Get details for first sensor
        if vallejo_data['sensors']:
            first_sensor = vallejo_data['sensors'][0]
            print(f"\n[Test 2] Fetching details for sensor {first_sensor['id']}...")
            sensor_details = service.get_sensor_by_id(first_sensor['id'])

            if sensor_details:
                print(f"Details for {sensor_details['name']}:")
                print(f"Location: {sensor_details['location']['lat']}, {sensor_details['location']['lng']}")
                print(f"Last seen: {sensor_details['last_seen']}")
                print(f"PM2.5: {sensor_details['measurements']['pm2_5']}")
                print(f"Temp: {sensor_details['measurements']['temperature']}°C")
            else:
                print("Failed to fetch sensor details")
    else:
        print("Failed to fetch area sensor data")


if __name__ == "__main__":
    test_purpleair_service()