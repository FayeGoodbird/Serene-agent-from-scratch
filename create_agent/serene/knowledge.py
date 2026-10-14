from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

EMBED_MODEL = "nomic-embed-text"
INDEX_PATH = Path(__file__).parent / ".cache" / "index.json"
_store: InMemoryVectorStore | None = None

def _breadcrumb(meta: dict) -> str:
    # Skip h1: it's just the document title ("SoYi — Framework"), which adds noise and the brand name.
    parts = [meta[h] for h in ("h2", "h3") if meta.get(h)]
    return " > ".join(parts) or meta.get("h1", "")

def _load_chunks() -> list[Document]:
    # Load markdown files
    knowledge_path = Path(__file__).resolve().parents[2] / "knowledge"
    md_files = list(knowledge_path.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files.")

    chunks = []
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Split on headings first
            header_splitter = MarkdownHeaderTextSplitter(strip_headers=True, headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")])
            header_chunks = header_splitter.split_text(content)
            # Then cap length with RecursiveCharacterTextSplitter
            char_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
            # chunks.extend([doc.page_content for doc in char_splitter.split_documents(header_chunks)])
            for doc in char_splitter.split_documents(header_chunks):
                doc.metadata["source"] = md_file.name
                crumb = _breadcrumb(doc.metadata)
                if crumb:
                    doc.page_content = f"[{crumb}]\n{doc.page_content}"
                chunks.append(doc)
    return chunks

class NomicEmbeddings(OllamaEmbeddings):
    """due to how it's trained, nomic-embed-text needs task prefixes:
      documents and queries are embedded differently."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return super().embed_documents([f"search_document: {t}" for t in texts])

    def embed_query(self, text: str) -> list[float]:
        return super().embed_query(f"search_query: {text}")

def get_store() -> InMemoryVectorStore:
    """Load the cached index, or build it. Delete .cache/ to force a rebuild."""
    global _store  # Not a new variable declaration here, but an instruction: the value is assigned to the module-level variable _store  
    if _store is None:
        embeddings = NomicEmbeddings(model=EMBED_MODEL)
        if INDEX_PATH.exists():
            _store = InMemoryVectorStore.load(str(INDEX_PATH), embeddings)
        else:
            _store = InMemoryVectorStore.from_documents(_load_chunks(), embeddings)
            INDEX_PATH.parent.mkdir(exist_ok=True)
            _store.dump(str(INDEX_PATH))
    return _store
# get_store()

def search(query: str, k: int = 4) -> list[Document]:
    return get_store().similarity_search(query, k=k)