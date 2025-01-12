from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from typing import Dict, Any

PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of a short 3 paragraph essay. 
Write such an outline for the user provided topic. Give the three main headers of an outline of 
the essay along with any relevant notes or instructions for the sections."""

WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 3 paragraph essays.
Generate the best essay possible for the user's request and the initial outline.
If the user provides critique, respond with a revised version of your previous attempts.
Utilize all the information below as needed:

------

{content}"""

REFLECTION_PROMPT = """You are a teacher grading an 3 paragraph essay submission.
Generate critique and recommendations for the user's submission.
Provide detailed recommendations, including requests for length, depth, style, etc."""

class LLMService:
    def __init__(self):
        self.model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-3.5-turbo", 
            temperature=0
        )

    def plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        messages = [
            SystemMessage(content=PLAN_PROMPT),
            HumanMessage(content=state['task'])
        ]
        response = self.model.invoke(messages)
        return {
            "plan": response.content,
            "lnode": "planner",
            "count": 1
        }

    def generation_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        content = "\n\n".join(state['content'] or [])
        user_message = HumanMessage(
            content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}"
        )
        messages = [
            SystemMessage(
                content=WRITER_PROMPT.format(content=content)
            ),
            user_message
        ]
        response = self.model.invoke(messages)
        return {
            "draft": response.content,
            "revision_number": state.get("revision_number", 1) + 1,
            "lnode": "generate",
            "count": 1
        }

    def reflection_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        messages = [
            SystemMessage(content=REFLECTION_PROMPT),
            HumanMessage(content=state['draft'])
        ]
        response = self.model.invoke(messages)
        return {
            "critique": response.content,
            "lnode": "reflect",
            "count": 1
        }
