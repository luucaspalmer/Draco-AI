from backend.memory.memory_manager import (
    buscar_memoria_permanente
)


from backend.memory.memory_controller import (
    processar_memoria
)


from backend.memory.memory_search import (
    buscar_memorias
)





# =====================================
# Identidade do Draco
# =====================================


def consultar_identidade():

    from backend.identity import get_identity


    identidade = get_identity()


    return (
        f"Meu nome é {identidade['nome']}. "
        f"Sou um {identidade['arquétipo']}. "
        f"Fui criado por {identidade['criador']['nome']}, "
        f"que atua como {identidade['criador']['papel']}. "
        f"Meu propósito é {identidade['propósito']}"
    )





def consultar_nome_draco():

    from backend.identity import get_identity


    identidade = get_identity()


    return (
        f"Meu nome é {identidade['nome']}. "
        f"Sou um {identidade['arquétipo']}."
    )





def consultar_criador():

    from backend.identity import get_identity


    criador = get_identity("criador")


    return (
        f"Meu criador é {criador['nome']}. "
        f"Ele atua como {criador['papel']}."
    )





def consultar_origem():

    from backend.identity import get_identity


    origem = get_identity("origem")


    return (
        f"Minha origem está ligada ao projeto {origem['projeto']}. "
        f"{origem['objetivo_inicial']}"
    )





def consultar_proposito():

    from backend.identity import get_identity


    return (
        f"Meu propósito é: "
        f"{get_identity('propósito')}"
    )





def consultar_missao():

    from backend.identity import get_identity


    missao = get_identity("missão")


    resposta = "Minha missão é:\n"


    for item in missao:

        resposta += f"- {item}\n"


    return resposta





def consultar_valores():

    from backend.identity import get_identity


    valores = get_identity("valores")


    resposta = "Meus valores são:\n"


    for item in valores:

        resposta += f"- {item}\n"


    return resposta





def consultar_capacidades():

    from backend.identity import get_identity


    capacidades = get_identity("capacidades")


    resposta = "Minhas capacidades incluem:\n"


    for item in capacidades:

        resposta += f"- {item}\n"


    return resposta





def consultar_arquitetura():

    from backend.identity import get_identity


    arquitetura = get_identity("arquitetura")


    resposta = (

        f"Minha arquitetura utiliza: "
        f"{arquitetura['modelo']}.\n\n"

        f"Minha infraestrutura: "
        f"{arquitetura['infraestrutura']}\n\n"

        "Meus principais componentes são:\n"

    )


    for componente in arquitetura["componentes"]:

        resposta += f"- {componente}\n"


    resposta += "\nMeu fluxo de processamento:\n"


    for etapa in arquitetura["fluxo_processamento"]:

        resposta += f"- {etapa}\n"


    return resposta





# =====================================
# Memórias hierárquicas
# =====================================


def salvar_nome(pergunta):


    formatos = [

        "meu nome é",

        "meu nome e"

    ]


    pergunta_normalizada = pergunta.lower()


    for formato in formatos:


        if formato in pergunta_normalizada:


            partes = pergunta.split(
                formato,
                1
            )


            if len(partes) > 1:


                nome = (

                    partes[1]

                    .replace(".", "")

                    .strip()

                )


                if nome:


                    processar_memoria({

                        "tipo": "permanente",

                        "chave": "nome",

                        "valor": nome

                    })


                    return (

                        f"Entendido. Registrei seu nome como {nome}."

                    )


    return None


# =====================================
# Salvar projeto
# =====================================


def salvar_projeto(pergunta):


    texto = pergunta.lower()


    for gatilho in [

        "meu projeto é",

        "meu projeto e",

        "guarde meu projeto",

        "lembre do meu projeto"

    ]:


        if gatilho in texto:


            projeto = (

                texto

                .split(gatilho)[1]

                .strip()

            )


            if projeto:


                processar_memoria({

                    "tipo": "projeto",

                    "valor": projeto

                })


                return (

                    f"Entendido. Registrei seu projeto: {projeto}."

                )


    return None







