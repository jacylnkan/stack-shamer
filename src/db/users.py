from src.db.db import connect_to_database


def create_users_table():
    """Creates the users table in the database if it does not exist."""
    connection, cursor = connect_to_database()
    create_table_cmd = """CREATE TABLE IF NOT EXISTS users(slack_id TEXT PRIMARY KEY, so_id TEXT NOT NULL)"""
    cursor.execute(create_table_cmd)

    connection.commit()


def insert_user(slack_id: str, so_id: str):
    """Inserts a user into the users table.

    slack_id is their Slack user ID, and so_id is their Stack Overflow userID.
    """
    connection, cursor = connect_to_database()
    insert_cmd = "INSERT INTO users (slack_id, so_id) VALUES (?, ?)"
    cursor.execute(insert_cmd, (slack_id, so_id))

    connection.commit()
