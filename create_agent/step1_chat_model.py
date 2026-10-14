from langchain_ollama import ChatOllama
from pathlib import Path

from messages import COACH_PROMPT, messages

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(exist_ok=True)

# Step 1. Call the LLM through a LangChain chat model (no agent yet)
LCChatModel = ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=100, reasoning = False)
LLMMsg = LCChatModel.invoke([{"role": "system", "content": COACH_PROMPT}, *messages])
Path(OUT / "step1_output.md").write_text(LLMMsg.content, encoding="utf-8")

LCChatModelReasoning = ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=300, reasoning = True)
LLMMsg = LCChatModelReasoning.invoke([{"role": "system", "content": COACH_PROMPT}, *messages])
Path(OUT / "step1_outputReasoning.md").write_text(LLMMsg.content, encoding="utf-8")