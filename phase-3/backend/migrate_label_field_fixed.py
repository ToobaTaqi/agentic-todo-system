"""
Migration script to add the label column to the tasks table
"""
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

async def add_label_column():
    # Create an async engine to connect to the database
    engine = create_async_engine(DATABASE_URL)

    try:
        async with engine.connect() as conn:
            # Add the label column to the tasks table if it doesn't exist
            await conn.execute(text("""
                ALTER TABLE tasks ADD COLUMN IF NOT EXISTS label VARCHAR(50) DEFAULT NULL;
            """))
            await conn.commit()
            print("Successfully added label column to tasks table")

            # Add index for better performance
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_tasks_label ON tasks(label);
            """))
            await conn.commit()
            print("Successfully added index for label column")

    except Exception as e:
        print(f"Error during migration: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(add_label_column())