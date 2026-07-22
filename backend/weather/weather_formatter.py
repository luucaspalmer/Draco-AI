"""
Weather Formatter
-----------------
Transforma dados meteorológicos da API Open-Meteo
em respostas naturais para o Draco AI.
"""


from backend.weather.weather_codes import (
    get_weather_description
)

from backend.weather.wind_direction import (
    get_wind_direction
)



class WeatherFormatter:
    """
    Responsável por formatar informações do clima.
    """



    def format_current_weather(
        self,
        data: dict
    ) -> str:
        """
        Converte dados atuais do clima em uma resposta textual.
        """

        current = data.get(
            "current",
            {}
        )


        print("\n===== WEATHER API =====")
        print(current)
        print("=======================\n")


        temperature = current.get(
            "temperature_2m",
            "desconhecida"
        )


        feels_like = current.get(
            "apparent_temperature",
            "desconhecida"
        )


        humidity = current.get(
            "relative_humidity_2m",
            "desconhecida"
        )


        weather_code = current.get(
            "weather_code"
        )


        weather_description = get_weather_description(
            weather_code
        )


        wind_speed = current.get(
            "wind_speed_10m",
            0
        )


        wind_direction = get_wind_direction(
            current.get(
                "wind_direction_10m"
            )
        )


        pressure = current.get(
            "surface_pressure",
            "desconhecida"
        )


        precipitation = current.get(
            "precipitation",
            0
        )


        is_day = current.get(
            "is_day",
            1
        )


        period = (
            "durante o dia"
            if is_day
            else "neste momento à noite"
        )



        if precipitation > 0:

            rain_status = (
                f"No momento, há precipitação registrada de "
                f"{precipitation} mm."
            )

        else:

            rain_status = (
                " No momento, não há precipitação registrada pelos dados meteorológicos consultados."
            )



        return (

            f"Consultei as condições meteorológicas para Araucária. "

            f"{period.capitalize()}, a temperatura é de "
            f"{temperature}°C, com sensação térmica de "
            f"{feels_like}°C. "

            f"O tempo está {weather_description}, "
            f"com umidade relativa do ar em "
            f"{humidity}%. "

            f"Os ventos sopram do "
            f"{wind_direction} "
            f"a {wind_speed} km/h. "

            f"A pressão atmosférica está em "
            f"{pressure} hPa. "

            f"{rain_status}"

        )