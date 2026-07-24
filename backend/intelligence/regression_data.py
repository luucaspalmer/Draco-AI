"""
Draco AI - Regression Data

Responsável por transformar registros de memória
(reais ou simulados) em vetores de features numéricas
que o modelo de regressão consegue consumir.

Este módulo NÃO lê nem escreve nos arquivos oficiais
de memória do Draco (permanent_memory.json etc).
Ele apenas sabe como interpretar um registro no formato
já usado por memory_manager.py:

{
    "valor": "...",
    "importancia": 8,
    "confianca": 1.0,
    "criado_em": "2026-07-17 21:17:10",
    "atualizado_em": "2026-07-18 10:10:29",
    "origem": "usuario"
}

Fase atual: sem histórico real de uso (quantas vezes a
memória foi recuperada / se foi útil na resposta), então
o treino usa dados simulados que já seguem essa mesma
estrutura de features. Quando o Draco passar a registrar
uso real (fase 2), basta trocar a fonte dos dados aqui.
"""

import random
from datetime import datetime, timedelta


# =====================================
# Nomes das features, na ordem usada
# pelo modelo (importante manter fixo)
# =====================================

FEATURE_NAMES = [
    "importancia",
    "confianca",
    "dias_desde_criacao",
    "dias_desde_atualizacao",
    "tamanho_valor",
    "foi_atualizada",
    "origem_usuario",
]


TIPO_PESO = {
    # peso base de importância por tipo de memória,
    # usado apenas na simulação (fase 1)
    "PERMANENTE": 9,
    "PROJETO": 7,
    "PREFERENCIA": 6,
    "CONHECIMENTO": 5,
}


# =====================================
# Utilitário de datas
# =====================================

def _parse_data(texto_data):

    if not texto_data:
        return None

    try:
        return datetime.strptime(texto_data, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


# =====================================
# Extrair features de um registro real
# =====================================

def extrair_features_memoria(registro, agora=None):
    """
    Recebe um registro no formato do memory_manager
    e retorna um vetor de features (lista de floats).

    Args:
        registro: dict com valor/importancia/confianca/...
        agora: datetime opcional (útil em testes)

    Returns:
        list[float] na ordem de FEATURE_NAMES
    """

    if not isinstance(registro, dict):
        return [0.0] * len(FEATURE_NAMES)

    agora = agora or datetime.now()

    importancia = float(registro.get("importancia", 5))

    confianca = float(registro.get("confianca", 0.5))

    criado_em = _parse_data(registro.get("criado_em"))

    atualizado_em = _parse_data(registro.get("atualizado_em"))

    dias_criacao = (
        (agora - criado_em).days
        if criado_em
        else 30
    )

    dias_atualizacao = (
        (agora - atualizado_em).days
        if atualizado_em
        else dias_criacao
    )

    valor = registro.get("valor", "")

    if isinstance(valor, list):
        tamanho_valor = sum(len(str(v)) for v in valor)
    else:
        tamanho_valor = len(str(valor))

    foi_atualizada = 1.0 if criado_em and atualizado_em and criado_em != atualizado_em else 0.0

    origem_usuario = 1.0 if registro.get("origem") == "usuario" else 0.0

    return [
        importancia,
        confianca,
        float(dias_criacao),
        float(dias_atualizacao),
        float(tamanho_valor),
        foi_atualizada,
        origem_usuario,
    ]


# =====================================
# Gerar dados simulados para treino
# =====================================

def gerar_dados_simulados(quantidade=400, seed=42):
    """
    Gera um dataset sintético (X, y) para treinar o
    modelo de relevância enquanto não existem dados
    reais de uso suficientes.

    A "verdade" simulada segue uma lógica plausível:
    memórias mais importantes, mais confiáveis, mais
    recentes e atualizadas recentemente tendem a ser
    mais relevantes. Isso dá ao modelo um ponto de
    partida sensato, não aleatório.

    Returns:
        (X, y): listas paralelas de features e alvo (0-1)
    """

    random.seed(seed)

    agora = datetime.now()

    X = []
    y = []

    tipos = list(TIPO_PESO.keys())

    for _ in range(quantidade):

        tipo = random.choice(tipos)

        peso_tipo = TIPO_PESO[tipo]

        importancia = max(
            1,
            min(10, round(random.gauss(peso_tipo, 1.5)))
        )

        confianca = max(0.3, min(1.0, random.gauss(0.85, 0.15)))

        dias_criacao = random.randint(0, 200)

        # atualização nunca é mais antiga que a criação
        dias_atualizacao = random.randint(0, dias_criacao)

        tamanho_valor = random.randint(3, 80)

        foi_atualizada = 1.0 if dias_atualizacao < dias_criacao else 0.0

        origem_usuario = 1.0 if random.random() > 0.15 else 0.0

        features = [
            float(importancia),
            confianca,
            float(dias_criacao),
            float(dias_atualizacao),
            float(tamanho_valor),
            foi_atualizada,
            origem_usuario,
        ]

        # =================================
        # Fórmula de relevância "verdadeira"
        # (usada só para gerar o alvo simulado)
        # =================================

        score = (
            (importancia / 10) * 0.45
            + confianca * 0.25
            + max(0.0, 1 - dias_criacao / 200) * 0.15
            + max(0.0, 1 - dias_atualizacao / 100) * 0.10
            + origem_usuario * 0.05
        )

        # ruído para não ficar uma função perfeita/determinística
        score += random.gauss(0, 0.04)

        score = max(0.0, min(1.0, score))

        X.append(features)
        y.append(score)

    return X, y


if __name__ == "__main__":

    X, y = gerar_dados_simulados(5)

    for features, alvo in zip(X, y):
        print(dict(zip(FEATURE_NAMES, features)), "-> relevância:", round(alvo, 3))
