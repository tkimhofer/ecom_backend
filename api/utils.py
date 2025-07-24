from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.db import engine

def check_db_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print("Database error:", e)
        return False
