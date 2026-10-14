# Serene-agent-from-scratch

Using the app SoYi as testbed, building "Serene", a calm coaching agent on a local open-source LLM (Qwen3 via Ollama), one layer at a time.

```
create_agent/   Step-by-step build with LangChain's create_agent (chat model, persona, tools, memory, RAG)
langgraph/      Same agent rebuilt on LangGraph (coming later)
knowledge/      Knowledge base shared by both builds
```

## Notes

[Serene_Agent_Notes.pdf](Serene_Agent_Notes.pdf) walks through the build step by step.

## Run (create_agent)

```
cd create_agent
python step6_agentic_rag.py
```

Requires Ollama with the chat model and `nomic-embed-text` pulled.
