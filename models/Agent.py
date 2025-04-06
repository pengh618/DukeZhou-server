from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class Agent(BaseModel):
    id: str
    code:str
    title: str
    description: Optional[str] = None
    prompt: Optional[str] = None
    model_type: Optional[str] = None
    parameter_mode: str
    is_enabled: bool = True