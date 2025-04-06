from fastapi.routing import APIRouter
from core.supabase_db import db

router = APIRouter()

@router.get("/query")
async def query():
    try:
        todos = db.from_("todos")\
            .select("id", "title", "is_complete")\
            .execute()
        if todos.data:
            return todos.data
        else:   
            return {"message": "No todos found"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "todos not found"}