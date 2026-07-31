import os

from dotenv import load_dotenv



# =====================================
# Carregamento do .env
# =====================================
#
# Precisa acontecer ANTES de qualquer os.environ.get()
# deste arquivo (LLM_MODE, GEMINI_API_KEY, GEMINI_MODEL
# mais abaixo).
#
# Este é o ÚNICO ponto do projeto que chama load_dotenv().
# Como config.py é importado por praticamente todo o
# restante do sistema e o Python só executa o corpo de um
# módulo uma vez por processo (cache de import), isso
# garante o carregamento do .env exatamente uma vez, sem
# depender de main.py, scripts avulsos ou testes se
# lembrarem de chamar load_dotenv() manualmente.
#
# O caminho é resolvido a partir da posição deste arquivo
# (backend/config.py -> raiz do projeto), e não do
# diretório de onde o Python foi executado (CWD), para que
# o .env seja encontrado independente de onde o comando é
# rodado.

_DOTENV_PATH = os.path.join(

    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),

    ".env"

)


load_dotenv(_DOTENV_PATH)



# =====================================
# Identidade do Draco
# =====================================

DRACO_NAME = "Draco"





# =====================================
# Modelo de inteligência
# =====================================

OLLAMA_MODEL = "qwen2.5:3b"





# =====================================
# Caminhos principais
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)





# =====================================
# Diretório de dados
# =====================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)



if not os.path.exists(DATA_DIR):

    os.makedirs(DATA_DIR)





# =====================================
# Memória hierárquica Draco AI
# =====================================

MEMORY_DIR = os.path.join(
    BASE_DIR,
    "backend",
    "memory"
)



PERMANENT_MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "permanent_memory.json"
)



PROJECT_MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "project_memory.json"
)



PREFERENCE_MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "preference_memory.json"
)



KNOWLEDGE_MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "knowledge_memory.json"
)



CHAT_HISTORY_FILE = os.path.join(
    DATA_DIR,
    "chat_history.json"
)







# =====================================
# Conversação
# =====================================

MAX_HISTORY = 10





# =====================================
# Controle de memória
# =====================================

# quantidade máxima de informações
# enviadas ao contexto do Qwen

MAX_MEMORY_CONTEXT = 20



# confiança mínima para usar memória

MEMORY_CONFIDENCE_THRESHOLD = 0.50





# =====================================
# Provedor de LLM
# =====================================
#
# Controla qual provedor de LLM o Draco AI utiliza para
# gerar respostas (backend/llm/llm_manager.py).
#
# Valores possíveis hoje:
#
#   "offline"  -> Ollama (padrão, comportamento histórico)
#   "online"   -> Gemini
#
# Futuramente também poderá aceitar:
#
#   "auto", "openai", "claude", "deepseek", etc.
#
# Lido de variável de ambiente para permitir alternar o
# provedor sem alterar código. Se a variável não estiver
# definida, o padrão continua sendo "offline", preservando
# 100% do comportamento atual do Draco AI.

LLM_MODE = os.environ.get(
    "LLM_MODE",
    "online"
)



# =====================================
# Provedor Online - Gemini
# =====================================
#
# Usadas exclusivamente por backend/llm/gemini_client.py.
# Nenhum valor sensível fica hardcoded no código-fonte.

GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY"
)


GEMINI_MODEL = os.environ.get(
    "GEMINI_MODEL",
    "gemini-flash-latest"
)