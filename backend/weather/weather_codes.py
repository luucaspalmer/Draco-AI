"""
Weather Codes
-------------
Traduz os códigos meteorológicos (WMO Weather Interpretation Codes)
retornados pela API Open-Meteo para descrições em português.

Referência:
https://open-meteo.com/en/docs
"""


WEATHER_CODES = {

    # Céu limpo
    0: "céu limpo",

    # Nuvens
    1: "predominantemente limpo",
    2: "parcialmente nublado",
    3: "encoberto",

    # Neblina
    45: "neblina",
    48: "neblina com geada",

    # Garoa
    51: "garoa leve",
    53: "garoa moderada",
    55: "garoa intensa",

    # Garoa congelante
    56: "garoa congelante leve",
    57: "garoa congelante intensa",

    # Chuva
    61: "chuva fraca",
    63: "chuva moderada",
    65: "chuva forte",

    # Chuva congelante
    66: "chuva congelante leve",
    67: "chuva congelante intensa",

    # Neve
    71: "queda de neve fraca",
    73: "queda de neve moderada",
    75: "queda de neve intensa",
    77: "cristais de neve",

    # Pancadas de chuva
    80: "pancadas de chuva fracas",
    81: "pancadas de chuva moderadas",
    82: "pancadas de chuva fortes",

    # Pancadas de neve
    85: "pancadas de neve fracas",
    86: "pancadas de neve fortes",

    # Tempestades
    95: "tempestade",
    96: "tempestade com granizo leve",
    99: "tempestade com granizo intenso"

}


def get_weather_description(code: int) -> str:
    """
    Retorna a descrição em português de um código meteorológico.

    Args:
        code: Código WMO retornado pela Open-Meteo.

    Returns:
        Descrição legível para o usuário.
    """

    return WEATHER_CODES.get(
        code,
        "condições meteorológicas desconhecidas"
    )