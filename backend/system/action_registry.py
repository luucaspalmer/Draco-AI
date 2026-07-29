"""
Draco AI
System Actions - Action Registry

Registro central de tudo o que o Draco
sabe executar no sistema operacional.

Para ensinar o Draco a abrir um novo
programa, basta adicionar uma entrada
neste arquivo.

Nenhum outro módulo do System Actions API
precisa ser alterado para isso.
"""


# =====================================
# Registro de aplicações conhecidas
# =====================================
#
# Cada entrada representa uma aplicação
# que o Draco sabe abrir.
#
# "executavel" -> comando ou caminho
#                 utilizado pelo executor
#
# "sinonimos"  -> palavras que o usuário
#                 pode usar para se referir
#                 à aplicação
#

APPLICATION_REGISTRY = {

    "cmd": {

        "executavel": "cmd.exe",

        "sinonimos": [
            "cmd",
            "prompt de comando",
            "prompt",
            "terminal",
            "console"
        ]

    },

    "calculator": {

        "executavel": "calc.exe",

        "sinonimos": [
            "calculadora",
            "calculator",
            "calc"
        ]

    },

    "notepad": {

        "executavel": "notepad.exe",

        "sinonimos": [
            "bloco de notas",
            "notepad"
        ]

    },

    "explorer": {

        "executavel": "explorer.exe",

        "sinonimos": [
            "explorador de arquivos",
            "explorador",
            "meus arquivos",
            "explorer"
        ]

    },

    "chrome": {

        "executavel": "chrome.exe",

        "sinonimos": [
            "google chrome",
            "chrome",
            "navegador"
        ]

    },

    "spotify": {

        "executavel": "spotify.exe",

        "sinonimos": [
            "spotify"
        ]

    },

    "discord": {

        "executavel": "discord.exe",

        "sinonimos": [
            "discord"
        ]

    }

}


# =====================================
# Buscar aplicação pelo nome canônico
# =====================================

def obter_aplicacao(target):

    return APPLICATION_REGISTRY.get(
        target
    )


# =====================================
# Resolver aplicação a partir de texto
# =====================================

def resolver_target_por_sinonimo(texto):
    """
    Recebe um trecho de texto e tenta
    encontrar a qual aplicação registrada
    ele corresponde.

    Quando mais de um sinônimo é encontrado,
    prevalece o mais específico (mais longo),
    evitando que "prompt" vença sobre
    "prompt de comando", por exemplo.

    Retorna o nome canônico da aplicação
    (a chave do registro) ou None.
    """

    if not texto:

        return None

    texto = texto.lower().strip()

    melhor_target = None

    melhor_tamanho = 0

    for target, dados in APPLICATION_REGISTRY.items():

        for sinonimo in dados["sinonimos"]:

            if sinonimo in texto:

                if len(sinonimo) > melhor_tamanho:

                    melhor_target = target

                    melhor_tamanho = len(sinonimo)

    return melhor_target


# =====================================
# Listar aplicações conhecidas
# =====================================

def listar_aplicacoes():

    return list(
        APPLICATION_REGISTRY.keys()
    )


# =====================================
# Registrar nova aplicação em tempo
# de execução (opcional)
# =====================================

def registrar_aplicacao(
    target,
    executavel,
    sinonimos
):
    """
    Permite registrar uma nova aplicação
    sem editar este arquivo manualmente.

    Útil caso o Draco venha a aprender
    novas aplicações dinamicamente no
    futuro (ex: via configuração externa).
    """

    APPLICATION_REGISTRY[target] = {

        "executavel": executavel,

        "sinonimos": sinonimos

    }
