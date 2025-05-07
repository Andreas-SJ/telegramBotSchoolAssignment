import requests
from credentials import weatherUserAgent, geoUserAgent
from geopy.geocoders import Nominatim

def get_weather(city, time):
    geolocator = Nominatim(user_agent=geoUserAgent)
    location = geolocator.geocode(city)

    if not location:
        return f"Could not find location: {city}"

    coords = {
        'lat': location.latitude,
        'long': location.longitude
    }

    headers = {'User-Agent': weatherUserAgent}
    response = requests.get(
        f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={coords['lat']}&lon={coords['long']}",
        headers=headers
    )

    try:
        air_temp = response.json()["properties"]["timeseries"][time]["data"]["instant"]["details"]["air_temperature"]
        return f"{air_temp}°C"
    except (IndexError, KeyError, ValueError):
        return "Invalid clock index or weather data not found."