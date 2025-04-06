from fastapi.routing import APIRouter
from core.supabase_db import db
from dao.AgentDao import AgentDao   

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
    

@router.get("/get_agent_by_code")
async def get_agent_by_code():
    try:
        agent_dao = AgentDao()
        code = "dream"
        agent = agent_dao.get_agent_by_code(code)
        if agent:
            return agent
        else:   
            return {"message": "No agent found"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "agent not found"}