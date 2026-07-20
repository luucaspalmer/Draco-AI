import json
import os
from datetime import datetime


from backend.memory.memory_types import MEMORY_TYPES
from backend.memory.memory_layers import MEMORY_LAYERS



# =====================================
# Caminho da memória
# =====================================

MEMORY_PATH = os.path.join(
    "backend",
    "memory"
)





# =====================================
# Arquivos de memória
# =====================================

ARQUIVOS_MEMORIA = {


    "PERMANENTE":
        "permanent_memory.json",


    "PROJETO":
        "project_memory.json",


    "PREFERENCIA":
        "preference_memory.json",


    "CONHECIMENTO":
        "knowledge_memory.json",


    "CONVERSA":
        "conversation_memory.json"

}







# =====================================
# Criar arquivos
# =====================================

def garantir_arquivos():


    if not os.path.exists(
        MEMORY_PATH
    ):

        os.makedirs(
            MEMORY_PATH
        )



    for arquivo in ARQUIVOS_MEMORIA.values():


        caminho = os.path.join(
            MEMORY_PATH,
            arquivo
        )



        if not os.path.exists(
            caminho
        ):


            with open(
                caminho,
                "w",
                encoding="utf-8"
            ) as f:


                json.dump(
                    {},
                    f,
                    indent=4,
                    ensure_ascii=False
                )









# =====================================
# Carregar camada
# =====================================

def carregar_camada(tipo):


    garantir_arquivos()



    arquivo = ARQUIVOS_MEMORIA.get(
        tipo
    )


    if not arquivo:

        return {}



    caminho = os.path.join(
        MEMORY_PATH,
        arquivo
    )



    try:

        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as f:


            return json.load(f)



    except json.JSONDecodeError:


        return {}









# =====================================
# Salvar camada
# =====================================

def salvar_camada(
    tipo,
    dados
):


    garantir_arquivos()



    arquivo = ARQUIVOS_MEMORIA.get(
        tipo
    )


    if not arquivo:

        return False



    caminho = os.path.join(
        MEMORY_PATH,
        arquivo
    )



    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )



    return True










# =====================================
# Criar registro cognitivo
# =====================================

def criar_registro(
    valor,
    importancia=5,
    confianca=1.0
):


    agora = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    registro = {

        "valor": valor,

        "importancia": importancia,

        "confianca": confianca,

        "criado_em": agora,

        "atualizado_em": agora

    }


    return registro










# =====================================
# Preparar valor cognitivo
# =====================================

def preparar_valor(
    valor
):


    if isinstance(
        valor,
        dict
    ):


        novo_valor = valor.get(
            "valor"
        )


        return {

            "valor": novo_valor,

            "origem": valor.get(
                "origem",
                "desconhecido"
            )

        }



    return {

        "valor": valor

    }











# =====================================
# Guardar memória
# =====================================

def guardar_memoria(
    tipo,
    chave,
    valor,
    importancia=5,
    confianca=1.0
):


    if tipo not in MEMORY_TYPES:

        return False



    memoria = carregar_camada(
        tipo
    )



    valor_processado = preparar_valor(
        valor
    )



    registro = criar_registro(
        valor_processado.get(
            "valor"
        ),
        importancia,
        confianca
    )



    # mantém origem quando existir

    if "origem" in valor_processado:


        registro["origem"] = valor_processado["origem"]






    if chave in memoria:


        registro["criado_em"] = memoria[chave].get(
            "criado_em",
            registro["criado_em"]
        )



        memoria[chave] = registro



    else:


        memoria[chave] = registro






    salvar_camada(
        tipo,
        memoria
    )



    return True











# =====================================
# Buscar memória
# =====================================

def buscar_memoria(
    tipo,
    chave=None
):


    memoria = carregar_camada(
        tipo
    )



    if chave:


        registro = memoria.get(
            chave
        )


        if registro:


            return registro.get(
                "valor"
            )



        return None



    return memoria










# =====================================
# Todas as memórias
# =====================================

def obter_todas_memorias():


    resultado = {}



    for tipo in ARQUIVOS_MEMORIA:


        resultado[tipo] = carregar_camada(
            tipo
        )



    return resultado










# =====================================
# Remover memória
# =====================================

def remover_memoria(
    tipo,
    chave
):


    memoria = carregar_camada(
        tipo
    )


    if chave in memoria:


        del memoria[chave]


        salvar_camada(
            tipo,
            memoria
        )


        return True



    return False










# =====================================
# Atualizar importância
# =====================================

def atualizar_importancia(
    tipo,
    chave,
    importancia
):


    memoria = carregar_camada(
        tipo
    )



    if chave not in memoria:

        return False




    memoria[chave]["importancia"] = importancia



    memoria[chave]["atualizado_em"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



    salvar_camada(
        tipo,
        memoria
    )


    return True



# =====================================
# Contexto cognitivo
# =====================================

def obter_memoria_contexto():

    contexto = {}

    for tipo in ARQUIVOS_MEMORIA:

        contexto[tipo] = carregar_camada(
            tipo
        )

    return contexto


# =====================================
# Compatibilidade - memória permanente
# =====================================

def buscar_memoria_permanente(
    chave=None
):

    return buscar_memoria(
        "PERMANENTE",
        chave
    )


    return contexto