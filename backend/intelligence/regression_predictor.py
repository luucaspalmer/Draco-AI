"""
Draco AI - Regression Predictor

Camada de mais alto nível da inteligência preditiva do
Draco. É a única porta de entrada que o resto do sistema
deveria usar (memory_search, context_manager, etc. quando
a integração for feita na fase 2).

Uso pretendido (futuro, opcional):

    from backend.intelligence.regression_predictor import predictor

    score = predictor.prever_relevancia(registro_memoria)

Nesta primeira versão, nada no restante do backend importa
este módulo — ele existe e funciona de forma independente,
sem risco de quebrar memória, RAG, intent classifier ou
brain.py.
"""

from backend.intelligence.regression_data import (
    FEATURE_NAMES,
    extrair_features_memoria,
    gerar_dados_simulados,
)

from backend.intelligence.regression_model import RegressionModel


class RelevancePredictor:
    """
    Prevê a relevância (0 a 1) de uma memória para o
    momento atual da conversa.
    """

    def __init__(self, auto_carregar=True):

        self.model = RegressionModel()

        self.pronto = False

        if auto_carregar:

            self._preparar()

    # =====================================
    # Preparação: carrega modelo salvo ou
    # treina com dados simulados na hora
    # =====================================

    def _preparar(self):

        if self.model.carregar():

            self.pronto = True

            return

        self.treinar_com_dados_simulados()

    # =====================================
    # Treino explícito
    # =====================================

    def treinar_com_dados_simulados(self, quantidade=400, salvar=True):

        X, y = gerar_dados_simulados(quantidade)

        metricas = self.model.treinar(X, y)

        self.pronto = True

        if salvar:

            self.model.salvar()

        return metricas

    def treinar_com_dados_reais(self, registros_com_alvo, salvar=True):
        """
        Fase 2: quando o Draco já tiver histórico real de
        uso de memória (ex: "essa memória foi usada e a
        resposta foi considerada boa"), treine com isso.

        Args:
            registros_com_alvo: list[(registro_memoria, relevancia_real)]
        """

        if not registros_com_alvo:

            raise ValueError("Nenhum dado real fornecido para treino.")

        X = [
            extrair_features_memoria(registro)
            for registro, _ in registros_com_alvo
        ]

        y = [alvo for _, alvo in registros_com_alvo]

        metricas = self.model.treinar(X, y)

        self.pronto = True

        if salvar:

            self.model.salvar()

        return metricas

    # =====================================
    # Predição individual
    # =====================================

    def prever_relevancia(self, registro_memoria):
        """
        Args:
            registro_memoria: dict no formato do memory_manager
                (valor/importancia/confianca/criado_em/...)

        Returns:
            float entre 0 e 1
        """

        if not self.pronto:

            self._preparar()

        features = extrair_features_memoria(registro_memoria)

        return self.model.prever(features)

    # =====================================
    # Predição em lote + ranking
    # =====================================

    def ranquear_memorias(self, camada_memoria):
        """
        Recebe uma camada inteira no formato:
        { "chave1": registro1, "chave2": registro2, ... }

        Returns:
            list[(chave, registro, score)] ordenada do
            mais relevante para o menos relevante.
        """

        if not isinstance(camada_memoria, dict) or not camada_memoria:

            return []

        chaves = list(camada_memoria.keys())

        features = [
            extrair_features_memoria(camada_memoria[chave])
            for chave in chaves
        ]

        if not self.pronto:

            self._preparar()

        scores = self.model.prever(features)

        resultado = [
            (chaves[i], camada_memoria[chaves[i]], scores[i])
            for i in range(len(chaves))
        ]

        resultado.sort(key=lambda item: item[2], reverse=True)

        return resultado

    def explicar_pesos(self):
        """
        Retorna a importância de cada feature no modelo
        atual — útil para debug e para entender o que o
        Draco está usando para decidir relevância.
        """

        if not self.pronto:

            self._preparar()

        return self.model.importancia_features(FEATURE_NAMES)


# =====================================
# Instância global (mesmo padrão de
# rag_manager em backend/rag/rag_manager.py)
# =====================================

predictor = RelevancePredictor()


# =====================================
# Teste manual
# =====================================

if __name__ == "__main__":

    registro_exemplo = {
        "valor": "Draco AI",
        "importancia": 8,
        "confianca": 0.9,
        "criado_em": "2026-07-17 21:17:10",
        "atualizado_em": "2026-07-18 10:10:29",
        "origem": "usuario"
    }

    score = predictor.prever_relevancia(registro_exemplo)

    print("Relevância prevista:", round(score, 3))

    print("\nImportância das features:")

    for nome, peso in predictor.explicar_pesos().items():

        print(f"- {nome}: {round(peso, 3)}")
