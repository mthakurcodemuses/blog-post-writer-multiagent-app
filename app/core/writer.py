from langgraph.graph import StateGraph
from app.services.llm import LLMService
from app.services.research import ResearchService
from typing import Dict, Any
import sqlite3

class EssayWriter:
    def __init__(self):
        self.llm = LLMService()
        self.research = ResearchService()
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the essay writing workflow graph"""
        builder = StateGraph(Dict[str, Any])
        
        # Add nodes
        builder.add_node("planner", self.llm.plan_node)
        builder.add_node("generate", self.llm.generation_node)
        builder.add_node("reflect", self.llm.reflection_node)
        builder.add_node("research_plan", self.research.research_plan_node)
        builder.add_node("research_critique", self.research.research_critique_node)

        # Set entry point
        builder.set_entry_point("planner")

        # Add edges
        builder.add_edge("planner", "research_plan")
        builder.add_edge("research_plan", "generate")
        builder.add_edge("reflect", "research_critique")
        builder.add_edge("research_critique", "generate")

        # Add conditional edges
        builder.add_conditional_edges(
            "generate",
            self._should_continue,
            {END: END, "reflect": "reflect"}
        )

        # Setup state persistence
        memory = SqliteSaver(conn=sqlite3.connect(":memory:", check_same_thread=False))
        
        return builder.compile(
            checkpointer=memory,
            interrupt_after=['planner', 'generate', 'reflect', 'research_plan', 'research_critique']
        )

    def _should_continue(self, state):
        """Determine if generation should continue"""
        if state["revision_number"] > state["max_revisions"]:
            return END
        return "reflect"
