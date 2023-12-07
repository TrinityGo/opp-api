"""
Database Initialization Module

This module initializes the database for the application. It sets up the database engine
that will be used to interact with the database.

Attributes:
    - engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine for connecting to the database.

Example:
    Import the `db` package and access the `engine` attribute:

    ```python
    from backend.db import engine

    # Now you can use the `engine` to interact with the database.
    ```

Note:
    Make sure to configure the database connection details before using the `engine`.

"""
from backend.db.database import engine
