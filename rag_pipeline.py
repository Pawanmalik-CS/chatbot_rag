import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq
import hashlib

# ─── Load Environment Variables ─────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ─── Constants ──────────────────────────────────────────────────
DATA_PATH = "data/"
CHROMA_PATH = "chroma_db/"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"

# ─── Step 1: Load Documents ─────────────────────────────────────
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} documents")
    return documents

# ─── Step 2: Split into Chunks ──────────────────────────────────
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks

# ─── Step 3: Create Embeddings & Store in ChromaDB ──────────────
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("✅ Vector store created and saved!")
    return vector_store

# ─── Step 4: Load Existing Vector Store ─────────────────────────
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    return vector_store

# ─── Step 5: Retrieve Relevant Chunks ───────────────────────────
def retrieve(query, vector_store, k=3):
    results = vector_store.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

# ─── Step 6: Generate Answer using Groq ─────────────────────────
def generate_answer(query, context, history=[]):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "system",
            "content": f"""You are a friendly, conversational AI assistant.
Talk naturally like a human would — be warm, engaging and casual.
For general chit chat like greetings, jokes or how are you — just respond naturally.
Answer questions naturally as if you already know the information — never mention any context, documents, or data source.

Important rules:
- NEVER say things like "according to the context", "as mentioned in the document", "based on the provided context", "you mentioned" or anything that reveals you are using a background document
- Just answer naturally as if the knowledge is your own
- Do NOT entertain sensitive, harmful, illegal, or inappropriate topics
- If someone asks about violence, drugs, weapons, or anything harmful politely decline and change the subject
- Do NOT provide medical, legal, or financial advice
- Keep conversations positive, helpful and safe
- Answer each question independently

Context:
{context}"""
        }
    ]

    # Safely add history
    try:
        for msg in history[-4:]:
            if (
                isinstance(msg, dict)
                and msg.get("role") in ["user", "assistant"]
                and isinstance(msg.get("content"), str)
                and msg.get("content").strip() != ""
            ):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
    except Exception:
        pass  # If history is broken just skip it

    # Add current question
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7
    )

    return response.choices[0].message.content

# ─── Main RAG Function ──────────────────────────────────────────


def get_files_hash():
    """Generate a hash of all files in data folder to detect changes"""
    hash_md5 = hashlib.md5()
    for root, dirs, files in os.walk(DATA_PATH):
        for file in sorted(files):
            filepath = os.path.join(root, file)
            with open(filepath, "rb") as f:
                hash_md5.update(f.read())
    return hash_md5.hexdigest()

def get_saved_hash():
    hash_file = os.path.join(CHROMA_PATH, "data_hash.txt")
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            return f.read()
    return None

def save_hash(hash_value):
    os.makedirs(CHROMA_PATH, exist_ok=True)
    hash_file = os.path.join(CHROMA_PATH, "data_hash.txt")
    with open(hash_file, "w") as f:
        f.write(hash_value)

def rag_answer(query, history=[]):
    use_rag = False

    # Only use RAG if data folder has files with content
    if os.path.exists(DATA_PATH) and os.listdir(DATA_PATH):
        current_hash = get_files_hash()
        saved_hash = get_saved_hash()

        if current_hash != saved_hash or not os.path.exists(CHROMA_PATH):
            print("🔄 Data changed! Rebuilding vector store...")
            documents = load_documents()
            chunks = split_documents(documents)
            if chunks:
                create_vector_store(chunks)
                save_hash(current_hash)
                print("✅ Vector store updated!")
                use_rag = True
            else:
                print("⚠️ No chunks found, skipping vector store.")
        else:
            use_rag = True

    # Use RAG context if available otherwise just use Groq directly
    if use_rag and os.path.exists(CHROMA_PATH):
        vector_store = load_vector_store()
        context = retrieve(query, vector_store)
    else:
        context = "No specific context available. Use your general knowledge."

    answer = generate_answer(query, context, history)
    return answer