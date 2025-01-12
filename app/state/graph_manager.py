from langgraph.graph import StateGraph, END
from typing import Dict, Any
import sqlite3
from app.core.essay_writer import EssayWriter
from app.models.schemas import AgentState
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class GraphManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.writer = EssayWriter()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the state graph for essay generation"""
        builder = StateGraph(Dict[str, Any])

        # Add nodes
        builder.add_node("planner", self._plan_node)
        builder.add_node("generate", self._generation_node) 
        builder.add_node("reflect", self._reflection_node)
        builder.add_node("research_plan", self._research_plan_node)
        builder.add_node("research_critique", self._research_critique_node)

        # Set entry point
        builder.set_entry_point("planner")

        # Add edges
        builder.add_conditional_edges(
            "generate",
            self._should_continue,
            {END: END, "reflect": "reflect"}
        )

        builder.add_edge("planner", "research_plan")
        builder.add_edge("research_plan", "generate")
        builder.add_edge("reflect", "research_critique")
        builder.add_edge("research_critique", "generate")

        return builder.compile()

    async def _plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate essay plan"""
        plan = await self.writer.generate_plan(state["task"])
        return {
            "plan": plan,
            "lnode": "planner",
            "count": state.get("count", 0) + 1
        }

    async def _research_plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Research for essay content"""
        queries = await self.writer.generate_research_queries(state["task"])
        content = await self.writer.search_content(queries.queries)
        return {
            "content": content,
            "queries": queries.queries,
            "lnode": "research_plan",
            "count": state.get("count", 0) + 1
        }

    async def _generation_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate essay draft"""
        draft = await self.writer.generate_draft(
            state["task"],
            state["plan"],
            state.get("content", [])
        )
        return {
            "draft": draft,
            "revision_number": state.get("revision_number", 0) + 1,
            "lnode": "generate",
            "count": state.get("count", 0) + 1
        }

    async def _reflection_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate essay critique"""
        critique = await self.writer.generate_critique(state["draft"])
        return {
            "critique": critique,
            "lnode": "reflect",
            "count": state.get("count", 0) + 1
        }

    async def _research_critique_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Research based on critique"""
        queries = await self.writer.generate_critique_queries(state["critique"])
        content = await self.writer.search_content(queries.queries)
        return {
            "content": content,
            "lnode": "research_critique",
            "count": state.get("count", 0) + 1
        }

    def _should_continue(self, state: Dict[str, Any]) -> str:
        """Determine if essay generation should continue"""
        if state["revision_number"] > state.get("max_revisions", 2):
            return END
        return "reflect"

    async def run_agent(self, initial_state: Dict[str, Any], thread: Dict[str, Any]):
        """Run the essay generation agent"""
        return await self.graph.ainvoke(initial_state, thread)

    def get_state(self, thread: Dict[str, Any]):
        """Get current state for thread"""
        return self.graph.get_state(thread)

    def get_state_history(self, thread: Dict[str, Any]):
        """Get state history for thread"""
        return self.graph.get_state_history(thread)