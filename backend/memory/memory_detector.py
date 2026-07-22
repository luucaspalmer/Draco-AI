"""
Draco AI - Memory Detector

Responsável por detectar informações simples
sobre o usuário antes do processamento com IA.

Não grava memória.
Não altera arquivos.

Apenas identifica e limpa padrões.
"""


import re



# =====================================
# Criar memória limpa
# =====================================

def criar_memoria():

    return {

        "nome": None,

        "idade": None,

        "profissao": None,

        "localizacao": None,

        "interesses": [],

        "projetos": [],

        "preferencias": [],

        "objetivos": [],

        "relacionamentos": [],

        "caracteristicas": [],

        "outras_memorias": []

    }



# =====================================
# Limpeza geral
# =====================================

def limpar_texto(valor):


    if not isinstance(valor, str):

        return valor


    valor = valor.strip()


    valor = re.sub(
        r"[.!?,;]+$",
        "",
        valor
    )


    return valor.strip()



# =====================================
# Limpar captura
# =====================================

def limpar_captura(valor):


    if not valor:

        return None


    valor = valor.strip()


    cortes = [

        " tenho ",
        " moro ",
        " moro em ",
        " estou ",
        " estudo ",
        " gosto ",
        " e moro ",
        " e tenho "

    ]


    texto_lower = valor.lower()


    for corte in cortes:

        posicao = texto_lower.find(corte)


        if posicao > 0:

            valor = valor[:posicao]

            break


    return limpar_texto(valor)



# =====================================
# Detectar nome
# =====================================

def detectar_nome(texto, memoria):


    padroes = [

        r"meu nome é ([^.!,]+)",

        r"meu nome e ([^.!,]+)",

        r"me chamo ([^.!,]+)"

    ]


    for padrao in padroes:


        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE
        )


        if resultado:


            nome = limpar_captura(
                resultado.group(1)
            )


            if nome:

                memoria["nome"] = nome

                return



    # ==============================
    # Caso "sou Lucas"
    # ==============================


    resultado = re.search(

        r"\bsou\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)\b",

        texto

    )


    if resultado:


        nome = resultado.group(1)


        palavras_invalidas = [

            "Uma",
            "Um",
            "Muito",
            "Feliz",
            "Triste",
            "Simpática",
            "Simpatica"

        ]


        if nome not in palavras_invalidas:

            memoria["nome"] = nome



# =====================================
# Detectar idade
# =====================================

def detectar_idade(texto, memoria):


    resultado = re.search(

        r"tenho\s+(\d+)\s+anos",

        texto,

        re.IGNORECASE

    )


    if resultado:

        memoria["idade"] = resultado.group(1)



# =====================================
# Detectar localização
# =====================================

def detectar_localizacao(texto, memoria):


    padroes = [

        r"moro em ([^.!,]+)",

        r"sou de ([^.!,]+)",

        r"vivo em ([^.!,]+)"

    ]


    for padrao in padroes:


        resultado = re.search(

            padrao,

            texto,

            re.IGNORECASE

        )


        if resultado:


            memoria["localizacao"] = limpar_texto(

                resultado.group(1)

            )


            return



# =====================================
# Detectar características pessoais
# =====================================

def detectar_caracteristicas(texto, memoria):


    padroes = [

        r"sou uma pessoa ([^.!,]+)",

        r"eu sou uma pessoa ([^.!,]+)",

        r"sou muito ([^.!,]+)",

        r"eu sou muito ([^.!,]+)"

    ]


    for padrao in padroes:


        resultado = re.search(

            padrao,

            texto,

            re.IGNORECASE

        )


        if resultado:


            caracteristica = limpar_texto(

                resultado.group(1)

            )


            if caracteristica:

                memoria["caracteristicas"].append(
                    caracteristica
                )



# =====================================
# Limpar interesse
# =====================================

def limpar_interesse(valor):


    valor = limpar_texto(valor)


    remover = [

        "jogar ",
        "assistir ",
        "ler ",
        "ver "

    ]


    for item in remover:


        if valor.lower().startswith(item):

            valor = valor[len(item):]

            break


    return limpar_texto(valor)



