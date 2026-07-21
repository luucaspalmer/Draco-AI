"""
Draco AI
Context Manager

Responsável por decidir quais tipos de contexto
serão utilizados para responder uma pergunta.

Agora também considera a rota cognitiva definida
pelo Question Router.
"""


class ContextManager:

    def decidir_contexto(
        self,
        pergunta,
        intencao,
        rota_pergunta=None
    ):

        pergunta = pergunta.lower().strip()

        rota = None

        if rota_pergunta:

            rota = rota_pergunta.get(
                "route"
            )

        plano = {

            # Identidade do Draco
            "usar_identidade": False,

            # Memórias do usuário
            "usar_memoria": False,

            # Projetos conhecidos
            "usar_projetos": False,

            # Personalidade do Draco
            "usar_personalidade": True,

            # Histórico recente da conversa
            "usar_conversa": True,

            # Base de conhecimento (RAG)
            "usar_rag": False,

            # Motivo da decisão
            "motivo": "Contexto padrão"

        }

        # =====================================
        # Intenções relacionadas à identidade
        # =====================================

        if intencao.startswith("identidade_"):

            plano["usar_identidade"] = True
            plano["usar_conversa"] = False
            plano["motivo"] = "Consulta de identidade"

            return plano

        # =====================================
        # Intenções relacionadas à memória
        # =====================================

        if intencao.startswith("memoria_"):

            plano["usar_memoria"] = True
            plano["motivo"] = "Consulta de memória"

            return plano

        # =====================================
        # Consulta sobre o usuário
        # =====================================

        usuario_keywords = [

            "quem sou eu",

            "o que sabe sobre mim",

            "o que você sabe sobre mim",

            "me conhece",

            "fale sobre mim",

            "me fale sobre mim"

        ]

        if any(k in pergunta for k in usuario_keywords):

            plano["usar_memoria"] = True
            plano["motivo"] = "Consulta sobre o usuário"

        # =====================================
        # Projeto Draco
        # =====================================

        projeto_keywords = [

            "draco",

            "projeto",

            "backend",

            "frontend",

            "python",

            "codigo",

            "código",

            "ollama",

            "qwen",

            "memoria",

            "memória",

            "rag"

        ]

        if any(k in pergunta for k in projeto_keywords):

            plano["usar_projetos"] = True
            plano["motivo"] = "Consulta sobre projeto"

        # =====================================
        # Conhecimento externo
        # =====================================

        conhecimento_keywords = [

            "explique",

            "como funciona",

            "o que é",

            "defina",

            "conceito",

            "história",

            "historia"

        ]

        if any(k in pergunta for k in conhecimento_keywords):

            plano["usar_rag"] = True
            plano["motivo"] = "Consulta de conhecimento"

        # =====================================
        # Ajustes baseados no Question Router
        # =====================================

        if rota == "identity":

            plano["usar_identidade"] = True

            plano["motivo"] = "Question Router → Identidade"

        elif rota == "knowledge":

            plano["usar_rag"] = True

            plano["motivo"] = "Question Router → Conhecimento"

        elif rota == "graph":

            plano["usar_memoria"] = True

            plano["motivo"] = "Question Router → Grafo de Memória"

        elif rota == "rag":

            plano["usar_rag"] = True

            plano["motivo"] = "Question Router → RAG"

        elif rota == "memory":

            plano["usar_memoria"] = True

            plano["motivo"] = "Question Router → Memória"

        elif rota == "time":

            plano["usar_rag"] = True

            plano["motivo"] = "Question Router → Tempo"

        return plano