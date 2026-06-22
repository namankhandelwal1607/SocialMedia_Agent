from langchain_core.tools import tool
import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

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
        print(
            f"\nDOC {i+1} SIZE:",
            len(doc.page_content)
        )

    return "\n\n".join(
        doc.page_content[:500]
        for doc in docs
    )