from core.supabase_db import db

class AgentDao:
    def __init__(self):
        self.table_name = "agent"

    async def get_all_agents(self):
        response = (
            db.from_(self.table_name)
            .select("*")
            .execute()
        )
        return response.data

    async def get_prompt_by_code(self, code):
        response = (
            db.from_(self.table_name)
            .select("*")
            .eq("code", code)
            .execute()  
        )

        # print(f"Response: {response.data[0].get('prompt')}")
        return response.data[0].get('prompt') if response.data else None
        