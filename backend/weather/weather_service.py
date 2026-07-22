"""
Weather Service
---------------
Responsável por consultar informações meteorológicas
utilizando a API Open-Meteo.

Documentação:
https://open-meteo.com/
"""

import requests


class WeatherService:
    """Serviço responsável por consultar dados meteorológicos."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(
        self,
        latitude: float,
        longitude: float
    ) -> dict:
        """
        Consulta as condições meteorológicas atuais.

        Args:
            latitude: Latitude da localização.
            longitude: Longitude da localização.

        Returns:
            Dicionário contendo os dados retornados pela API.
        """

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": [

                "temperature_2m",

                "apparent_temperature",

                "relative_humidity_2m",

                "weather_code",

                "wind_speed_10m",

                "wind_direction_10m",

                "surface_pressure",

                "precipitation",

                "is_day"

            ],

            "forecast_days": 1

        }

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:

            raise RuntimeError(
                f"Erro ao consultar a API Open-Meteo: {error}"
            ) from error