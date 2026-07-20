"""
Draco AI
Context Manager

Responsável por decidir quais tipos de contexto
serão utilizados para responder uma pergunta.

Nesta primeira versão ele NÃO busca memórias,
NÃO consulta RAG e NÃO monta prompts.

Sua única responsabilidade é gerar um plano
de contexto para o cérebro do Draco.
"""


class ContextManager:

    def decidir_contexto(self, pergunta, intencao):

        pergunta = pergunta.lower().strip()

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

        return plano