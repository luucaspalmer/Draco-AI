"""
Draco AI
System Actions API

Interface pública do módulo de ações
do sistema operacional.

O restante do Draco (brain.py, tools,
question_analyzer, etc.) deve conversar
SOMENTE com este arquivo.

Ninguém fora deste módulo deve importar
command_parser, action_executor ou
action_registry diretamente.

Fluxo:

Texto do usuário
        ↓
command_parser  -> interpreta
        ↓
      Action
        ↓
action_executor -> executa
        ↓
   ActionResult
"""

from backend.system.models import Action, ActionResult

from backend.system.command_parser import parse_command

from backend.system.action_executor import execute

from backend.system.action_registry import listar_aplicacoes


# =====================================
# Verificar se o texto é um comando
# de sistema
# =====================================

def is_system_command(texto: str) -> bool:
    """
    Indica se um texto representa um
    comando de sistema reconhecido,
    sem executar nada.

    Útil para módulos de intenção
    (ex: question_analyzer) decidirem
    se devem encaminhar a mensagem para
    o System Actions API.
    """

    return parse_command(texto) is not None


# =====================================
# Executar uma ação já estruturada
# =====================================

def execute_action(
    intent: str,
    target: str = None,
    parameters: dict = None
) -> ActionResult:
    """
    Executa diretamente uma ação já
    conhecida, sem passar pelo parser.

    Exemplo:

    execute_action(
        intent="open_application",
        target="cmd"
    )
    """

    action = Action(

        intent=intent,

        target=target,

        parameters=parameters or {}

    )

    return execute(action)


# =====================================
# Interpretar e executar um texto
# =====================================

def process_text(texto: str) -> ActionResult:
    """
    Interpreta um texto em linguagem
    natural e, caso corresponda a um
    comando de sistema conhecido,
    executa a ação correspondente.

    Retorna None quando o texto não é
    reconhecido como um comando de
    sistema (o chamador deve então
    seguir o fluxo normal do Draco).
    """

    action = parse_command(texto)

    if not action:

        return None

    return execute(action)


# =====================================
# Aplicações conhecidas pelo Draco
# =====================================

def get_known_applications():

    return listar_aplicacoes()
