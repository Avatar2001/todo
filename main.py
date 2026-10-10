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
