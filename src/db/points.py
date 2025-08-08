from src.db.db import connect_to_database


def create_points_table():
    """Creates the points table in the database if it does not exist."""
    connection, cursor = connect_to_database()
    create_table_cmd = """CREATE TABLE IF NOT EXISTS points(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slack_id TEXT NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        points INTEGER NOT NULL DEFAULT 0,
        UNIQUE (slack_id, year, month),
        FOREIGN KEY (slack_id) REFERENCES users(slack_id)
        )"""
    cursor.execute(create_table_cmd)

    connection.commit()


def increment_points(slack_id: str, year: int, month: int):
    """Increments the points for a user in the points table by 1."""
    connection, cursor = connect_to_database()
    insert_cmd = """INSERT INTO points (slack_id, year, month, points) 
                    VALUES (?, ?, ?, 1) 
                    ON CONFLICT(slack_id, year, month) 
                    DO UPDATE SET points = points + 1"""
    cursor.execute(insert_cmd, (slack_id, year, month))

    connection.commit()

