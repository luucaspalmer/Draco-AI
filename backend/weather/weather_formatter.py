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
                f" Há registro de precipitação "
                f"de {precipitation} mm."
            )

        else:

            rain_status = (
                " Não há registro de chuva no momento."
            )



        return (

            f"Consultei as condições meteorológicas de Araucária. "

            f"{period.capitalize()}, "
            f"a temperatura é de {temperature}°C "
            f"com sensação térmica de {feels_like}°C. "

            f"A umidade relativa do ar está em "
            f"{humidity}%. Condição atual: "
            f"{weather_description}. "

            f"Os ventos estão a "
            f"{wind_speed} km/h "
            f"(vindos do {wind_direction}). "

            f"A pressão atmosférica está em "
            f"{pressure} hPa."

            f"{rain_status}"

        )