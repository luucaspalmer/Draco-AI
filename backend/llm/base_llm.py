"""
Draco AI - LLM / Base LLM

Interface base para qualquer provedor de LLM (Ollama, Gemini,
OpenAI, Claude, DeepSeek, Grok, Mistral, LM Studio, etc).

Este arquivo NÃO contém nenhuma implementação. Ele define
apenas o contrato que todo provedor precisa seguir para ser
utilizado pelo llm_manager.py.

Qualquer novo provedor de LLM adicionado no futuro deve:

1. Herdar de BaseLLM.
2. Implementar generate().
3. Implementar available().

Nenhuma outra parte do Draco AI (brain.py, prompt_builder.py,
etc) deve depender de um provedor específico. Todas as
chamadas devem passar pelo llm_manager.py.
"""

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Contrato mínimo que qualquer provedor de LLM deve seguir.
    """

    @abstractmethod
    def generate(self, prompt: str, num_predict: int = 300) -> str:
        """
        Gera uma resposta a partir de um prompt.

        Args:
            prompt: texto final já construído pelo prompt_builder.py.

            num_predict: teto máximo de tokens gerados pela
                resposta. Decidido pelo Response Planner
                (backend/question/response_planner.py).

        Returns:
            str com a resposta gerada pelo modelo.

        Cada provedor é responsável por tratar seus próprios
        erros internamente (timeout, conexão, etc) e retornar
        uma mensagem de fallback amigável em caso de falha,
        nunca lançar exceção para quem o chama (mesmo padrão
        já usado em backend/ollama_client.py).
        """

        raise NotImplementedError

    @abstractmethod
    def available(self) -> bool:
        """
        Indica se este provedor está pronto para ser utilizado
        no momento da chamada (ex: variável de ambiente
        configurada, serviço local acessível, etc).

        Usado pelo llm_manager.py para decidir se pode usar
        este provedor ou se deve recorrer a um fallback.

        Returns:
            True se o provedor pode ser utilizado agora.
        """

        raise NotImplementedError
