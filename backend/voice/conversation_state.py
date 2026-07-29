"""
Draco AI
Voice - Conversation State

Máquina de estados do modo de ativação por voz (Wake Word).

WAITING_WAKE -> WAKE_WORD_DETECTED -> LISTENING -> PROCESSING -> SPEAKING -> WAITING_WAKE

Cada ciclo completo (uma wake word) permite EXATAMENTE uma
pergunta e uma resposta. Ao final de SPEAKING, o sistema
retorna sempre para WAITING_WAKE, onde só reage novamente à
wake word.
"""

from enum import Enum, auto


class ConversationState(Enum):

    WAITING_WAKE = auto()
    WAKE_WORD_DETECTED = auto()
    LISTENING = auto()
    PROCESSING = auto()
    SPEAKING = auto()


class ConversationStateMachine:

    def __init__(self):

        self.state = ConversationState.WAITING_WAKE

    def transition(self, novo_estado: ConversationState):

        print(f"[Estado] {self.state.name} -> {novo_estado.name}")

        self.state = novo_estado

    def is_waiting_wake(self):

        return self.state == ConversationState.WAITING_WAKE