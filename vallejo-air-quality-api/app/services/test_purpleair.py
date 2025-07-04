from app.services.purpleair import PurpleAirService


def test_fetch_sensors():
    service = PurpleAirService()
    data = service.get_sensors_in_area(38.1041, -122.2560, radius_km=5)
    if data is None:
        print("No data returned or API request failed")
    else:
        print(f"Found {len(data['sensors'])} sensors")
        for sensor in data['sensors']:
            print(sensor)

if __name__ == "__main__":
    test_fetch_sensors()
