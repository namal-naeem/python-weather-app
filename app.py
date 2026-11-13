
import streamlit as st
import requests

st.set_page_config(
    page_title="Weather App",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Weather Information App")
st.write("Check the current weather of any city around the world.")

city = st.text_input("Enter city name:", placeholder="e.g. Tokyo")

if st.button("Get Weather"):

    if not city.strip():
        st.warning("Please enter a city name.")

    else:
        try:
            with st.spinner("Searching for your city..."):

                geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                geo_params = {
                    "name": city.strip(),
                    "count": 5,
                    "language": "en",
                    "format": "json",
                    "feature_code": "PPLC,PPLA,PPLA2,PPLA3"
                }

                geo_response = requests.get(
                    geo_url,
                    params=geo_params,
                    timeout=20
                )

                geo_response.raise_for_status()
                geo_data = geo_response.json()

            if not geo_data.get("results"):
                st.error("City not found. Please try another city.")

            else:
                location = geo_data["results"][0]

                with st.spinner("Fetching weather information..."):

                    weather_url = "https://api.open-meteo.com/v1/forecast"

                    weather_params = {
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                        "current": "temperature_2m,relative_humidity_2m,weather_code",
                        "timezone": "auto"
                    }

                    weather_response = requests.get(
                        weather_url,
                        params=weather_params,
                        timeout=20
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

                st.success("Weather found successfully!")

                st.subheader(
                    f"Weather in {location['name']}, {location['country']}"
                )

                col1, col2 = st.columns(2)

                col1.metric("Temperature", f"{temperature} °C")
                col2.metric("Humidity", f"{humidity}%")

                st.write("Weather condition:", condition)

        except requests.exceptions.Timeout:
            st.error("The weather service took too long to respond. Please try again.")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

        except (KeyError, IndexError, TypeError):
            st.error("Unexpected weather data received. Please try again.")
