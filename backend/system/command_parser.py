"""
Draco AI
System Actions - Command Parser

Responsável por interpretar frases do
usuário em linguagem natural e transformá-las
em uma Action estruturada.

Este módulo NUNCA executa nada.
Ele apenas interpreta.

Fluxo:

"Abra o CMD"
        ↓
Action(intent="open_application", target="cmd")
"""

import re

from backend.system.models import Action

from backend.system.action_registry import (
    resolver_target_por_sinonimo
)


# =====================================
# Gatilhos de abertura de aplicação
# =====================================
#
# Ordenados do mais específico para o
# mais genérico, para que "quero abrir"
# seja reconhecido antes de "quero".
#

OPEN_TRIGGERS = [

    "me abre o",
    "me abre a",

    "quero abrir",
    "quero o",
    "quero a",

    "inicie o",
    "inicie a",

    "execute o",
    "execute a",

    "abra o",
    "abra a",
    "abrir o",
    "abrir a",
    "abre o",
    "abre a",

    "abra",
    "abrir",
    "abre",

    "iniciar",
    "inicia",

    "executar"

]


# =====================================
# Normalização de texto
# =====================================

def _normalizar(texto):

    texto = texto.lower().strip()

    texto = re.sub(
        r"[?!.,;:]+",
        "",
        texto
    )

    return " ".join(
        texto.split()
    )


# =====================================
# Detectar: abrir aplicação
# =====================================

def _detectar_open_application(texto):

    # Caso 1:
    # o gatilho aparece no início da frase
    # Exemplo: "abra o cmd"

    for gatilho in OPEN_TRIGGERS:

        if texto.startswith(gatilho):

            resto = texto[len(gatilho):].strip()

            alvo_texto = resto if resto else texto

            target = resolver_target_por_sinonimo(
                alvo_texto
            )

            if target:

                return Action(

                    intent="open_application",

                    target=target

                )

    # Caso 2:
    # o gatilho existe em qualquer lugar
    # da frase, junto com um alvo conhecido
    # Exemplo: "quero o terminal aberto"

    possui_gatilho = any(

        gatilho in texto

        for gatilho in OPEN_TRIGGERS

    )

    if possui_gatilho:

        target = resolver_target_por_sinonimo(
            texto
        )

        if target:

            return Action(

                intent="open_application",

                target=target

            )

    return None


# =====================================
# Parser principal
# =====================================

def parse_command(texto):
    """
    Recebe um texto do usuário e retorna
    uma Action correspondente.

    Retorna None caso o texto não
    represente um comando de sistema
    conhecido pelo Draco.
    """

    if not texto:

        return None

    texto_normalizado = _normalizar(
        texto
    )

    # =================================
    # Intenções suportadas
    # =================================

    detectores = [

        _detectar_open_application

        # Novas intenções (ex: fechar
        # aplicação, ajustar volume)
        # podem ser adicionadas aqui
        # como novas funções

    ]

    for detectar in detectores:

        action = detectar(
            texto_normalizado
        )

        if action:

            return action

    return None
