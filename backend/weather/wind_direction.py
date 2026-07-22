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



    directions = [

        (0, "norte"),

        (22.5, "nordeste"),

        (67.5, "leste"),

        (112.5, "sudeste"),

        (157.5, "sul"),

        (202.5, "sudoeste"),

        (247.5, "oeste"),

        (292.5, "noroeste"),

        (337.5, "norte")

    ]



    for limit, direction in directions:

        if degrees < limit:

            return direction



    return "norte"