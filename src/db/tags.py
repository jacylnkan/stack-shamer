from src.db.db import connect_to_database


def create_tags_table():
    """Creates the tags table in the database if it does not exist."""
    connection, cursor = connect_to_database()
    create_table_cmd = """CREATE TABLE IF NOT EXISTS tags(tag TEXT PRIMARY KEY)"""
    cursor.execute(create_table_cmd)

    connection.commit()


def insert_tag(tag: str):
    """Inserts a tag into the tags table."""
    connection, cursor = connect_to_database()
    insert_cmd = "INSERT INTO tags (tag) VALUES (?)"
    cursor.execute(insert_cmd, (tag,))

    connection.commit()

def select_random_tag() -> str:
    """Selects a random tag from the tags table."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT tag FROM tags ORDER BY RANDOM() LIMIT 1"
    cursor.execute(select_cmd)
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        raise ValueError("No tags found in the database.")


if __name__ == "__main__":
    # create_tags_table()
    # insert_tag("python")
    tag = select_random_tag()
    print(tag)

