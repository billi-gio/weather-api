from pytest import mark
import responses

from weather_api.weather_requests.clients.weather_clients_folder.base_day_forecast import (
    CallEndpointMixin,
    ForecastClientConfig,
)


@mark.parametrize(
    "endpoint, parameters, expected_result",
    [
        (
            "https://api.openweathermap.org/data/2.5/forecast/daily",
            {"q": "city", "units": "metric", "appid": "0000000"},
            "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        ),
        (
            "https://api.openweathermap.org/data/2.5/weather",
            {"q": "city", "units": "metric", "appid": "0000000"},
            "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        ),
    ],
)
@responses.activate
def test_call_endpoint_nonexistent_apikey(endpoint, parameters, expected_result):
    responses.add(
        responses.GET,
        "https://api.openweathermap.org/data/2.5/weather?q=city&units=metric&appid=0000000",
        json={
            "cod": "401",
            "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        },
        status=401,
    )

    responses.add(
        responses.GET,
        "https://api.openweathermap.org/data/2.5/forecast/daily?q=city&units=metric&appid=0000000",
        json={
            "cod": "401",
            "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        },
        status=401,
    )

    config = ForecastClientConfig("0000000")
    client = CallEndpointMixin(config)

    response = client.call_endpoint(endpoint, parameters)
    assert response.json()["cod"] == "401"
    assert response.json()["message"] == expected_result


@mark.parametrize(
    "endpoint, parameters, expected_result",
    [
        (
            "https://api.openweathermap.org/data/2.5/forecast/daily",
            {"q": "non_existant", "units": "metric", "appid": "123abc"},
            "city not found",
        ),
        (
            "https://api.openweathermap.org/data/2.5/weather",
            {"q": "non_existant", "units": "metric", "appid": "123abc"},
            "city not found",
        ),
    ],
)
@responses.activate
def test_call_endpoint_nonexistent_city(endpoint, parameters, expected_result):
    responses.add(
        responses.GET,
        "https://api.openweathermap.org/data/2.5/weather?q=non_existant&units=metric&appid=123abc",
        json={"cod": "404", "message": "city not found"},
        status=404,
    )

    responses.add(
        responses.GET,
        "https://api.openweathermap.org/data/2.5/forecast/daily?q=non_existant&units=metric&appid=123abc",
        json={"cod": "404", "message": "city not found"},
        status=404,
    )

    config = ForecastClientConfig("123abc")
    client = CallEndpointMixin(config)

    response = client.call_endpoint(endpoint, parameters)
    assert response.json()["cod"] == "404"
    assert response.json()["message"] == expected_result
