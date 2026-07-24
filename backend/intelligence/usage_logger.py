"""
Draco AI - Usage Logger

Registra QUAIS memórias foram recuperadas para QUAL
pergunta, sem alterar em nada o comportamento de quem
o chama.

Esse é o dado bruto que faltava para a fase 2 do
regression_predictor: treinar com uso real do Draco,
em vez de apenas dados simulados.

Garantias deste módulo:

- Nunca lança exceção para quem o chama. Falha de
  logging não pode derrubar uma resposta do Draco.
- Append-only: só acrescenta eventos, nunca apaga
  nem modifica os arquivos oficiais de memória.
- Arquivo próprio (usage_log.json), isolado dos
  arquivos usados por memory_manager.py.
"""

import json
import os

from datetime import datetime


BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE_DIR, "data")

USAGE_LOG_FILE = os.path.join(
    DATA_DIR,
    "usage_log.json"
)


# limite de eventos guardados (evita crescimento infinito)
MAX_EVENTOS = 5000


# =====================================
# Arquivo
# =====================================

def _garantir_arquivo():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USAGE_LOG_FILE):

        with open(USAGE_LOG_FILE, "w", encoding="utf-8") as arquivo:

            json.dump(
                {"eventos": []},
                arquivo,
                indent=4,
                ensure_ascii=False
            )


def _carregar():

    _garantir_arquivo()

    try:

        with open(USAGE_LOG_FILE, "r", encoding="utf-8") as arquivo:

            return json.load(arquivo)

    except (json.JSONDecodeError, FileNotFoundError):

        return {"eventos": []}


def _salvar(dados):

    with open(USAGE_LOG_FILE, "w", encoding="utf-8") as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# =====================================
# Registrar evento de uso
# =====================================

def registrar_uso(
    pergunta,
    categoria,
    chaves,
    origem="regras",
    confianca=None
):
    """
    Registra que, para uma determinada pergunta, o Draco
    recuperou uma categoria de memória e um conjunto de
    chaves específicas.

    Nunca levanta exceção: se algo falhar (disco cheio,
    permissão, etc), o evento simplesmente não é salvo e
    a função retorna False. Quem chama não precisa tratar
    nada.
    """

    try:

        dados = _carregar()

        evento = {

            "pergunta": pergunta,

            "categoria": categoria,

            "chaves": list(chaves) if chaves else [],

            "origem": origem,

            "confianca": confianca,

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

        dados["eventos"].append(evento)

        # mantém só os eventos mais recentes
        dados["eventos"] = dados["eventos"][-MAX_EVENTOS:]

        _salvar(dados)

        return True

    except Exception:

        return False


# =====================================
# Consultas sobre o log
# =====================================

def carregar_eventos():

    return _carregar().get("eventos", [])


def contar_recuperacoes(chave):
    """
    Quantas vezes essa chave de memória já foi recuperada.
    Feature útil para uma futura versão do modelo de
    relevância (frequência de uso real).
    """

    eventos = carregar_eventos()

    return sum(
        1
        for evento in eventos
        if chave in evento.get("chaves", [])
    )


def ultima_recuperacao(chave):
    """
    Timestamp (string) da última vez que essa chave foi
    recuperada, ou None se nunca foi.
    """

    eventos = carregar_eventos()

    for evento in reversed(eventos):

        if chave in evento.get("chaves", []):

            return evento.get("timestamp")

    return None


if __name__ == "__main__":

    registrar_uso(
        pergunta="Qual meu nome?",
        categoria="permanente",
        chaves=["nome"],
        origem="regras",
        confianca=1.0
    )

    print("Eventos registrados:", len(carregar_eventos()))

    print("Recuperações de 'nome':", contar_recuperacoes("nome"))
