from core.supabase_db import db

class AgentDao:
    def __init__(self):
        self.table_name = "agent"

    def get_all_agents(self):
        response = (
            db.from_(self.table_name)
            .select("*")
            .execute()
        )
        return response.data

    def get_agent_by_code(self, code):
        response = (
            db.from_(self.table_name)
            .select("*")
            .eq("code", code)
            .execute()
        )
        return response.data