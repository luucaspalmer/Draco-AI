def identificar_intencao(pergunta):

    texto = pergunta.lower()


        # =====================================
    # Proteção identidade básica
    # =====================================

    if (
        "seu nome" in texto
        or
        "teu nome" in texto
        or
        "como você se chama" in texto
        or
        "como voce se chama" in texto
    ):

        return "identidade_nome"



    # =====================================
    # Identidade - Nome do Draco
    # =====================================

    identidade_nome = [

    "quem é você",
    "quem e voce",
    "quem voce e",

    "qual seu nome",
    "qual é seu nome",
    "qual e seu nome",

    "diga seu nome",
    "me diga seu nome",

    "quem é o draco",
    "quem e o draco"
    ]


    for frase in identidade_nome:

        if frase in texto:

            return "identidade_nome"





    # =====================================
    # Identidade - Criador
    # =====================================

    identidade_criador = [

        "quem é seu criador",
        "quem e seu criador",

        "quem criou você",
        "quem criou voce",

        "quem fez você",
        "quem fez voce"
    ]


    for frase in identidade_criador:

        if frase in texto:

            return "identidade_criador"





    # =====================================
    # Identidade - Origem
    # =====================================

    identidade_origem = [

        "qual sua origem",

        "de onde você veio",
        "de onde voce veio"
    ]


    for frase in identidade_origem:

        if frase in texto:

            return "identidade_origem"





    # =====================================
    # Identidade - Propósito
    # =====================================

    identidade_proposito = [

        "qual seu propósito",
        "qual seu proposito",

        "qual sua função",
        "qual sua funcao"
    ]


    for frase in identidade_proposito:

        if frase in texto:

            return "identidade_proposito"





    # =====================================
    # Identidade - Missão
    # =====================================

    identidade_missao = [

        "qual sua missão",
        "qual sua missao",

        "qual sua missão de vida"
    ]


    for frase in identidade_missao:

        if frase in texto:

            return "identidade_missao"





    # =====================================
    # Identidade - Valores
    # =====================================

    identidade_valores = [

        "quais seus princípios",
        "quais seus principios",

        "quais seus valores"
    ]


    for frase in identidade_valores:

        if frase in texto:

            return "identidade_valores"





    # =====================================
    # Identidade - Capacidades
    # =====================================

    identidade_capacidades = [

        "o que você consegue fazer",
        "o que voce consegue fazer",

        "quais suas capacidades",

        "quais suas habilidades",

        "suas habilidades"
    ]


    for frase in identidade_capacidades:

        if frase in texto:

            return "identidade_capacidades"





    # =====================================
    # Consultar memória geral
    # =====================================

    perguntas_memoria = [

        "o que voce lembra",
        "o que você lembra",

        "mostre sua memoria",
        "mostre sua memória",

        "quais são minhas informações",
        "quais minhas informações"
    ]


    for frase in perguntas_memoria:

        if frase in texto:

            return "consultar_memoria"





    # =====================================
    # Consultar nome do usuário
    # =====================================

    perguntas_nome = [

        "qual meu nome",

        "qual é meu nome",
        "qual e meu nome",

        "voce sabe meu nome",
        "você sabe meu nome",

        "lembra meu nome"
    ]


    for frase in perguntas_nome:

        if frase in texto:

            return "consultar_nome"





    # =====================================
    # Esquecer memória
    # =====================================

    if (

        "esqueça meu nome" in texto

        or

        "esqueca meu nome" in texto

    ):

        return "esquecer_nome"





    # =====================================
    # Alterar estilo
    # =====================================

    if "altere meu estilo para" in texto:

        return "alterar_estilo"





    # =====================================
    # Nova memória - Projeto
    # =====================================

    projeto = [

        "estou criando",
        "estou desenvolvendo",
        "estou fazendo",

        "meu projeto é",
        "meu projeto e",

        "guarde meu projeto",
        "lembre do meu projeto",

        "memorize meu projeto"
    ]


    for frase in projeto:

        if frase in texto:

            return "memoria_projeto"





    # =====================================
    # Nova memória - Objetivo
    # =====================================

    objetivo = [

        "meu objetivo é",
        "meu objetivo e",

        "quero aprender",

        "quero estudar",

        "quero conseguir",

        "guarde meu objetivo",

        "lembre meu objetivo"
    ]


    for frase in objetivo:

        if frase in texto:

            return "memoria_objetivo"





    # =====================================
    # Nova memória - Conhecimento
    # =====================================

    conhecimento = [

        "estou estudando",

        "estou aprendendo",

        "tenho conhecimento em",

        "guarde que sei",

        "lembre que sei"
    ]


    for frase in conhecimento:

        if frase in texto:

            return "memoria_conhecimento"





    # =====================================
    # Memória de nome
    # =====================================

    palavras_nome = [

        "meu nome é",
        "meu nome e",

        "me chamo",

        "sou o"
    ]



    gatilhos_memoria = [

        "lembre",

        "guarde",

        "memorize",

        "anote",

        "salve",

        "não esqueça",

        "nao esqueça"
    ]



    possui_nome = False

    possui_memoria = False



    for palavra in palavras_nome:

        if palavra in texto:

            possui_nome = True





    for palavra in gatilhos_memoria:

        if palavra in texto:

            possui_memoria = True





    if possui_nome and possui_memoria:

        return "memoria_nome"





    # =====================================
    # Memória de preferência
    # =====================================

    preferencias = [

        "gosto de",

        "gosto de respostas",

        "prefiro",

        "minha preferência",

        "minha preferencia"
    ]



    for palavra in preferencias:

        if palavra in texto and possui_memoria:

            return "memoria_preferencia"





    # =====================================
    # Conversa normal
    # =====================================

    return "conversa"