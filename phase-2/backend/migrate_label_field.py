"""
Migration script to add the label column to the tasks table
"""
import asyncio
import asyncpg
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

async def add_label_column():
    # Extract the sync database URL (remove asyncpg part)
    sync_db_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    # Connect to the database directly with asyncpg
    conn = await asyncpg.connect(DATABASE_URL.replace("postgresql+asyncpg://", "").replace("postgresql://", ""))

    try:
        # Add the label column to the tasks table
        await conn.execute("""
            ALTER TABLE tasks ADD COLUMN IF NOT EXISTS label VARCHAR(50) DEFAULT NULL;
        """)
        print("Successfully added label column to tasks table")

        # Add index for better performance
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_label ON tasks(label);
        """)
        print("Successfully added index for label column")

    except Exception as e:
        print(f"Error during migration: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(add_label_column())