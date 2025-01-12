from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):
    task: str
    plan: Optional[str] = ""
    draft: Optional[str] = ""
    critique: Optional[str] = ""
    content: Optional[List[str]] = []
    queries: Optional[List[str]] = []
    revision_number: int = 1
    max_revisions: int = 2
    thread_id: Optional[str] = None
    lnode: Optional[str] = ""
    count: int = 0

class AgentResponse(BaseModel):
    state: Dict[str, Any]
    node: str
    next_node: str
    revision: int

class EssayRequest(BaseModel):
    topic: str
    max_revisions: int = 2

class EssayResponse(BaseModel):
    thread_id: str
    state: AgentState

class Queries(BaseModel):
    queries: List[str]