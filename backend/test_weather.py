from weather.weather_service import WeatherService
from weather.weather_formatter import WeatherFormatter



weather = WeatherService()

formatter = WeatherFormatter()



data = weather.get_weather(
    -25.413006,
    -49.241608
)


resposta = formatter.format_current_weather(
    data
)


print(resposta)