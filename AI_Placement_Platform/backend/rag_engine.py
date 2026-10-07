import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini = genai.GenerativeModel(
    "gemini-2.0-flash"
)

DATA_DIR = Path(__file__).resolve().parent / "data"
CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"

model = None
client = None
collection = None


def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def get_collection():
    global client, collection
    if client is None:
        import chromadb

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if collection is None:
        collection = client.get_or_create_collection(name="placement_docs")
    return collection


def load_documents():
    docs = []

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    for path in sorted(DATA_DIR.iterdir()):
        if path.is_file():
            with path.open("r", encoding="utf8") as f:
                docs.append(f.read())

    return docs


def index_documents():
    docs = load_documents()
    current_collection = get_collection()
    existing = set(current_collection.get().get("ids", []))
    embedding_model = get_model()

    for i, doc in enumerate(docs):
        doc_id = str(i)
        if doc_id in existing:
            continue
        embedding = embedding_model.encode(doc).tolist()
        current_collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[doc],
        )

    print("Indexed Successfully")

def retrieve(query):
    embedding_model = get_model()
    current_collection = get_collection()
    query_embedding = embedding_model.encode(query).tolist()

    results = current_collection.query(

        query_embeddings=[query_embedding],

        n_results=2
    )

    return results["documents"]


def ask_question(question):

    docs = retrieve(question)

    context = "\n".join(docs[0])

    prompt = f"""

    Context:

    {context}

    Question:

    {question}

    Answer:
    """

    response = gemini.generate_content(
        prompt
    )

    return response.text