# =====================================
# Detectar interesses
# =====================================

def detectar_interesses(texto, memoria):


    resultados = re.findall(

        r"gosto de ([^.!,]+)",

        texto,

        re.IGNORECASE

    )


    for item in resultados:


        item = limpar_interesse(item)


        if item:

            memoria["interesses"].append(item)



# =====================================
# Detectar projetos
# =====================================

def detectar_projetos(texto, memoria):


    padroes = [

        r"estou criando ([^.!,]+)",

        r"estou desenvolvendo ([^.!,]+)",

        r"meu projeto.*é ([^.!,]+)"

    ]


    for padrao in padroes:


        resultados = re.findall(

            padrao,

            texto,

            re.IGNORECASE

        )


        for item in resultados:


            item = limpar_texto(item)


            if "draco ai" in item.lower():

                item = "Draco AI"


            memoria["projetos"].append(item)



# =====================================
# Detectar conhecimentos
# =====================================

def detectar_conhecimentos(texto, memoria):


    resultados = re.findall(

        r"(?:estudo|estou estudando|aprendo) ([^.!,]+)",

        texto,

        re.IGNORECASE

    )


    for item in resultados:


        item = limpar_texto(item)


        if item:

            memoria["outras_memorias"].append(item)



# =====================================
# Identificar tipo mensagem
# =====================================

def identificar_tipo_mensagem(texto):

    texto = texto.lower().strip()

    # =================================
    # CONSULTAS DE MEMÓRIA
    # =================================

    perguntas_usuario = [

        "o que você sabe sobre mim",

        "quem sou eu",

        "você lembra de mim",

        "me descreva",

        "qual meu nome",

        "qual minha idade",

        "onde eu moro",

        "o que eu gosto",

        "do que eu gosto",

        "quais são meus interesses",

        "quais meus interesses",

        "quais são minhas preferências",

        "o que você lembra sobre mim"

    ]


    for pergunta in perguntas_usuario:

        if pergunta in texto:

            return "CONSULTA_MEMORIA"


    # =================================
    # QUALQUER PERGUNTA
    # =================================

    if texto.endswith("?"):

        return "CONVERSA"


    # =================================
    # AFIRMAÇÕES PARA APRENDER
    # =================================

    afirmacoes = [

        "meu nome é",

        "meu nome e",

        "me chamo",

        "eu sou",

        "tenho",

        "eu tenho",

        "gosto de",

        "eu gosto de",

        "moro em",

        "sou de",

        "estou criando",

        "estou desenvolvendo"

    ]


    for afirmacao in afirmacoes:

        if afirmacao in texto:

            return "APRENDER_MEMORIA"


    return "CONVERSA"   



# =====================================
# Remover duplicados
# =====================================

def remover_duplicados(lista):


    resultado = []


    for item in lista:


        if item not in resultado:

            resultado.append(item)


    return resultado



# =====================================
# Detector principal
# =====================================

def detectar_memoria(texto):

    if isinstance(texto, dict):
        texto = texto.get("texto", "")

    texto = texto.strip()


    memoria = criar_memoria()


    texto = texto.strip()



    detectar_nome(
        texto,
        memoria
    )


    detectar_idade(
        texto,
        memoria
    )


    detectar_localizacao(
        texto,
        memoria
    )


    detectar_caracteristicas(
        texto,
        memoria
    )


    detectar_interesses(
        texto,
        memoria
    )


    detectar_projetos(
        texto,
        memoria
    )


    detectar_conhecimentos(
        texto,
        memoria
    )



    memoria["interesses"] = remover_duplicados(
        memoria["interesses"]
    )


    memoria["projetos"] = remover_duplicados(
        memoria["projetos"]
    )


    memoria["caracteristicas"] = remover_duplicados(
        memoria["caracteristicas"]
    )


    memoria["outras_memorias"] = remover_duplicados(
        memoria["outras_memorias"]
    )



    encontrou = any([

        memoria["nome"],

        memoria["idade"],

        memoria["localizacao"],

        memoria["interesses"],

        memoria["projetos"],

        memoria["caracteristicas"],

        memoria["outras_memorias"]

    ])



    if encontrou:

        return memoria


    return None