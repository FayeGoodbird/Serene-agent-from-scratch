# ## Step 5. Smart Memory: a checkpointer and `thread_id`

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from pathlib import Path

from messages import messages
from serene.persona import SERENE_PROMPT
from serene.tools import log_episode, recall_history

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(exist_ok=True)


LCAgent = create_agent(
    model=ChatOllama(model="qwen3:8b", temperature=0.2, num_predict=3500, reasoning = True),
    tools=[log_episode, recall_history],
    system_prompt=SERENE_PROMPT,
    checkpointer=InMemorySaver()
    )

with open(OUT / "step5_output.md", "a", encoding="utf-8") as f: 
    f.write(LCAgent.get_graph().draw_ascii()+ "\n")
    for in_msg in messages:
        LLMMsg = LCAgent.invoke({"messages": [in_msg]}, config={"configurable": {"thread_id": "ToSerene1"}})
        for msg in LLMMsg["messages"]:
                f.write(f"\n-----------")
                f.write(f"{type(msg).__name__}: {msg.content}\n")        
                f.write(f"tool_calls: {getattr(msg, 'tool_calls', None)}\n")

    LLMMsg = LCAgent.invoke({"messages": [messages[-1]]}, config={"configurable": {"thread_id": "new_thread"}})   
    for msg in LLMMsg["messages"]:
            f.write(f"\n---Diff Thread------")
            f.write(f"{type(msg).__name__}: {msg.content}\n")        
            f.write(f"tool_calls: {getattr(msg, 'tool_calls', None)}\n")