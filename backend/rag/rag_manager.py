"""
=====================================
Draco AI
RAG Manager
=====================================

Camada responsável por orquestrar
todo o sistema RAG.

O restante do Draco nunca deve acessar
retriever, vector_store ou embeddings
diretamente.

Fluxo:

Context Builder
        ↓
RAG Manager
        ↓
Retriever
        ↓
ChromaDB
"""

from backend.rag.rag_context import (
    construir_contexto_rag
)


class RAGManager:
    """
    Gerencia todas as operações
    relacionadas ao RAG.
    """

    def __init__(self):

        self.ativo = True


    def buscar_contexto(
        self,
        pergunta,
        limite=3
    ):
        """
        Retorna o contexto recuperado
        da base vetorial.
        """

        if not self.ativo:

            return ""

        return construir_contexto_rag(
            pergunta,
            limite
        )


    def ativar(self):

        self.ativo = True


    def desativar(self):

        self.ativo = False


    def status(self):

        return self.ativo


# =====================================
# Instância global
# =====================================

rag_manager = RAGManager()


# =====================================
# Teste
# =====================================

if __name__ == "__main__":

    pergunta = "O que é o Projeto Eclipse?"

    contexto = rag_manager.buscar_contexto(
        pergunta
    )

    print(contexto)