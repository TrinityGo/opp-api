"""Test the database connection"""
# Standard imports
from backend.db import database

# Test the database connection
def test_database_connection():
    """Test the database connection"""
    assert database.engine is not None
    assert database.SessionLocal is not None
