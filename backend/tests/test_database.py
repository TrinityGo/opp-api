from db import database

def test_database_connection():
    assert database.engine is not None
    assert database.SessionLocal is not None