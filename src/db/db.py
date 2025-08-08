import sqlite3

from src.utils.constants import DATABASE_NAME, DATABASE_LOCATION


def connect_to_database(set_column_names: bool = False):
    """Connects to the SQLite database and returns the connection object."""
    connection = sqlite3.connect(f"{DATABASE_LOCATION}/{DATABASE_NAME}")

    if set_column_names:
        # Set the row factory to sqlite3.Row to access columns by name
        connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    return connection, cursor
