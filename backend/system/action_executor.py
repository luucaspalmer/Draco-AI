"""
Draco AI
System Actions - Action Executor

Responsável por executar ações já
estruturadas (Action) no sistema
operacional Windows.

Este é o único módulo do System Actions
API que efetivamente interage com o
sistema operacional.

command_parser e action_registry nunca
tocam em subprocess.
"""

import subprocess

from backend.system.models import Action, ActionResult

from backend.system.action_registry import obter_aplicacao


# =====================================
# Executor: abrir aplicação
# =====================================

def _executar_open_application(
    action: Action
) -> ActionResult:

    aplicacao = obter_aplicacao(
        action.target
    )

    if not aplicacao:

        return ActionResult(

            success=False,

            message=(
                f"Não conheço a aplicação '{action.target}'."
            ),

            action=action

        )

    executavel = aplicacao["executavel"]

    try:

        subprocess.Popen(

            executavel,

            creationflags=subprocess.CREATE_NEW_CONSOLE

        )

        return ActionResult(

            success=True,

            message=(
                f"Abrindo {action.target}."
            ),

            action=action

        )

    except Exception as erro:

        return ActionResult(

            success=False,

            message=(
                f"Não consegui abrir {action.target}: {erro}"
            ),

            action=action

        )


# =====================================
# Mapa de executores
# =====================================
#
# Cada intenção suportada aponta para
# a função responsável por executá-la.
#
# Novas intenções (fechar aplicação,
# ajustar volume, bloquear tela, etc.)
# são adicionadas aqui, sem alterar
# a função execute().
#

EXECUTORS = {

    "open_application": _executar_open_application

}


# =====================================
# Executor principal
# =====================================

def execute(action: Action) -> ActionResult:
    """
    Executa uma Action utilizando o
    executor registrado para sua intenção.
    """

    executor = EXECUTORS.get(
        action.intent
    )

    if not executor:

        return ActionResult(

            success=False,

            message=(
                f"Intenção '{action.intent}' ainda não é suportada."
            ),

            action=action

        )

    return executor(action)
