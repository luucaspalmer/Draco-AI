"""
Draco AI - LLM / Ollama Client (Provedor Offline)

IMPORTANTE:

Este arquivo NÃO reimplementa a comunicação com o Ollama.

Toda a lógica HTTP original (streaming, tratamento de erro,
timeout, montagem do payload) continua vivendo, inalterada,
em:

    backend/ollama_client.py  (perguntar_ao_qwen)

Motivo dessa decisão:

    backend/memory/memory_extractor.py já importa
    "perguntar_ao_qwen" diretamente de backend.ollama_client.
    Mover ou duplicar essa função exigiria alterar um módulo
    de memory, o que está fora do escopo desta mudança.

Este arquivo é apenas um adaptador (adapter) que faz o
backend/ollama_client.py existente seguir o contrato BaseLLM,
para que o llm_manager.py possa tratá-lo como "só mais um
provedor de LLM", igual ao Gemini ou a qualquer outro futuro.
"""

from backend.llm.base_llm import BaseLLM

from backend.ollama_client import perguntar_ao_qwen


class OllamaLLM(BaseLLM):
    """
    Provedor Offline do Draco AI.

    Adaptador sobre a função perguntar_ao_qwen já existente
    em backend/ollama_client.py. Nenhuma lógica de rede nova
    é introduzida aqui.
    """

    def generate(self, prompt: str, num_predict: int = 300) -> str:

        return perguntar_ao_qwen(
            prompt,
            num_predict=num_predict
        )

    def available(self) -> bool:
        """
        O Ollama é o provedor padrão/offline do Draco AI.

        Não fazemos uma checagem de rede aqui (isso adicionaria
        latência extra a cada resposta). A função original
        perguntar_ao_qwen já trata falha de conexão e timeout
        internamente, retornando uma mensagem de fallback
        amigável em vez de lançar exceção.

        Portanto, do ponto de vista do llm_manager.py, o
        Ollama está sempre "disponível para tentar" -
        exatamente o comportamento atual do sistema.
        """

        return True


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    cliente = OllamaLLM()

    print("Disponível:", cliente.available())

    print(
        cliente.generate(
            "Responda apenas: teste ok.",
            num_predict=20
        )
    )
