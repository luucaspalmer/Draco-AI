import ast
import unittest
from pathlib import Path

from backend.intelligence.intelligence_orchestrator import (
    IntelligenceOrchestrator,
)
from backend.prompt_builder import construir_prompt


class IntelligenceIntegrationTests(unittest.TestCase):

    def test_ambiguity_stops_before_context_planning(self):
        result = IntelligenceOrchestrator().analisar(
            "Pode melhorar isso?",
            {"entity": "", "question_type": "unknown"},
            {"route": "general"},
            "conversa",
        )

        self.assertTrue(result["precisa_esclarecimento"])
        self.assertIsNone(result["plano_contexto"])
        self.assertIsNone(result["estrategia_resposta"])

    def test_orchestrator_returns_context_plan_and_strategy(self):
        result = IntelligenceOrchestrator().analisar(
            "Explique detalhadamente redes neurais.",
            {
                "entity": "redes neurais",
                "question_type": "definition",
            },
            {"route": "general"},
            "conversa",
        )

        self.assertFalse(result["precisa_esclarecimento"])
        self.assertEqual(result["analise_intencao"]["complexidade"], "alta")
        self.assertIsNotNone(result["plano_contexto"])
        self.assertIn("passo", result["estrategia_resposta"])

    def test_prompt_includes_intelligence_strategy(self):
        prompt = construir_prompt(
            {
                "pergunta": "Compare duas abordagens.",
                "plano_resposta": {
                    "instrucao_estilo": "Use linguagem clara."
                },
                "estrategia_resposta": (
                    "Organize a resposta em tópicos."
                ),
            }
        )

        self.assertIn("=== ESTRATÉGIA DE RESPOSTA ===", prompt)
        self.assertIn("Organize a resposta em tópicos.", prompt)

    def test_brain_references_the_intelligence_orchestrator(self):
        source = Path("backend/brain.py").read_text(encoding="utf-8")
        tree = ast.parse(source)

        imported = any(
            isinstance(node, ast.ImportFrom)
            and node.module == "backend.intelligence.intelligence_orchestrator"
            and any(alias.name == "IntelligenceOrchestrator" for alias in node.names)
            for node in ast.walk(tree)
        )
        instantiated = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "IntelligenceOrchestrator"
            for node in ast.walk(tree)
        )

        self.assertTrue(imported)
        self.assertTrue(instantiated)


if __name__ == "__main__":
    unittest.main()
