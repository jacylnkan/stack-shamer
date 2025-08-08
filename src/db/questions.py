from src.db.db import connect_to_database


def create_questions_table():
    """Creates the questions table in the database if it does not exist."""
    connection, cursor = connect_to_database()
    create_table_cmd = """CREATE TABLE IF NOT EXISTS questions(
        qid INTEGER PRIMARY KEY, 
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        timestamp INTEGER NOT NULL, 
        escalation_lvl INTEGER DEFAULT 0,
        designated_answerer_id TEXT DEFAULT NULL,
        answered INTEGER DEFAULT 0,
        tag TEXT NOT NULL,
        FOREIGN KEY (designated_answerer_id) REFERENCES users(slack_id),
        FOREIGN KEY (tag) REFERENCES tags(tag)
        )
        """
    cursor.execute(create_table_cmd)

    connection.commit()


def insert_question(id: int, title: str, link: str, timestamp: int, tag: str):
    """Inserts a question into the questions table."""
    connection, cursor = connect_to_database()
    insert_cmd = "INSERT INTO questions (qid, title, link, timestamp, tag) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(insert_cmd, (id, title, link, timestamp, tag))

    connection.commit()


def check_if_question_exists(id: int) -> bool:
    """Checks if a question with the given ID already exists in the questions table."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT qid FROM questions WHERE qid = ?"
    cursor.execute(select_cmd, (id,))
    result = cursor.fetchone()

    return result is not None


def select_unanswered_question_ids():
    """Selects all unanswered questions IDs from the questions table."""
    connection, cursor = connect_to_database()
    select_cmd = "SELECT qid FROM questions WHERE answered = 0"
    cursor.execute(select_cmd)
    results = cursor.fetchall()

    return [row[0] for row in results] if results else []


def mark_question_as_answered(id: int):
    """Marks a question as answered in the questions table."""
    connection, cursor = connect_to_database()
    update_cmd = "UPDATE questions SET answered = 1 WHERE qid = ?"
    cursor.execute(update_cmd, (id,))

    connection.commit()


def increment_escalation_level(id: int) -> int:
    """Increments the escalation level of a question."""
    connection, cursor = connect_to_database()
    update_cmd = "UPDATE questions SET escalation_lvl = escalation_lvl + 1 WHERE qid = ?"
    cursor.execute(update_cmd, (id,))

    connection.commit()

    get_escalation_level_cmd = "SELECT escalation_lvl FROM questions WHERE qid = ?"
    result = cursor.execute(get_escalation_level_cmd, (id,)).fetchone()

    if not result:
        raise ValueError(f"Could not retrieve escalation level for question ID {id}.")

    return result[0]  # Return the updated escalation level


def select_question(id: int):
    """Selects a question by its ID."""
    connection, cursor = connect_to_database(set_column_names=True)
    select_cmd = "SELECT * FROM questions WHERE qid = ?"
    cursor.execute(select_cmd, (id,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"Question with ID {id} does not exist.")

    return dict(result)


def insert_designated_answerer(id: int, slack_id: str):
    """Inserts a designated answerer for a question."""
    connection, cursor = connect_to_database()
    update_cmd = "UPDATE questions SET designated_answerer_id = ? WHERE qid = ?"
    cursor.execute(update_cmd, (slack_id, id))

    connection.commit()


def set_question_as_wont_answer(id: int):
    """Marks a question as 'won't answer'."""
    connection, cursor = connect_to_database()
    update_cmd = "UPDATE questions SET answered = -1 WHERE qid = ?"
    cursor.execute(update_cmd, (id,))

    connection.commit()
