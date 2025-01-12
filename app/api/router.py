from fastapi import APIRouter, HTTPException
from app.models import EssayRequest, EssayResponse, AgentState
from app.state.graph_manager import GraphManager
from typing import Dict, Any
import uuid

router = APIRouter()
graph_manager = GraphManager()

@router.post("/essay", response_model=EssayResponse)
async def create_essay(request: EssayRequest):
    """Start essay generation process"""
    try:
        thread_id = str(uuid.uuid4())
        thread = {"configurable": {"thread_id": thread_id}}
        
        initial_state = {
            "task": request.topic,
            "max_revisions": request.max_revisions,
            "revision_number": 0,
            "content": [],
            "lnode": "",
            "count": 0
        }
        
        state = await graph_manager.run_agent(initial_state, thread)
        
        return EssayResponse(
            thread_id=thread_id,
            state=AgentState(**state)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/essay/{thread_id}/continue")
async def continue_essay(thread_id: str):
    """Continue essay generation for existing thread"""
    try:
        thread = {"configurable": {"thread_id": thread_id}}
        state = await graph_manager.run_agent(None, thread)
        return {"state": state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/essay/{thread_id}/state")
async def get_essay_state(thread_id: str):
    """Get current state of essay generation"""
    try:
        thread = {"configurable": {"thread_id": thread_id}}
        state = graph_manager.get_state(thread)
        return {"state": state.values}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/essay/{thread_id}/history")
async def get_essay_history(thread_id: str):
    """Get history of essay generation states"""
    try:
        thread = {"configurable": {"thread_id": thread_id}}
        history = list(graph_manager.get_state_history(thread))
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
