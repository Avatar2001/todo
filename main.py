from fastapi import FastAPI
from db import get_connection
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "lol"}

@app.get("/db-test")
def test_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()

    return {
        "database_connected": True,
        "postgresql_version": result[0],
    }


@app.get("/todos/{user_id}")
def get_todos(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
SELECT id, title, description, is_done, priority, due_date, created_at
                FROM todos
                WHERE user_id = %s
                ORDER BY created_at DESC;

                """,
                (user_id,),

            )
            rows=cur.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "is_done": row[3],
            "priority": row[4],
            "due_date": row[5],
            "created_at": row[6],
        }
        for row in rows
    ]




