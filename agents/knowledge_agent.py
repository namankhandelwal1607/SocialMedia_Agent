from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from config import gemini_llm
import os

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTORSTORE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "vectorstore",
    "auriga"
)

vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 5
    }
)

@tool
def auriga_search(query: str):
    """
    Search Auriga knowledge base.
    """

    docs = retriever.invoke(query)

    print("\nRETRIEVED DOCS:", len(docs))

    for i, doc in enumerate(docs):
        print(f"\nDOC {i+1} SIZE:", len(doc.page_content))

    return "\n\n".join(
        doc.page_content[:500]
        for doc in docs
    )

from langchain.agents import create_agent

knowledge_agent = create_agent(
    model=gemini_llm,
    tools=[auriga_search],
    system_prompt="""
    You are Auriga's Knowledge Agent.

Use the knowledge base and return ONLY:

1. Relevant Auriga services
2. Relevant expertise
3. Relevant case studies
4. Why this trend matches Auriga

Keep response under 300 words.

    Always use the knowledge base.
    """
)