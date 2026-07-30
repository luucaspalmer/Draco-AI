Documentação Técnica — Draco AI

Versão: Julho/2026
Status: Em desenvolvimento ativo
Arquitetura: Assistente Inteligente Local baseado em LLM + Memória Persistente + Sistema Cognitivo Modular




1. Visão Geral do Projeto




OBJETIVO
O Draco AI é um assistente pessoal inteligente desenvolvido para funcionar localmente, oferecendo uma experiência semelhante aos grandes assistentes baseados em IA (como ChatGPT), porém com:

memória persistente;
raciocínio contextual;
arquitetura modular;
processamento local;
possibilidade de expansão praticamente ilimitada.

O projeto não foi pensado apenas como um chatbot.

A ideia sempre foi construir um sistema cognitivo, dividido em módulos especializados que analisam perguntas, escolhem fontes de informação, organizam contexto, utilizam ferramentas externas quando necessário e produzem respostas consistentes.





FILOSOFIA DO PROJETO

Ao invés de enviar toda pergunta diretamente para um LLM, o Draco tenta "pensar antes de responder".

O fluxo geral é:

Usuário
      │
      ▼

Análise da intenção

      │
      ▼

Planejamento da resposta

      │
      ▼

Escolha das fontes

      │
      ▼

Construção de contexto

      │
      ▼

LLM

      │
      ▼

Resposta

Ou seja, existe uma camada de inteligência entre o usuário e o modelo de IA.

Atualmente o projeto possui:

Núcleo
Conversação por texto
Comunicação com LLM local
Construção dinâmica de prompt
Context Builder
Context Manager
Histórico de conversa
Sistema de Memória

Implementado praticamente por completo.

Inclui:

memória permanente
memória temporária
memória de preferências
memória de projetos
memória de conhecimento

Também possui:

detector automático de memória
extração
validação
armazenamento
pesquisa
formatação
raciocínio sobre memórias
grafo de memória
Inteligência


Inclui módulos como:

Intent Analyzer
Ambiguity Detector
Source Planner
Response Strategy
Memory Attention
Context Relevance Selector

Esses módulos funcionam como um "cérebro executivo".

Sistema de Perguntas:

Responsável por:

interpretar perguntas
identificar entidades
resolver entidades
decidir qual ferramenta utilizar
despachar execução
Sistema RAG

Possui:

carregamento de documentos
embeddings
banco vetorial
recuperação semântica
geração de contexto
Ferramentas

Atualmente existem ferramentas como:

Weather Tool
Windows Controller Tool / criado manualmente
Tool Manager

A arquitetura foi preparada para expansão com dezenas de ferramentas.

Voz

Grande parte implementada.

Inclui:

Speech-to-Text
Text-to-Speech
reprodução de áudio
gerenciamento de voz

Também foi desenvolvido um protótipo de Wake Assistant utilizando Faster Whisper + Piper.

Frontend

Interface Web composta por:

Chat
Avatar
Sidebar
Painéis
Comunicação HTTP com backend
Objetivos futuros







2. Arquitetura e Estrutura do Sistema

A estrutura atual do projeto é composta por um backend modular e um frontend web. As principais pastas identificadas são as seguintes.

Draco AI
│
├── backend
│
├── intelligence
├── memory
├── question
├── rag
├── tools
├── voice
├── weather
├── tests
│
└── frontend
    ├── assets
    ├── components
    ├── css
    └── js
Backend

É o cérebro do sistema.

Responsável por toda lógica.

Arquivos centrais incluem brain.py, prompt_builder.py, context_builder.py, context_manager.py, ollama_client.py, identity.py, personality.py, commands.py, config.py e módulos de intenção e memória.

intelligence/

Camada cognitiva.

Responsável por decidir como responder.

Contém:

Intelligence Orchestrator
Intent Analyzer
Ambiguity Detector
Source Planner
Response Strategy
Memory Attention
Context Relevance Selector
Regressão para relevância
memory/

É provavelmente o maior módulo do projeto.

Responsável por:

detectar memórias
validar
armazenar
pesquisar
raciocinar
montar grafos
controlar memória persistente

Também armazena arquivos JSON de memória e documentação da arquitetura.

question/

Pipeline de perguntas.

Divide o problema em etapas:

Pergunta

↓

