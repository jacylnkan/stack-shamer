import sqlite3

from src.utils.constants import DATABASE_NAME, DATABASE_LOCATION


def connect_to_database():
    """Connects to the SQLite database and returns the connection object."""
    connection = sqlite3.connect(f"{DATABASE_LOCATION}/{DATABASE_NAME}")
    cursor = connection.cursor()
    return connection, cursor
