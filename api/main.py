from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import platform
import psutil
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- CONDITIONAL IMPORTS FOR DEVELOPMENT SPEED ---
# We wrap heavy imports so the API starts fast if they aren't installed yet
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    VECTOR_SUPPORT = True
except ImportError:
    VECTOR_SUPPORT = False

app = FastAPI(title="Antigravity Prime API", version="0.3.0 (Interactive)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str
    timestamp: float = datetime.now().timestamp()

class ChatRequest(BaseModel):
    message: str

class MemoryItem(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class Skill(BaseModel):
    id: str
    category: str
    path: str
    enabled: bool
    metadata: Optional[dict] = None

class SystemHealth(BaseModel):
    status: str
    uptime_seconds: float
    cpu_usage: float
    memory_usage: float
    platform: str
    timestamp: str
    vector_support: bool

# --- STATE ---
START_TIME = datetime.now()
CHROMA_CLIENT = None
EMBEDDING_MODEL = None

# --- UTILS ---
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
REGISTRY_PATH = os.path.join(ROOT_DIR, "antigravity", "skill_registry.json")
DATA_DIR = os.path.join(ROOT_DIR, "antigravity", "data", "chroma_db")

def init_vector_db():
    global CHROMA_CLIENT, EMBEDDING_MODEL
    if VECTOR_SUPPORT and CHROMA_CLIENT is None:
        try:
            print("🧠 Initializing Memory System (This may take a moment)...")
            os.makedirs(DATA_DIR, exist_ok=True)
            CHROMA_CLIENT = chromadb.PersistentClient(path=DATA_DIR)
            EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
            print("🧠 Memory System Online.")
        except Exception as e:
            print(f"❌ Memory System Failed: {e}")

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"skills": []}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

# Initialize DB on startup (background task in prod)
if VECTOR_SUPPORT:
    pass

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {
        "system": "Antigravity Prime",
        "version": "0.3.0",
        "interactive": True,
        "vector_memory": "active" if VECTOR_SUPPORT else "inactive (install requirements)"
    }

@app.post("/api/chat", response_model=ChatMessage)
async def chat_interaction(request: ChatRequest):
    """
    Core Interaction Loop:
    1. Receive User Message
    2. (Optional) Retrieve relevant context from Memory
    3. Process (Currently a simple Echo/Router simulation)
    4. Respond
    """
    user_text = request.message
    response_text = ""

    # Simple Keyword Routing Logic (Placeholder for LLM)
    if "remember" in user_text.lower():
        # Store in memory
        if VECTOR_SUPPORT:
            init_vector_db() # Lazy load
            collection = CHROMA_CLIENT.get_or_create_collection(name="antigravity_memory")
            embedding = EMBEDDING_MODEL.encode(user_text).tolist()
            collection.add(
                documents=[user_text],
                embeddings=[embedding],
                metadatas=[{"source": "chat", "timestamp": datetime.now().isoformat()}],
                ids=[f"mem_{datetime.now().timestamp()}"]
            )
            response_text = "🧠 I have stored that in my vector memory."
        else:
            response_text = "⚠️ Vector memory not available. Please install dependencies."
    
    elif "recall" in user_text.lower() or "what" in user_text.lower():
        # Retrieve from memory
        if VECTOR_SUPPORT:
            init_vector_db() # Lazy load
            collection = CHROMA_CLIENT.get_or_create_collection(name="antigravity_memory")
            embedding = EMBEDDING_MODEL.encode(user_text).tolist()
            results = collection.query(
                query_embeddings=[embedding],
                n_results=1
            )
            if results["documents"] and results["documents"][0]:
                memory = results["documents"][0][0]
                response_text = f"🔍 Found relevant memory: '{memory}'"
            else:
                response_text = "I couldn't find any relevant memories matching that."
        else:
            response_text = "⚠️ Vector memory not available."
    
    else:
        # Default Echo / Instruction
        response_text = f"Received: {user_text}\n(Try saying 'Remember [fact]' or 'Recall [fact]' to test memory.)"

    return ChatMessage(role="assistant", content=response_text)

@app.get("/api/skills", response_model=List[Skill])
def get_skills():
    data = load_registry()
    skills = []
    for s in data.get("skills", []):
        meta_path = os.path.join(ROOT_DIR, s["path"], "metadata.json")
        metadata = None
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r") as f:
                    metadata = json.load(f)
            except:
                pass
        
        skills.append(Skill(
            id=s["id"],
            category=s["category"],
            path=s["path"],
            enabled=s["enabled"],
            metadata=metadata
        ))
    return skills

@app.get("/api/health", response_model=SystemHealth)
def health_check():
    process = psutil.Process(os.getpid())
    return SystemHealth(
        status="operational",
        uptime_seconds=(datetime.now() - START_TIME).total_seconds(),
        cpu_usage=psutil.cpu_percent(),
        memory_usage=process.memory_info().rss / 1024 / 1024,
        platform=platform.system(),
        timestamp=datetime.now().isoformat(),
        vector_support=VECTOR_SUPPORT
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
