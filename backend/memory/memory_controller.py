"""
Draco AI - Memory Controller

Responsável pelo ciclo de aprendizado
da memória cognitiva.

Detector
    ↓
Validator
    ↓
Controller
    ↓
Memory Manager
    ↓
JSON
"""


import re


from backend.memory.memory_extractor import extrair_memorias

from backend.memory.memory_detector import detectar_memoria

from backend.memory.memory_validator import validar_memorias

from backend.memory.memory_manager import guardar_memoria





# =====================================
# Mapeamento cognitivo
# =====================================

def identificar_tipo_memoria(campo):


    mapa = {


        "nome":
            "PERMANENTE",


        "idade":
            "PERMANENTE",


        "profissao":
            "PERMANENTE",


        "localizacao":
            "PERMANENTE",


        "caracteristicas":
            "PERMANENTE",


        "objetivos":
            "PROJETO",


        "relacionamentos":
            "PERMANENTE",


        "projetos":
            "PROJETO",


        "interesses":
            "CONHECIMENTO",


        "preferencias":
            "PREFERENCIA",


        "outras_memorias":
            "CONHECIMENTO"


    }


    return mapa.get(
        campo
    )





# =====================================
# Normalizar chave
# =====================================

def normalizar_chave(texto):


    texto = str(texto).lower()



    texto = re.sub(
        r"[^a-z0-9áéíóúãõç\s]",
        "",
        texto
    )



    texto = texto.strip()



    texto = texto.replace(
        " ",
        "_"
    )


    return texto





# =====================================
# Criar chave cognitiva
# =====================================

def criar_chave(
    campo,
    valor
):


    prefixo = campo



    if campo.endswith("s"):

        prefixo = campo[:-1]



    return (

        prefixo

        + "_"

        + normalizar_chave(valor)

    )





# =====================================
# Validar valor
# =====================================

def valor_valido(valor):


    if valor is None:

        return False



    if isinstance(valor,str):

        if not valor.strip():

            return False



    if isinstance(valor,list):

        if len(valor) == 0:

            return False



    return True





# =====================================
# Guardar memória
# =====================================

def guardar_item(

    campo,

    valor,

    importancia=5,

    confianca=1.0

):


    tipo = identificar_tipo_memoria(
        campo
    )


    if not tipo:

        return False



    if not valor_valido(valor):

        return False





    # Valores únicos
    if isinstance(valor,str):


        guardar_memoria(

            tipo,

            campo,

            {

                "valor": valor,

                "origem": "usuario"

            },

            importancia,

            confianca

        )


        return True





    # Listas
    if isinstance(valor,list):


        for item in valor:


            if not valor_valido(item):

                continue



            chave = criar_chave(

                campo,

                item

            )



            guardar_memoria(

                tipo,

                chave,

                {

                    "valor": item,

                    "origem": "usuario"

                },

                importancia,

                confianca

            )


        return True




    return False






# =====================================
# Processar memória
# =====================================

def processar_memoria(
    texto
):


    memoria_detectada = detectar_memoria(
        texto
    )



    # fallback IA
    if not memoria_detectada:


        memoria_detectada = extrair_memorias(
            texto
        )




    if not memoria_detectada:

        return {

            "processado": False,

            "alteracoes": [],

            "memorias": {}

        }




    memoria_validada = validar_memorias(
        memoria_detectada
    )



    alteracoes = []





    for campo, valor in memoria_validada.items():



        if not valor_valido(valor):

            continue





        tipo = identificar_tipo_memoria(
            campo
        )



        if not tipo:

            continue





        importancia = 5

        confianca = 1.0






        # =================================
        # Texto simples
        # =================================

        if isinstance(
            valor,
            str
        ):



            if guardar_item(

                campo,

                valor,

                importancia,

                confianca

            ):


                alteracoes.append(
                    campo
                )







        # =================================
        # Lista
        # =================================

        elif isinstance(
            valor,
            list
        ):



            for item in valor:



                if not valor_valido(item):

                    continue




                chave = criar_chave(

                    campo,

                    item

                )



                guardar_memoria(

                    tipo,

                    chave,

                    {

                        "valor": item,

                        "origem": "usuario"

                    },

                    importancia,

                    confianca

                )



                alteracoes.append(
                    chave
                )







        # =================================
        # Estrutura do extractor
        # =================================

        elif isinstance(
            valor,
            dict
        ):



            item_valor = valor.get(
                "valor"
            )



            if not valor_valido(
                item_valor
            ):

                continue




            guardar_memoria(

                tipo,

                campo,

                valor,

                valor.get(
                    "importancia",
                    importancia
                ),

                valor.get(
                    "confianca",
                    0.8
                )

            )



            alteracoes.append(
                campo
            )






    return {


        "processado":

            True,


        "alteracoes":

            alteracoes,


        "memorias":

            memoria_validada


    }