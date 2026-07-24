"""
Draco AI
Response Planner

Responsável por decidir o ESTILO da resposta
antes da construção do prompt.

Fluxo:

question_analyzer
        |
        ↓
entity_resolver / entity_classifier
        |
        ↓
question_router
        |
        ↓
response_planner   <-- este módulo
        |
        ↓
context_manager / context_builder
        |
        ↓
prompt_builder
        |
        ↓
ollama_client


Filosofia:

Resposta curta é a REGRA.
Resposta longa é a EXCEÇÃO.

Este módulo é 100% baseado em regras determinísticas,
sem chamadas ao Qwen, para não adicionar latência
extra ao pipeline.
"""


# =====================================
# Estilos de resposta disponíveis
# =====================================

ESTILOS = {


    "DIRETA": {

        "num_predict": 60,

        "instrucao": (
            "Responda em UMA frase curta e direta. "
            "Vá direto ao ponto. "
            "Não adicione contexto, explicações ou informações "
            "que não foram solicitadas. "
            "Não elabore além do necessário."
        )

    },


    "EXPLICATIVA": {

        "num_predict": 220,

        "instrucao": (
            "Responda em um parágrafo curto, entre 2 e 4 frases. "
            "Vá direto ao ponto principal antes de complementar. "
            "Evite alongar o assunto além do necessário para "
            "responder à pergunta."
        )

    },


    "APROFUNDADA": {

        "num_predict": 700,

        "instrucao": (
            "O usuário pediu uma explicação detalhada. "
            "Você pode explicar em profundidade, estruturar "
            "por tópicos e usar exemplos quando fizer sentido."
        )

    }

}



# =====================================
# Tipos de pergunta que indicam
# busca factual pontual
# =====================================

QUESTION_TYPES_DIRETOS = (

    "person",

    "time",

    "location",

    "owner",

    "quantity"

)



# =====================================
# Tipos de pergunta que normalmente
# pedem uma explicação curta
# =====================================

QUESTION_TYPES_EXPLICATIVOS = (

    "definition",

    "reason",

    "event"

)



# =====================================
# Intenções que sempre geram
# respostas diretas
# =====================================

INTENTS_DIRETOS = (

    "identidade_nome",

    "identidade_criador",

    "identidade_origem",

    "identidade_proposito",

    "consultar_nome",

    "consultar_memoria",

    "memoria_nome",

    "memoria_projeto",

    "memoria_objetivo",

    "memoria_preferencia",

    "memoria_conhecimento"

)



# =====================================
# Intenções que naturalmente pedem
# uma explicação um pouco maior
# =====================================

INTENTS_EXPLICATIVOS = (

    "identidade_missao",

    "identidade_valores",

    "identidade_capacidades",

    "identidade_arquitetura"

)



# =====================================
# Gatilhos explícitos de aprofundamento
# =====================================

PALAVRAS_APROFUNDAR = (

    "detalhadamente",

    "com detalhes",

    "em detalhes",

    "detalhe",

    "aprofunde",

    "aprofundada",

    "explique a fundo",

    "passo a passo",

    "em profundidade",

    "elabore",

    "escreva um texto",

    "escreva sobre",

    "me explique tudo",

    "quero entender completamente"

)



# =====================================
# Normalização simples
# =====================================

def normalizar(texto):

    if not texto:

        return ""

    return texto.lower().strip()



# =====================================
# Detectar pedido explícito de detalhe
# =====================================

def pedido_de_aprofundamento(texto):

    texto = normalizar(texto)

    for palavra in PALAVRAS_APROFUNDAR:

        if palavra in texto:

            return True

    return False



# =====================================
# Escolher estilo
# =====================================

def escolher_estilo(
    pergunta,
    dados_pergunta=None,
    rota_pergunta=None
):

    dados_pergunta = dados_pergunta or {}

    rota_pergunta = rota_pergunta or {}


    intent = dados_pergunta.get(
        "intent",
        rota_pergunta.get("intent")
    )


    question_type = dados_pergunta.get(
        "question_type",
        rota_pergunta.get("question_type")
    )



    # =================================
    # PRIORIDADE 1
    # Pedido explícito de aprofundamento
    # =================================

    if pedido_de_aprofundamento(pergunta):

        return "APROFUNDADA"



    # =================================
    # PRIORIDADE 2
    # Intenções diretas conhecidas
    # =================================

    if intent in INTENTS_DIRETOS:

        return "DIRETA"



    if intent in INTENTS_EXPLICATIVOS:

        return "EXPLICATIVA"



    # =================================
    # PRIORIDADE 3
    # Tipo da pergunta
    # =================================

    if question_type in QUESTION_TYPES_DIRETOS:

        return "DIRETA"


    if question_type in QUESTION_TYPES_EXPLICATIVOS:

        return "EXPLICATIVA"



    # =================================
    # PADRÃO
    #
    # Resposta curta é a regra.
    # =================================

    return "DIRETA"



# =====================================
# Planejar resposta
# =====================================

def planejar_resposta(
    pergunta,
    dados_pergunta=None,
    rota_pergunta=None
):
    """
    Retorna o plano de resposta:

    {
        "estilo": "DIRETA" | "EXPLICATIVA" | "APROFUNDADA",
        "num_predict": int,
        "instrucao_estilo": str
    }
    """

    estilo = escolher_estilo(
        pergunta,
        dados_pergunta,
        rota_pergunta
    )


    config = ESTILOS[estilo]


    return {

        "estilo": estilo,

        "num_predict": config["num_predict"],

        "instrucao_estilo": config["instrucao"]

    }



# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":


    exemplos = [

        {
            "pergunta": "Qual é meu nome?",
            "dados": {"intent": "consultar_nome", "question_type": "unknown"}
        },

        {
            "pergunta": "Quem criou você?",
            "dados": {"intent": "identidade_criador", "question_type": "unknown"}
        },

        {
            "pergunta": "Explique detalhadamente como funciona o RAG.",
            "dados": {"intent": "conversa", "question_type": "definition"}
        },

        {
            "pergunta": "O que é inteligência artificial?",
            "dados": {"intent": "conversa", "question_type": "definition"}
        }

    ]


    for exemplo in exemplos:


        plano = planejar_resposta(

            exemplo["pergunta"],

            exemplo["dados"]

        )


        print("\nPergunta:", exemplo["pergunta"])

        print("Plano:", plano)
