from pydantic import BaseModel

class Todo(BaseModel):
    id: int 
    title: str
    is_complete: str
    created_at: str