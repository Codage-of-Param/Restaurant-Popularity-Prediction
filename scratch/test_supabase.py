import os
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path

def test_connection():
    env_path = Path(".env")
    load_dotenv(env_path)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
        return

    try:
        supabase = create_client(url, key)
        # Try to list buckets
        buckets = supabase.storage.list_buckets()
        print(f"Connection Successful! Found {len(buckets)} buckets.")
        for b in buckets:
            print(f"- Bucket: {b.name}")
            
        # Try to check if 'predictions' table exists
        # We can do this by trying to select 0 rows
        try:
            res = supabase.table("predictions").select("id").limit(1).execute()
            print("Table 'predictions' exists.")
        except Exception as e:
            print(f"Table 'predictions' check failed: {e}")

    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
