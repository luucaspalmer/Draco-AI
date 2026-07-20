# Arquitetura Atual da Memória (Legacy)

## Estrutura

backend/
│
├── memory/
│   ├── memory_controller.py
│   ├── memory_manager.py
│   ├── conversation_memory.py
│   ├── knowledge_memory.py
│   ├── permanent_memory.py
│   ├── preference_memory.py
│   ├── project_memory.py
│   └── docs/
│
├── memory_manager.py (legacy)
├── memory_search.py (legacy)
├── context_builder.py (legacy)
├── memory_detector.py (legacy)

---

## Dependências encontradas

### memory_manager

- commands.py
- context_builder.py
- memory_controller.py
- memory_search.py
- testes

### memory_search

- commands.py
- context_builder.py

### context_builder

- brain.py

### memory_detector

- brain.py
- memory_controller.py
- testes

---

## Observações

Atualmente coexistem duas arquiteturas:

1. Arquitetura antiga localizada em backend/.
2. Nova arquitetura localizada em backend/memory/.

Durante a migração nenhuma delas será removida até que a nova arquitetura baseada em SQLite esteja totalmente funcional.