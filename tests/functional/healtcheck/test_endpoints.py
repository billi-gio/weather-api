def test_returns_correct_response(test_client):
    # given
    endpoint = "/healthcheck"

    # when
    response = test_client.get(endpoint)

    # when
    assert response.status_code == 200
    assert response.json() == {
        # "environment": "test",
        "service": "weather-api",
    }