Analisar

↓

Resolver entidades

↓

Planejar resposta

↓

Executar

↓

Retornar
rag/

Sistema de Retrieval Augmented Generation.

Possui:

loader
embeddings
retriever
vector store
manager
tools/

Sistema de ferramentas.

Existe um Tool Manager que registra ferramentas disponíveis.

Hoje já existe uma Weather Tool.

voice/

Toda parte de voz.

Inclui:

microfone
whisper
TTS
player
gerenciamento de voz
weather/

Módulo isolado para previsão do tempo.

Inclui serviço, formatação e códigos meteorológicos.

tests/

Testes unitários e de integração para praticamente todos os módulos principais (RAG, perguntas, ferramentas, inteligência e clima).

Frontend

Estrutura web organizada em componentes, folhas de estilo e scripts JavaScript. Possui index.html, componentes reutilizáveis (chat.html, sidebar.html, draco.html, status.html), CSS dedicado e scripts como api.js, app.js, chat.js, draco.js, ui.js e voice.js.

3. Stack Tecnológica
Backend
Python
FastAPI
Uvicorn
JSON
ChromaDB
Sentence Transformers
Faster Whisper
Piper
SQLite (módulos especializados, como futebol)
Joblib
RandomForestRegressor (modelo de relevância)
Frontend
HTML
CSS
JavaScript

Sem frameworks pesados.

IA
Modelo principal

Ollama

Modelo utilizado durante o desenvolvimento:

Qwen 2.5 3B

A arquitetura, entretanto, foi desenhada para permitir troca de modelo praticamente sem alterar a lógica da aplicação, podendo integrar outros LLMs locais (como LM Studio) ou APIs externas no futuro.

RAG

Tecnologias utilizadas:

Sentence Transformers
ChromaDB
Embeddings
Busca Vetorial
Voz

Speech-to-Text

Faster Whisper

Text-to-Speech

Piper
4. Fluxo de Dados e Rotas da API
Fluxo Geral
Frontend

↓

HTTP

↓

FastAPI

↓

Brain

↓

Intelligence

↓

Question System

↓

Memory

↓

RAG

↓

Tools

↓

LLM

↓

Resposta
Fluxo interno
Usuário

↓

Question Analyzer

↓

Intent Analyzer

↓

Source Planner

↓

Memory Search

↓

RAG

↓

Prompt Builder

↓

Ollama

↓

Resposta

↓

Salvar memória
Endpoints principais

Embora a estrutura completa do servidor não esteja listada nos arquivos enviados, durante o desenvolvimento foram definidos como principais:

Endpoint	Função
/chat	Recebe mensagens de texto, executa todo o pipeline cognitivo e retorna a resposta do LLM.
/voice	Recebe áudio do frontend, realiza transcrição (Speech-to-Text), processa a pergunta e retorna a resposta, que pode ser sintetizada em voz.

O backend foi concebido para permitir a adição de novos endpoints (ferramentas, plugins, automações e integrações) mantendo a separação entre interface, lógica de negócio e módulos especializados.

Comunicação Frontend → Backend

Fluxo:

Usuário

↓

chat.js

↓

api.js

↓

FastAPI

↓

Backend

↓

JSON

↓

Frontend

↓

Interface

A comunicação é baseada em requisições HTTP com troca de dados em JSON.

5. Estado Atual e Próximos Passos
Funcionalidades concluídas
Arquitetura modular
Sistema de memória persistente
Detector de memória
Extração e validação de memória
Context Builder
Context Manager
Pipeline de perguntas
Sistema RAG
Sistema de Inteligência
Tool Manager
Weather Tool
Comunicação com Ollama
Frontend funcional
Voz (Speech-to-Text e Text-to-Speech)
Testes para diversos módulos
Últimas implementações




CONCLUSÃO

O Draco AI evoluiu de um chatbot para uma plataforma de assistência inteligente composta por módulos independentes que cooperam entre si. Sua arquitetura privilegia separação de responsabilidades, facilidade de manutenção e escalabilidade. O sistema já reúne um núcleo conversacional, memória persistente, mecanismos de recuperação de conhecimento (RAG), orquestração cognitiva, ferramentas especializadas e suporte a voz, formando uma base sólida para futuras capacidades de agentes autônomos e automação inteligente.