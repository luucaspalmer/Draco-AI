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


        precipitation = current.get(
            "precipitation",
            0
        )

        daily = data.get(
            "daily",
            {}
        )

        minimum_temperature = self._get_today_value(
            daily,
            "temperature_2m_min"
        )

        maximum_temperature = self._get_today_value(
            daily,
            "temperature_2m_max"
        )

        precipitation_probability = self._get_today_value(
            daily,
            "precipitation_probability_max"
        )

        precipitation_sum = self._get_today_value(
            daily,
            "precipitation_sum"
        )

        current_status = (
            f"Em Araucária, agora faz {temperature}°C, "
            f"com sensação de {feels_like}°C e {weather_description}. "
            f"A umidade está em {humidity}%."
        )

        if wind_speed >= 15:
            current_status += (
                f" Venta de {wind_direction} "
                f"a {wind_speed} km/h."
            )

        if precipitation > 0:
            current_status += (
                f" Foram registrados {precipitation} mm de chuva "
                "nos últimos 15 minutos."
            )

        forecast_status = self._format_today_forecast(
            minimum_temperature,
            maximum_temperature,
            precipitation_probability,
            precipitation_sum
        )

        return f"{current_status}\n\n{forecast_status}"

    @staticmethod
    def _get_today_value(
        daily: dict,
        key: str
    ):
        """Retorna o primeiro valor diário disponível para hoje."""

        values = daily.get(
            key,
            []
        )

        return values[0] if values else None

    @staticmethod
    def _format_today_forecast(
        minimum_temperature,
        maximum_temperature,
        precipitation_probability,
        precipitation_sum
    ) -> str:
        """Monta um resumo simples da previsão para hoje."""

        if minimum_temperature is None or maximum_temperature is None:
            return "A previsão para o restante do dia não está disponível."

        forecast = (
            f"Para hoje, a temperatura varia entre {minimum_temperature}°C "
            f"e {maximum_temperature}°C."
        )

        if precipitation_probability is not None:
            forecast += (
                f" Há até {precipitation_probability}% de chance de chuva"
            )

            if precipitation_sum is not None:
                forecast += (
                    f", com previsão de {precipitation_sum} mm "
                    "ao longo do dia."
                )
            else:
                forecast += "."

        return forecast
