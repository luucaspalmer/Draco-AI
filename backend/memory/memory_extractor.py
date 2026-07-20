"""
Draco AI - Memory Extractor

Responsável por interpretar informações do usuário
e converter informações importantes em memórias
estruturadas.
"""

import json

from backend.ollama_client import perguntar_ao_qwen



MEMORY_TEMPLATE = {

    "nome": None,

    "idade": None,

    "profissao": None,

    "localizacao": None,

    "interesses": [],

    "projetos": [],

    "preferencias": [],

    "objetivos": [],

    "relacionamentos": [],

    "outras_memorias": []

}





def extrair_memorias(texto: str) -> dict:
    """
    Recebe uma mensagem do usuário e extrai
    informações importantes para memória.
    """



    prompt = f"""
Você é o Memory Extractor da Draco AI.

Sua única função é extrair memórias importantes
sobre o usuário.

NÃO converse.
NÃO explique.
NÃO responda perguntas.

Retorne SOMENTE JSON válido.



===============================
REGRAS DE EXTRAÇÃO
===============================


Extraia informações explicitamente presentes
na mensagem.

Não invente informações.

Não transforme contexto em profissão.



===============================
NOME
===============================

Quando o usuário informar o próprio nome.

Exemplo:

Entrada:
"Meu nome é Lucas"

Saída:

"nome": "Lucas"



===============================
LOCALIZAÇÃO
===============================

Quando informar cidade, estado ou país.

Exemplo:

Entrada:
"Moro em Araucária no Paraná"

Saída:

"localizacao":
"Araucária, Paraná"



===============================
PROFISSÃO
===============================

Somente extraia profissão quando o usuário
declarar explicitamente.

Aceito:

"Minha profissão é logística"

"Eu trabalho como programador"


Não aceito:

"Estou criando uma IA"

"Tenho um projeto de servidor"

"Estudo Python"


Nunca deduza profissão.



===============================
PROJETOS
===============================

Use quando o usuário estiver criando,
desenvolvendo ou trabalhando em algo.


Exemplos:


Entrada:

"Estou criando o Draco AI como meu projeto
principal"


Saída:

"projetos":
[
    "Draco AI"
]



Entrada:

"Estou desenvolvendo um servidor Ragnarok"


Saída:

"projetos":
[
    "Servidor Ragnarok"
]



===============================
INTERESSES
===============================

Use para coisas que o usuário gosta:

- jogos
- filmes
- músicas
- hobbies


Exemplo:


Entrada:

"Gosto de jogar Ragnarok"


Saída:

"interesses":
[
    "Ragnarok"
]



===============================
CONHECIMENTOS
===============================

Use em outras_memorias.

Quando o usuário:

- estuda;
- aprende;
- conhece;
- domina.


Exemplo:


Entrada:

"Também estudo Python"


Saída:

"outras_memorias":
[
    "Python"
]



===============================
PREFERÊNCIAS
===============================

Use para estilo de comunicação.


Exemplo:

"Prefiro explicações passo a passo"



===============================
OBJETIVOS
===============================

Use para metas futuras.


Exemplo:

"Quero aprender programação"



===============================
EXEMPLOS COMPLETOS
===============================



Mensagem:

"Meu nome é Lucas.
Moro em Araucária.
Gosto de Ragnarok.
Estou criando o Draco AI.
Também estudo Python."


Resultado esperado:

{{
    "nome": "Lucas",

    "localizacao": "Araucária",

    "interesses": [
        "Ragnarok"
    ],

    "projetos": [
        "Draco AI"
    ],

    "outras_memorias": [
        "Python"
    ]
}}



===============================
FORMATO FINAL OBRIGATÓRIO
===============================


Retorne exatamente:

{json.dumps(
    MEMORY_TEMPLATE,
    ensure_ascii=False,
    indent=4
)}



Mensagem do usuário:

--------------------

{texto}

--------------------

"""



    resposta = perguntar_ao_qwen(
        prompt
    )



    try:

        memoria = json.loads(
            resposta
        )


        if isinstance(
            memoria,
            dict
        ):

            return memoria



    except Exception:

        pass



    return MEMORY_TEMPLATE.copy()