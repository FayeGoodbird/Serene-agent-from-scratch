from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from pathlib import Path

from messages import messages
from serene.persona import SERENE_PROMPT
from serene.tools import log_episode, recall_history, search_knowledge


LCAgent = create_agent(
    model=ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=5000, reasoning = True),
    tools=[log_episode, recall_history, search_knowledge],
    system_prompt=SERENE_PROMPT,
    checkpointer=InMemorySaver()
    )

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
OUT.mkdir(exist_ok=True)
(OUT / "step6_output.md").unlink(missing_ok=True)
(HERE / "serene" / "history.json").unlink(missing_ok=True)

with open(OUT / "step6_output.md", "a", encoding="utf-8") as f: 
    f.write(LCAgent.get_graph().draw_ascii()+ "\n")
    for in_msg in messages:        
        LLMMsg = LCAgent.invoke({"messages": [in_msg]}, config={"configurable": {"thread_id": "ToSerene1"}})
               
        for msg in LLMMsg["messages"]:
                f.write(f"\n-----------")
                f.write(f"{type(msg).__name__}: {msg.content}\n")        
                f.write(f"tool_calls: {getattr(msg, 'tool_calls', None)}\n")
