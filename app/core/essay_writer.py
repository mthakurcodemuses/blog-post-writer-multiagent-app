from app.services.openai_service import OpenAIService
from app.services.tavily_service import TavilyService
from app.core.prompts import *
from app.models import AgentState, Queries

class EssayWriter:
    def __init__(self):
        self.openai = OpenAIService()
        self.tavily = TavilyService()

    async def generate_plan(self, task: str) -> str:
        """Generate essay plan"""
        return await self.openai.generate_completion(PLAN_PROMPT, task)

    async def generate_research_queries(self, task: str) -> Queries:
        """Generate research queries"""
        return await self.openai.generate_structured_output(
            RESEARCH_PLAN_PROMPT, 
            task,
            Queries
        )

    async def generate_critique_queries(self, critique: str) -> Queries:
        """Generate queries based on critique"""
        return await self.openai.generate_structured_output(
            RESEARCH_CRITIQUE_PROMPT,
            critique,
            Queries
        )

    async def generate_draft(self, task: str, plan: str, content: list[str]) -> str:
        """Generate essay draft"""
        content_text = "\n\n".join(content)
        user_message = f"{task}\n\nHere is my plan:\n\n{plan}"
        return await self.openai.generate_completion(
            WRITER_PROMPT.format(content=content_text),
            user_message
        )

    async def generate_critique(self, draft: str) -> str:
        """Generate essay critique"""
        return await self.openai.generate_completion(REFLECTION_PROMPT, draft)

    async def search_content(self, queries: list[str]) -> list[str]:
        """Search for content using queries"""
        return await self.tavily.search(queries)
