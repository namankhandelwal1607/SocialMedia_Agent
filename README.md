Phase 1: Project Setup

Since you're already using WSL, I recommend doing everything inside WSL.

Create Project
mkdir auriga-social-ai
cd auriga-social-ai
Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
Install Core Dependencies
pip install langgraph
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install langchain-core
pip install langsmith

pip install tavily-python
pip install beautifulsoup4
pip install faiss-cpu
pip install sentence-transformers

pip install fastapi
pip install uvicorn

pip install python-dotenv
pip install pydantic
Create Structure
auriga-social-ai/

├── agents/
│   ├── supervisor.py
│   ├── trend_agent.py
│   ├── knowledge_agent.py
│   ├── strategy_agent.py
│   ├── content_agent.py
│   ├── compliance_agent.py
│
├── tools/
│   ├── web_search.py
│   ├── rag_tool.py
│
├── data/
│   ├── auriga_docs/
│
├── graph/
│   ├── state.py
│   ├── workflow.py
│
├── app.py
├── .env
└── requirements.txt
Phase 2: Build Version 1 (Core Workflow)

Don't build publishing, analytics, scheduling, Instagram, LinkedIn APIs initially.

Build this flow:

User
 ↓
Supervisor
 ↓
Trend Agent
 ↓
Knowledge Agent
 ↓
Strategy Agent
 ↓
Content Agent
 ↓
Compliance Agent
 ↓
Output

No human approval yet.

Goal:

Input:

Find trending AI topics and generate a LinkedIn post.

Output:

Trending Topic:
Multi-Agent Systems

Auriga Angle:
Enterprise AI Automation

LinkedIn Post:
...

If this works, you've already demonstrated LangGraph multi-agent orchestration.

Phase 3: Create State

graph/state.py

from typing import TypedDict

class GraphState(TypedDict):
    user_query: str

    trend_data: str

    company_context: str

    strategy: str

    generated_content: str

    compliance_feedback: str

    final_output: str

This alone demonstrates State Management.

Phase 4: Build Trend Discovery Agent

Create a web search tool.

Initially use Tavily.

@tool
def search_trends(query: str):
    ...

Agent responsibility:

Input:
Find trending AI topics

Output:
1. Agentic AI
2. MCP
3. AI Coding Agents
4. Multi-Agent Systems
Phase 5: Build Auriga Knowledge Agent

Now implement RAG.

Collect:

Auriga website pages
Blogs
Service pages

Store them in:

data/auriga_docs/

Create:

FAISS
Sentence Transformers

Pipeline:

Documents
↓
Chunking
↓
Embeddings
↓
FAISS
↓
Retriever

Agent retrieves relevant company information.

Example:

Trend:
Agentic AI

Retrieved:
Auriga provides AI consulting,
custom software solutions,
digital transformation.

Now you've demonstrated RAG.

Phase 6: Strategy Agent

Input:

Trend = Agentic AI

Auriga Context = AI consulting

Output:

Target Audience:
CTOs

Platform:
LinkedIn

Angle:
How enterprises can adopt
multi-agent systems.

This is just an LLM node.

Phase 7: Content Generation Agent

Generate:

class SocialPost(BaseModel):
    title: str
    content: str
    hashtags: list[str]

Use structured output.

Now you demonstrate:

Structured Output
Pydantic Models
Phase 8: Compliance Agent

Input:

Generated Content

Check:

professionalism
factual claims
tone

Output:

APPROVED

or

REVISE

Add conditional edge.

if approved:
    END

else:
    Content Agent

Now you've demonstrated Conditional Routing.

Phase 9: Add Human Approval (Interrupts)

This is where LangGraph becomes impressive.

Flow:

Content Agent
↓
Interrupt
↓
Human Review
↓
Resume Graph

Example:

from langgraph.types import interrupt
feedback = interrupt(
    {
        "post": generated_post
    }
)

User can:

approve

or

modify hashtags

Resume execution afterward.

This demonstrates:

Human-in-the-Loop
Interrupts
Checkpointing
Phase 10: Add Memory

Store:

Previous Posts
Brand Guidelines
User Preferences

Use:

MemorySaver()

or

Postgres Checkpointer

Now the agent remembers:

Don't use excessive emojis
Prefer LinkedIn content
Focus on AI topics
Phase 11: Add Streaming

Stream outputs while content is being generated.

graph.stream(...)

Show:

Trend Agent Running...
Knowledge Agent Running...
Generating Content...

This looks great during demos.

Phase 12: Add Publishing Agent

Only after everything above works.

Create tools:

post_to_linkedin()
post_to_twitter()

Initially mock them:

Posted Successfully

You don't need real LinkedIn/Twitter integration for the internship demo.

Phase 13: Add Analytics Agent

Simplified version:

Store posts in SQLite.

Post
Date
Platform
Likes
Comments
Impressions

Analytics Agent can answer:

What topics perform best?

using SQL queries.

Recommended MVP

If I were building this for a mentor demo, I'd stop after:

✅ Supervisor Agent
✅ Trend Agent
✅ Knowledge Agent (RAG)
✅ Strategy Agent
✅ Content Agent
✅ Compliance Agent
✅ Human Approval Interrupt
✅ MemorySaver Checkpointer
✅ Streaming

That already covers almost every major LangGraph concept and is more than enough for a strong internship project. After that, you can add publishing and analytics as bonus features.






For this project:

Agent	Model
Trend Agent	Gemini
Knowledge Agent	Gemini
Strategy Agent	Groq
Content Agent	Groq
Compliance Agent	Groq
Supervisor	Groq