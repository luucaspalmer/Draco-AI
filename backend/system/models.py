"""
Draco AI
System Actions - Models

Modelos de dados utilizados pelo
System Actions API.

Uma Action representa "o que fazer".
Um ActionResult representa "o que aconteceu".
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


# =====================================
# Ação
# =====================================

@dataclass
class Action:
    """
    Representa uma ação a ser executada
    no sistema operacional.

    intent:
        Tipo da ação.
        Exemplo: "open_application"

    target:
        Alvo da ação.
        Exemplo: "cmd", "calculator"

    parameters:
        Dados adicionais opcionais
        necessários para a execução.
    """

    intent: str

    target: Optional[str] = None

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )


# =====================================
# Resultado da ação
# =====================================

@dataclass
class ActionResult:
    """
    Representa o resultado da execução
    de uma Action.
    """

    success: bool

    message: str

    action: Optional[Action] = None
