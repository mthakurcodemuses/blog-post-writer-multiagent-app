from langchain_openai import ChatOpenAI
from app.config import get_settings
from langchain_core.messages import SystemMessage, HumanMessage

class OpenAIService:
    def __init__(self):
        settings = get_settings()
        self.model = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0, 
            api_key=settings.OPENAI_API_KEY
        )

    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Generate completion using OpenAI"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response = await self.model.ainvoke(messages)
        return response.content

    async def generate_structured_output(self, system_prompt: str, user_prompt: str, output_class):
        """Generate structured output using output_class schema"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        return await self.model.with_structured_output(output_class).ainvoke(messages)
