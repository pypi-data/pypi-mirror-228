import requests

class WeatherApp:

    _API_KEY = "7a9d100dc1d4a5ac458caf5ac8b79a8f"
    _BASE_URL = "https://api.openweathermap.org/data/2.5/weather"    
    
    def get_weather(self, city):
        try:
            params = {"APPID": self._API_KEY, "q": city, "units": "metric"}
            response = requests.get( self._BASE_URL, params=params)
            weather = response.json()
            return weather
        except Exception as e:
            print(e)
    
    def weather_report(self, weather):
        try:
            report = f"""
            City: {weather['name']}
            Country: {weather['sys']['country']}
            Temperature: {weather['main']['temp']}°C
            Feels like: {weather['main']['feels_like']}°C
            Weather: {weather['weather'][0]['main']}
            Description: {weather['weather'][0]['description']}
            """
            return report
        except Exception as e:
            print(e)