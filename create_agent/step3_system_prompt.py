from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from pathlib import Path

from messages import messages
from serene.persona import SERENE_PROMPT

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(exist_ok=True)

LCAgent = create_agent(
    model=ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=300, reasoning = True,),
    tools=[],
    system_prompt=SERENE_PROMPT
    )

LLMMsg = LCAgent.invoke({"messages": messages})
Path(OUT / "step3_output.md").write_text(LCAgent.get_graph().draw_ascii(), encoding="utf-8")

for msg in LLMMsg["messages"]:
    with open(OUT / "step3_output.md", "a", encoding="utf-8") as f:
        f.write(f"\n-----------")
        f.write(f"{type(msg).__name__}: {msg.content}\n")
