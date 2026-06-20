import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Models


groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)