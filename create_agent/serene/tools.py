from serene import knowledge
from langchain_core.tools import tool

# 1. In `serene/tools.py`, write `log_episode(behaviour, trigger, choice, note="")` 
# that appends a dict to a JSON file (use your own path, e.g. `serene/history.json`) and returns `"Logged."`.
@tool
def log_episode(behaviour: str, trigger: str, choice: str, note: str = "") -> str:
    """
    Log an episode of behavior, including the behavior, trigger, choice, and an optional note.
    This function appends the information to a JSON file for future reference.

    Parameters:
    - behaviour (str): The behavior that occurred.
    - trigger (str): The trigger that led to the behavior.
    - choice (str): The choice made in response to the trigger.
    - note (str, optional): Additional notes or context about the episode.

    Returns:
    - str: A confirmation message indicating that the episode has been logged.
    """
    import json
    from pathlib import Path

    # Define the path to the history file
    history_file = Path("serene/history.json")

    # Create the history file if it doesn't exist
    if not history_file.exists():
        history_file.write_text("[]", encoding="utf-8")

    # Load existing history
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    # Append the new episode
    episode = {
        "behaviour": behaviour,
        "trigger": trigger,
        "choice": choice,
        "note": note
    }
    history.append(episode)

    # Save the updated history back to the file
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    return "Logged."


# 2. Write `recall_history(limit=10)` that returns the last entries as JSON, or `"No history yet."`.
@tool
def recall_history(limit: int = 10) -> str:
    """
    Recall the last entries from the history of logged episodes.

    Parameters:
    - limit (int): The maximum number of recent entries to return.

    Returns:
    - str: A JSON string containing the last entries, or a message indicating no history exists.
    """
    import json
    from pathlib import Path

    # Define the path to the history file
    history_file = Path("serene/history.json")

    # Check if the history file exists
    if not history_file.exists():
        return "No history yet."

    # Load existing history
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    # Get the last 'limit' entries
    recent_history = history[-limit:]

    return json.dumps(recent_history, indent=4)

@tool
def search_knowledge(query: str) -> str:
    """Search Serene's knowledge base: 
    the 11 emotional trigger types (what is happening, what to offer, how Serene responds), 
    the coaching spec, and Yi Method philosophy. 
    Use a short description of the user's situation or feeling as the query, e.g. 'eating when stressed at the end of a work day'. 
    Returns labelled excerpts.

    Parameters:
    - query (str): The user's query or topic to search for.

    Returns:
    - str: A summary of the relevant information found in Serene's framework.
    """


    docs = knowledge.search(query)
    return "\n\n".join(f"[Source {i}: {d.metadata['source']}]\n{d.page_content}" for i, d in enumerate(docs, 1))
