"""
Draco AI - Regression Model

Wrapper enxuto sobre um modelo scikit-learn.

Responsabilidades:
- Treinar o modelo a partir de (X, y)
- Salvar/carregar o modelo treinado em disco (joblib)
- Prever relevância para novas features

Este módulo não sabe nada sobre memória, prompt ou
Draco em si — ele só sabe treinar/prever números.
Isso mantém a camada de inteligência desacoplada do
resto do sistema, como pedido.
"""

import os

import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


DEFAULT_MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "relevance_model.joblib"
)


class RegressionModel:
    """
    Modelo de regressão genérico usado pelo Draco
    para pontuar relevância / decisões.
    """

    def __init__(self, model_path=None):

        self.model_path = model_path or DEFAULT_MODEL_PATH

        self.model = RandomForestRegressor(
            n_estimators=150,
            max_depth=6,
            random_state=42
        )

        self.treinado = False

    # =====================================
    # Treino
    # =====================================

    def treinar(self, X, y, avaliar=True):

        if avaliar and len(X) >= 20:

            X_treino, X_teste, y_treino, y_teste = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            self.model.fit(X_treino, y_treino)

            predicoes = self.model.predict(X_teste)

            erro_medio = mean_absolute_error(y_teste, predicoes)

        else:

            self.model.fit(X, y)

            erro_medio = None

        self.treinado = True

        return {
            "amostras": len(X),
            "erro_medio_absoluto": erro_medio
        }

    # =====================================
    # Predição
    # =====================================

    def prever(self, features):
        """
        Args:
            features: lista única [f1, f2, ...] ou lista de listas

        Returns:
            float (se entrada única) ou list[float]
        """

        if not self.treinado:
            raise RuntimeError(
                "Modelo ainda não foi treinado nem carregado."
            )

        entrada_unica = (
            len(features) > 0 and not isinstance(features[0], (list, tuple))
        )

        dados = [features] if entrada_unica else features

        resultado = self.model.predict(dados)

        resultado = [max(0.0, min(1.0, float(v))) for v in resultado]

        return resultado[0] if entrada_unica else resultado

    # =====================================
    # Persistência
    # =====================================

    def salvar(self, path=None):

        path = path or self.model_path

        os.makedirs(os.path.dirname(path), exist_ok=True)

        joblib.dump(self.model, path)

    def carregar(self, path=None):

        path = path or self.model_path

        if not os.path.exists(path):
            return False

        self.model = joblib.load(path)

        self.treinado = True

        return True

    def importancia_features(self, nomes_features):

        if not self.treinado:
            return {}

        return dict(
            zip(nomes_features, self.model.feature_importances_.tolist())
        )
