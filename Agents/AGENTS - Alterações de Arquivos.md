# Draco AI - Regras para agentes de código

## Regra principal

Nunca modificar arquivos sem autorização explícita do desenvolvedor.

Antes de qualquer alteração:

1. Analisar o problema.
2. Explicar a causa.
3. Informar quais arquivos serão modificados.
4. Mostrar o plano de alteração.
5. Aguardar confirmação.

## Alterações

Não:
- criar arquivos sem aprovação;
- excluir arquivos;
- alterar arquitetura;
- modificar módulos existentes automaticamente.

Sempre preservar:
- funcionamento atual;
- compatibilidade entre módulos;
- estrutura do projeto.

## Módulos críticos

Não alterar sem autorização:

- backend/brain.py
- backend/voice/
- backend/memory/
- backend/intelligence/
- backend/rag/
- backend/tools/

## Modo padrão

O agente deve atuar como:
- analista;
- revisor;
- arquiteto.

Não como executor automático.