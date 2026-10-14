from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from pathlib import Path

from messages import messages
from serene.persona import SERENE_PROMPT
from serene.tools import log_episode, recall_history

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(exist_ok=True)

# ## Step 4. Your first tool
LCAgent = create_agent(
    model=ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=1500, reasoning = True),
    tools=[log_episode, recall_history],
    system_prompt=SERENE_PROMPT
    )

historical_messages = []

with open(OUT / "step4_output.md", "a", encoding="utf-8") as f: 
    f.write(LCAgent.get_graph().draw_ascii()+ "\n")    
    for in_msg in messages:
        historical_messages.append(in_msg)
        LLMMsg = LCAgent.invoke({"messages": historical_messages})
        historical_messages = LLMMsg["messages"]


        for msg in LLMMsg["messages"]:
                f.write(f"\n-----------")
                f.write(f"{type(msg).__name__}: {msg.content}\n")
        
                f.write(f"tool_calls: {getattr(msg, 'tool_calls', None)}\n")
        
