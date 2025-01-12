from fastapi import APIRouter, HTTPException
from app.models.schemas import AgentState, AgentResponse, EssayRequest, EssayResponse
from app.core.writer import EssayWriter
from typing import Dict, Any
import uuid

router = APIRouter()
writer = EssayWriter()

@router.post("/generate", response_model=AgentResponse)
async def generate_essay(state: AgentState):
    """Generate or continue essay generation based on state"""
    try:
        response = await writer.graph.ainvoke(dict(state), {"configurable": {"thread_id": str(state.thread_id)}})
        return AgentResponse(
            state=response,
            node=response.get("lnode", ""),
            next_node=response.get("next", ""),
            revision=response.get("revision_number", 1)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state/{thread_id}")
async def get_state(thread_id: str):
    """Get current state for a thread"""
    try:
        state = writer.graph.get_state({"configurable": {"thread_id": thread_id}})
        return state.values
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"State not found: {str(e)}")

@router.post("/update_state")
async def update_state(thread_id: str, state: Dict[str, Any], node: str):
    """Update state for a thread"""
    try:
        writer.graph.update_state(
            {"configurable": {"thread_id": thread_id}}, 
            state,
            as_node=node
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))