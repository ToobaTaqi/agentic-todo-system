"""
Script to verify the label column exists in the tasks table
"""
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

async def verify_label_column():
    # Create an async engine to connect to the database
    engine = create_async_engine(DATABASE_URL)

    try:
        async with engine.connect() as conn:
            # Check if the label column exists
            result = await conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'tasks' AND column_name = 'label';
            """))

            columns = result.fetchall()
            if columns:
                print(f"Label column exists: {columns[0]}")
            else:
                print("Label column does not exist in tasks table")

            # Show all columns in the tasks table
            result = await conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'tasks'
                ORDER BY ordinal_position;
            """))

            all_columns = result.fetchall()
            print("\nAll columns in tasks table:")
            for col in all_columns:
                print(f"  - {col[0]}: {col[1]}")

    except Exception as e:
        print(f"Error during verification: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(verify_label_column())