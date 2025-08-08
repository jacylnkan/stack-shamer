from src.db.points import create_points_table
from src.db.questions import create_questions_table
from src.db.tags import create_tags_table
from src.db.users import create_users_table


def create_all_tables():
    create_tags_table()
    create_users_table()
    create_questions_table()
    create_points_table()

