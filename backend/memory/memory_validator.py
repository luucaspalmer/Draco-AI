"""
Draco AI - Memory Validator

Responsável por validar e padronizar
memórias recebidas.

Aceita:

1 - Memory Detector
2 - Memory Extractor

Retorna sempre o formato cognitivo:
{
    valor,
    origem,
    confianca,
    importancia
}
"""


import copy





# =====================================
# Configuração das memórias
# =====================================


IMPORTANCIAS = {


    "nome":
        10,


    "idade":
        9,


    "profissao":
        8,


    "localizacao":
        8,


    "caracteristicas":
        7,


    "projetos":
        8,


    "interesses":
        6,


    "preferencias":
        6,


    "objetivos":
        7,


    "relacionamentos":
        7,


    "outras_memorias":
        5

}







CONFIANCAS = {


    "usuario":
        1.0,


    "inferido":
        0.6

}








# =====================================
# Campos aceitos
# =====================================


CAMPOS_MEMORIA = [

    "nome",

    "idade",

    "profissao",

    "localizacao",

    "caracteristicas",

    "interesses",

    "projetos",

    "preferencias",

    "objetivos",

    "relacionamentos",

    "outras_memorias"

]








# =====================================
# Criar registro
# =====================================


def criar_registro(

    valor,

    origem="usuario",

    confianca=None,

    importancia=None

):


    if confianca is None:

        confianca = CONFIANCAS.get(

            origem,

            0.5

        )



    if importancia is None:

        importancia = 5





    return {


        "valor":

            valor,


        "origem":

            origem,


        "confianca":

            confianca,


        "importancia":

            importancia

    }









# =====================================
# Validar memória
# =====================================


def validar_memorias(
    memorias: dict
):


    resultado = {}




    if not isinstance(
        memorias,
        dict
    ):

        return resultado








    for campo in CAMPOS_MEMORIA:



        if campo not in memorias:

            continue





        valor = memorias.get(
            campo
        )



        if valor is None:

            continue







        importancia_padrao = IMPORTANCIAS.get(

            campo,

            5

        )







        # =================================
        # Estrutura do Extractor IA
        # =================================


        if isinstance(
            valor,
            dict
        ):



            if "valor" in valor:



                resultado[campo] = criar_registro(


                    valor.get(
                        "valor"
                    ),


                    valor.get(
                        "origem",
                        "usuario"
                    ),


                    valor.get(
                        "confianca"
                    ),


                    valor.get(
                        "importancia",
                        importancia_padrao
                    )


                )


                continue







        # =================================
        # Texto simples
        # =================================


        if isinstance(
            valor,
            str
        ):



            valor = valor.strip()




            if valor:



                resultado[campo] = criar_registro(


                    valor,


                    "usuario",


                    1.0,


                    importancia_padrao


                )









        # =================================
        # Lista
        # =================================


        elif isinstance(
            valor,
            list
        ):



            itens = []




            for item in valor:



                if isinstance(
                    item,
                    str
                ):



                    item = item.strip()




                    if item and item not in itens:

                        itens.append(
                            item
                        )







            if itens:



                resultado[campo] = criar_registro(


                    itens,


                    "usuario",


                    0.9,


                    importancia_padrao


                )







    return resultado