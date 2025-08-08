from src.db.db import connect_to_database


def create_users_table():
    """Creates the users table in the database if it does not exist."""
    connection, cursor = connect_to_database()
    create_table_cmd = """CREATE TABLE IF NOT EXISTS users(
        slack_id TEXT PRIMARY KEY, 
        so_id INTEGER NOT NULL,
        manager_id TEXT,
        ph INTEGER NOT NULL,
        FOREIGN KEY (manager_id) REFERENCES users(slack_id)
        )
        """
    cursor.execute(create_table_cmd)

    connection.commit()


def insert_user(slack_id: str, so_id: int, manager_id: str, ph: int):
    """Inserts a user into the users table.

    slack_id is their Slack user ID, and so_id is their Stack Overflow userID.
    """
    connection, cursor = connect_to_database()
    insert_cmd = "INSERT INTO users (slack_id, so_id, manager_id, ph) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_cmd, (slack_id, so_id, manager_id, ph))

    connection.commit()


def fetch_all_user_so_ids():
    """Fetches all Stack Overflow user IDs from the users table."""
    connection, cursor = connect_to_database(set_column_names=True)
    select_cmd = "SELECT slack_id, so_id FROM users"
    cursor.execute(select_cmd)
    results = cursor.fetchall()

    if not results:
        raise ValueError("No users found in the database.")

    return [dict(row) for row in results]


def fetch_random_user_slack_id():
    """Fetches a random Slack user ID from the users table."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT slack_id FROM users ORDER BY RANDOM() LIMIT 1"
    cursor.execute(select_cmd)
    result = cursor.fetchone()

    if not result:
        raise ValueError("No users found in the database.")

    return result[0]


def fetch_user_manager(slack_id: str) -> str:
    """Fetches the manager's Slack ID for a given user's Slack ID."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT manager_id FROM users WHERE slack_id = ?"
    cursor.execute(select_cmd, (slack_id,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"No user found with Slack ID '{slack_id}'.")

    return result[0]


def fetch_user_phone_number(slack_id: str) -> str:
    """Fetches the phone number for a given user's Slack ID."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT ph FROM users WHERE slack_id = ?"
    cursor.execute(select_cmd, (slack_id,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"No user found with Slack ID '{slack_id}'.")

    return result[0]


def fetch_all_user_slack_ids():
    """Fetches all Slack user IDs from the users table."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT slack_id FROM users"
    cursor.execute(select_cmd)
    results = cursor.fetchall()

    if not results:
        raise ValueError("No users found in the database.")

    return [row[0] for row in results]  # Return a list of Slack IDs
