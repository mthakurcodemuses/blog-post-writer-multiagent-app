from tavily import TavilyClient
from app.config import get_settings

class TavilyService:
    def __init__(self):
        settings = get_settings()
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    async def search(self, queries: list[str], max_results: int = 2) -> list[str]:
        """Search using Tavily and return content"""
        content = []
        for query in queries:
            response = await self.client.search(query=query, max_results=max_results)
            for r in response['results']:
                content.append(r['content'])
        return content
