from tavily import TavilyClient
from app.core.config import settings
from app.models.schemas import Queries
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can
be used when writing the following essay. Generate a list of search queries that will gather
any relevant information. Only generate 3 queries max."""

RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can
be used when making any requested revisions (as outlined below).
Generate a list of search queries that will gather any relevant information.
Only generate 2 queries max."""

class ResearchService:
    def __init__(self):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0
        )

    def research_plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        queries = self.model.with_structured_output(Queries).invoke([
            SystemMessage(content=RESEARCH_PLAN_PROMPT),
            HumanMessage(content=state['task'])
        ])
        content = state['content'] or []
        for q in queries.queries:
            response = self.tavily.search(query=q, max_results=2)
            for r in response['results']:
                content.append(r['content'])
        return {
            "content": content,
            "queries": queries.queries,
            "lnode": "research_plan",
            "count": 1
        }

    def research_critique_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        queries = self.model.with_structured_output(Queries).invoke([
            SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
            HumanMessage(content=state['critique'])
        ])
        content = state['content'] or []
        for q in queries.queries:
            response = self.tavily.search(query=q, max_results=2)
            for r in response['results']:
                content.append(r['content'])
        return {
            "content": content,
            "lnode": "research_critique",
            "count": 1
        }
