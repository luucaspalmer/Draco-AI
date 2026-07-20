"""
Draco AI - Memory Graph

Sistema de relações entre memórias.

Transforma memórias isoladas em conhecimento conectado.

Exemplo:

Lucas
 |
 criou
 |
Draco AI

"""

import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")

GRAPH_FILE = os.path.join(
    DATA_DIR,
    "memory_graph.json"
)


# =====================================
# Carregar grafo
# =====================================

def carregar_grafo():

    if not os.path.exists(GRAPH_FILE):
        return {
            "entidades": {},
            "relacoes": []
        }

    with open(
        GRAPH_FILE,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)



# =====================================
# Salvar grafo
# =====================================

def salvar_grafo(grafo):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        GRAPH_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            grafo,
            arquivo,
            indent=4,
            ensure_ascii=False
        )



# =====================================
# Criar entidade
# =====================================

def adicionar_entidade(
        nome,
        tipo
):

    grafo = carregar_grafo()


    if nome not in grafo["entidades"]:

        grafo["entidades"][nome] = {

            "tipo": tipo,

            "criado_em":
                datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
        }


    salvar_grafo(grafo)



# =====================================
# Criar relação
# =====================================

def adicionar_relacao(
        origem,
        relacao,
        destino
):

    grafo = carregar_grafo()


    nova_relacao = {

        "origem": origem,

        "relacao": relacao,

        "destino": destino,

        "criado_em":
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")

    }


    if nova_relacao not in grafo["relacoes"]:

        grafo["relacoes"].append(
            nova_relacao
        )


    salvar_grafo(grafo)



# =====================================
# Buscar relações
# =====================================

def buscar_relacoes(entidade):

    grafo = carregar_grafo()


    resultado = []


    for relacao in grafo["relacoes"]:


        if (
            relacao["origem"] == entidade
            or
            relacao["destino"] == entidade
        ):

            resultado.append(
                relacao
            )


    return resultado



# =====================================
# Criar conhecimento inicial Draco
# =====================================

def criar_base_draco():


    adicionar_entidade(
        "Lucas",
        "pessoa"
    )


    adicionar_entidade(
        "Draco AI",
        "projeto"
    )


    adicionar_entidade(
        "Memória Cognitiva",
        "funcionalidade"
    )


    adicionar_relacao(
        "Lucas",
        "criador",
        "Draco AI"
    )


    adicionar_relacao(
        "Draco AI",
        "objetivo",
        "IA pessoal cognitiva"
    )


    adicionar_relacao(
        "Draco AI",
        "desenvolvimento_atual",
        "Memória Cognitiva"
    )


# =====================================
# Listar entidades conhecidas
# =====================================

def listar_entidades():

    grafo = carregar_grafo()

    return list(
        grafo["entidades"].keys()
    )



if __name__ == "__main__":

    criar_base_draco()

    print(
        "Grafo cognitivo criado."
    )