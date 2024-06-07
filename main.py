import requests
import datetime
import re

def get_weather(api_key, city, date):
    try:

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)

        if response.status_code == 401:
            return "Error: Unauthorized. Please check your API key."

        if response.status_code != 200:
            return f"Error: Unable to fetch data. Status code: {response.status_code}"

        data = response.json()

        if 'list' not in data:
            return "Error: No weather data available."

        for forecast in data['list']:
            forecast_time = datetime.datetime.fromtimestamp(forecast['dt'], datetime.timezone.utc)
            forecast_date = forecast_time.date()

            if forecast_date == datetime.datetime.strptime(date, "%Y-%m-%d").date():
                temp = forecast['main']['temp']
                weather_description = forecast['weather'][0]['description']
                return f"Weather in {city} on {date}: {weather_description}, temperature: {temp}°C"

        return "Weather data for the given date is not available."

    except Exception as e:
        return f"Error: {str(e)}"


def is_valid_city(city):
    return bool(re.match(r'^[A-Z-a-z]+$', city))


def is_valid_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    api_key = "f63364cab88fa91f8a1cfbc22295a4ae"

    city = input("Enter city: ")
    while not is_valid_city(city):
        print("Invalid city name. City should consist of one word and contain no numbers.")
        city = input("Enter city: ")

    date = input("Enter date (YYYY-MM-DD): ")
    while not is_valid_date(date):
        print("Invalid date. Please enter the date in YYYY-MM-DD format.")
        date = input("Enter date (YYYY-MM-DD): ")

    weather_report = get_weather(api_key, city, date)
    print(weather_report)
