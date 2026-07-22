"""
Weather Tool
------------
Interface do Draco para consultar informações meteorológicas.
"""

from backend.weather.weather_service import WeatherService
from backend.weather.weather_formatter import WeatherFormatter


class WeatherTool:
    """Ferramenta responsável por consultar e formatar informações do clima."""

    # Localização padrão (Araucária/PR)
    DEFAULT_LATITUDE = -25.5931
    DEFAULT_LONGITUDE = -49.4042

    def __init__(self):
        self.service = WeatherService()
        self.formatter = WeatherFormatter()

    def execute(
        self,
        latitude: float = DEFAULT_LATITUDE,
        longitude: float = DEFAULT_LONGITUDE,
    ) -> str:
        """
        Consulta o clima e retorna uma resposta pronta para o usuário.

        Args:
            latitude: Latitude da localização.
            longitude: Longitude da localização.

        Returns:
            Resposta formatada em português.
        """

        try:
            weather_data = self.service.get_weather(
                latitude=latitude,
                longitude=longitude
            )

            if not weather_data:
                return (
                    "Não foi possível obter informações meteorológicas no momento."
                )

            return self.formatter.format_current_weather(
                weather_data
            )

        except Exception as error:
            print(f"[WeatherTool] Erro: {error}")

            return (
                "Ocorreu um erro ao consultar a previsão do tempo."
            )