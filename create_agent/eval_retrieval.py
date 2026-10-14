from serene.knowledge import get_store

K = 4

# What the LLM actually sends to search_knowledge (see output/step6_output.md), plus paraphrases.
QUERIES = [
    # taken from your real runs
    "eating when stressed",
    "self-judgment",
    "stress and eating",
    # paraphrases of the same situations
    "stress eating",
    "I eat when I feel overwhelmed at work",
    "can't stop snacking because of pressure",
    "feeling bad about my body",
    "I'm never going to look good again",
    "harsh inner critic after overeating",
    "ate biscuits after a bad day at work",
]

def section(meta: dict) -> str:
    parts = [meta.get(h) for h in ("h1", "h2", "h3") if meta.get(h)]
    return " > ".join(parts) or "(no heading)"

store = get_store()
for q in QUERIES:
    print(f"\n=== {q}")
    for rank, (doc, score) in enumerate(store.similarity_search_with_score(q, k=K), 1):
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"{rank}  {score:.3f}  [{doc.metadata['source']}] {section(doc.metadata)}")
        print(f"      {preview}")
