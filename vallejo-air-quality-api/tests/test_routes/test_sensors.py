def test_get_sensors(client):
    response = client.get('/api/sensors')
    assert response.status_code == 200
    assert 'sensors' in response.json