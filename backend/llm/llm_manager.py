"""
Draco AI - LLM / LLM Manager

Único módulo que o restante do Draco AI (brain.py, e no
futuro qualquer outro chamador) deve conhecer para gerar
respostas via LLM.

Responsabilidade:

    Decidir QUAL provedor de LLM utilizar, com base em
    LLM_MODE (backend/config.py), e delegar a geração da
    resposta para ele, seguindo sempre o contrato BaseLLM.

Fluxo:

    Prompt Builder
            |
            v
    llm_manager.generate(prompt, num_predict)
            |
            v
    LLM_MODE == "offline"  -> OllamaLLM
    LLM_MODE == "online"   -> GeminiLLM
            |
            v
        Resposta (str)

--------------------------------------------------------
Como adicionar um novo provedor no futuro
(OpenAI, Claude, DeepSeek, Grok, Mistral, LM Studio, etc)
--------------------------------------------------------

1. Criar backend/llm/<novo_provedor>_client.py implementando
   BaseLLM (generate() e available()), seguindo o mesmo
   padrão de ollama_client.py / gemini_client.py.

2. Registrar a nova classe no dicionário PROVIDERS abaixo,
   com uma nova chave de LLM_MODE (ex: "openai", "claude").

3. Nenhuma outra parte do sistema precisa ser alterada.
   brain.py, prompt_builder.py e todo o resto continuam
   chamando apenas llm_manager.generate(prompt).

--------------------------------------------------------
Fallback de segurança
--------------------------------------------------------

Se LLM_MODE apontar para um provedor indisponível (ex:
"online" sem GEMINI_API_KEY configurada), o llm_manager
faz fallback automático para o provedor "offline" (Ollama),
que é o padrão histórico do Draco AI e nunca deve deixar
de responder por falta de configuração externa.
"""

from backend.config import LLM_MODE

from backend.llm.ollama_client import OllamaLLM
from backend.llm.gemini_client import GeminiLLM


# =====================================
# Registro de provedores
# =====================================
#
# Chave: valor esperado de LLM_MODE
# Valor: classe do provedor (BaseLLM)
#
# Instanciados uma única vez, na carga do módulo, seguindo
# o mesmo padrão de instância global já usado no projeto
# (ex: rag_manager em backend/rag/rag_manager.py).
#

PROVIDERS = {

    "offline": OllamaLLM(),

    "online": GeminiLLM()

}


# Provedor usado quando LLM_MODE é desconhecido ou quando o
# provedor selecionado não está disponível no momento.
FALLBACK_MODE = "offline"


class LLMManager:
    """
    Fachada única de geração de texto via LLM.
    """

    def __init__(self, modo_padrao=None):

        self.modo_padrao = modo_padrao or LLM_MODE

    def _resolver_provider(self, modo):

        provider = PROVIDERS.get(modo)

        if provider is None:

            print(
                f"[LLMManager] LLM_MODE '{modo}' desconhecido. "
                f"Usando fallback '{FALLBACK_MODE}'."
            )

            return PROVIDERS[FALLBACK_MODE], FALLBACK_MODE

        if not provider.available():

            print(
                f"[LLMManager] Provedor '{modo}' indisponível "
                f"no momento. Usando fallback '{FALLBACK_MODE}'."
            )

            return PROVIDERS[FALLBACK_MODE], FALLBACK_MODE

        return provider, modo

    def generate(self, prompt: str, num_predict: int = 300) -> str:
        """
        Gera uma resposta utilizando o provedor configurado
        em LLM_MODE, com fallback automático para o modo
        offline caso o provedor escolhido esteja indisponível.
        """

        provider, modo_efetivo = self._resolver_provider(
            self.modo_padrao
        )

        print(
            f"[LLMManager] Gerando resposta via provedor "
            f"'{modo_efetivo}'."
        )

        return provider.generate(
            prompt,
            num_predict=num_predict
        )


# =====================================
# Instância global
# =====================================
#
# Mesmo padrão de rag_manager (backend/rag/rag_manager.py) e
# predictor (backend/intelligence/regression_predictor.py):
# um único ponto de entrada, pronto para uso, sem exigir que
# quem consome precise instanciar nada.
#

llm_manager = LLMManager()


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    resposta = llm_manager.generate(
        "Responda apenas: teste ok.",
        num_predict=20
    )

    print(resposta)