# =====================================
# Salvar conhecimento
# =====================================


def salvar_conhecimento(pergunta):


    texto = pergunta.lower()


    for gatilho in [

        "estou estudando",

        "estou aprendendo",

        "tenho conhecimento em"

    ]:


        if gatilho in texto:


            conhecimento = (

                texto

                .split(gatilho)[1]

                .strip()

            )


            if conhecimento:


                processar_memoria({

                    "tipo": "conhecimento",

                    "valor": conhecimento

                })


                return (

                    f"Entendido. Registrei esse conhecimento: {conhecimento}."

                )


    return None







# =====================================
# Salvar preferência
# =====================================


def salvar_preferencia(pergunta):


    texto = pergunta.lower()


    for gatilho in [

        "prefiro",

        "gosto de",

        "quero respostas"

    ]:


        if gatilho in texto:


            preferencia = (

                texto

                .split(gatilho)[1]

                .strip()

            )


            if preferencia:


                processar_memoria({

                    "tipo": "preferencia",

                    "categoria": "resposta",

                    "chave": "estilo",

                    "valor": preferencia

                })


                return (

                    f"Entendido. Vou lembrar sua preferência: {preferencia}."

                )


    return None







# =====================================
# Consultar memória
# =====================================


def consultar_memoria(pergunta):


    resultado = buscar_memorias(

        pergunta

    )


    if not resultado:


        return (

            "Não encontrei informações relacionadas "

            "na minha memória."

        )



    memoria = resultado.get(

        "memoria",

        {}

    )


    resposta = ""



    for categoria, dados in memoria.items():


        resposta += f"\n{categoria.upper()}:\n"



        if isinstance(dados, dict):


            for chave, valor in dados.items():

                resposta += (

                    f"- {chave}: {valor}\n"

                )


        elif isinstance(dados, list):


            for item in dados:

                resposta += (

                    f"- {item}\n"

                )


        else:


            resposta += (

                f"- {dados}\n"

            )


    return resposta







# =====================================
# Consultar nome
# =====================================

def consultar_nome():

    nome = buscar_memoria_permanente(
        "nome"
    )


    if nome:

        return (
            f"Seu nome é {nome}."
        )


    return (
        "Ainda não tenho seu nome registrado."
    )



# =====================================
# Alterar estilo
# =====================================


def alterar_estilo(pergunta):


    texto = pergunta.lower()


    comando = "altere meu estilo para"



    if comando in texto:


        estilo = (

            texto

            .split(comando)[1]

            .strip()

        )


        processar_memoria({

            "tipo": "preferencia",

            "categoria": "resposta",

            "chave": "estilo",

            "valor": estilo

        })


        return (

            f"Entendido. Meu estilo agora será {estilo}."

        )


    return None







# =====================================
# Executor principal
# =====================================


def executar_comando(intencao, pergunta):


    if intencao == "identidade_nome":

        return consultar_nome_draco()



    if intencao == "identidade_criador":

        return consultar_criador()



    if intencao == "identidade_origem":

        return consultar_origem()



    if intencao == "identidade_proposito":

        return consultar_proposito()



    if intencao == "identidade_missao":

        return consultar_missao()



    if intencao == "identidade_valores":

        return consultar_valores()



    if intencao == "identidade_capacidades":

        return consultar_capacidades()



    if intencao == "identidade_arquitetura":

        return consultar_arquitetura()





    if intencao == "memoria_nome":

        return salvar_nome(pergunta)



    if intencao == "memoria_projeto":

        return salvar_projeto(pergunta)



    if intencao == "memoria_conhecimento":

        return salvar_conhecimento(pergunta)



    if intencao == "memoria_preferencia":

        return salvar_preferencia(pergunta)



    if intencao == "consultar_memoria":

        return consultar_memoria(pergunta)



    if intencao == "consultar_nome":

        return consultar_nome()



    if intencao == "alterar_estilo":

        return alterar_estilo(pergunta)



    return None