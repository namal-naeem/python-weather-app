
import requests

city = input("Enter city name: ")

print("Searching weather for:", city)

url = "https://geocoding-api.open-meteo.com/v1/search"

params = {
    "name": city,
    "count": 5,
    "language": "en",
    "format": "json",
    "feature_code": "PPLC,PPLA,PPLA2,PPLA3"
}

try:
    print("Connecting to Geocoding API...")

    # Retry the geocoding request up to 3 times
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3")

            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()

            data = response.json()
            print("API response received!")
            break

        except requests.exceptions.RequestException as e:
            print("Connection failed:", e)

    else:
        print("Unable to connect after 3 attempts.")
        raise SystemExit

    if data.get("results"):

        location = data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        print("City:", location["name"])
        print("Country:", location["country"])
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "auto"
        }

        print("Fetching weather information...")

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=60
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = current["weather_code"]

        if weather_code == 0:
            condition = "Clear sky"
        elif weather_code in [1, 2, 3]:
            condition = "Partly cloudy"
        elif weather_code in [45, 48]:
            condition = "Foggy"
        elif weather_code in [51, 53, 55]:
            condition = "Drizzle"
        elif weather_code in [61, 63, 65]:
            condition = "Rain"
        elif weather_code in [95, 96, 99]:
            condition = "Thunderstorm"
        else:
            condition = "Other weather condition"

        print("\n----- WEATHER REPORT -----")
        print("City:", location["name"])
        print("Country:", location["country"])
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")
        print("Weather Condition:", condition)

    else:
        print("City not found!")

except requests.exceptions.RequestException as e:
    print("Connection error:", e)
