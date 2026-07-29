"""
Wind Direction
--------------
Converte graus de direção do vento
em orientação textual.
"""


WIND_DIRECTIONS = {

    0: "norte",

    45: "nordeste",

    90: "leste",

    135: "sudeste",

    180: "sul",

    225: "sudoeste",

    270: "oeste",

    315: "noroeste"

}



def get_wind_direction(
    degrees: float
) -> str:
    """
    Converte graus em direção do vento.

    Args:
        degrees:
            Direção em graus retornada pela API.

    Returns:
        Direção textual.
    """


    if degrees is None:

        return "desconhecida"



    # Normaliza valores
    degrees = degrees % 360



    direction_index = int(
        (degrees + 22.5) // 45
    ) % 8

    return WIND_DIRECTIONS[
        direction_index * 45
    ]
