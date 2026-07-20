import os



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
# Memória antiga
# Compatibilidade temporária
# =====================================

MEMORY_FILE = os.path.join(
    DATA_DIR,
    "memory.json"
)


PERSONALITY_FILE = os.path.join(
    DATA_DIR,
    "personality_memory.json"
)







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



CONVERSATION_MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "conversation_memory.json"
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