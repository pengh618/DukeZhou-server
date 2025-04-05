from supabase import Client, create_client
import os

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def create_supabase_client():
    print("Creating Supabase client...")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be provided.")
    supabase: Client = create_client(url, key)
    return supabase

# Initialize supabase client
db = create_supabase_client()

# response = (
#     db.table("todos")
#     .select("*")
#     .execute()
# )

# for todo in response.data:
#     print(todo)