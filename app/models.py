from typing import List, Optional
from pydantic import BaseModel

class Queries(BaseModel):
    queries: List[str]

class AgentState(BaseModel):
    task: str
    plan: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    content: List[str] = []
    queries: List[str] = []
    revision_number: int = 0
    max_revisions: int = 2
    lnode: str = ""
    count: int = 0

class EssayRequest(BaseModel):
    topic: str
    max_revisions: int = 2

class EssayResponse(BaseModel):
    thread_id: str
    state: AgentState
