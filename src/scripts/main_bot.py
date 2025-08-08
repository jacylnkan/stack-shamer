import time
import schedule

from src.db.points import increment_points
from src.db.questions import insert_question, select_unanswered_question_ids, mark_question_as_answered, \
    increment_escalation_level, select_question
from src.db.users import fetch_all_user_so_ids
from src.slack.slack import post_question_to_slack, congratulate_user
from src.stack_overflow.so import fetch_question, fetch_owner_ids_from_responses, fetch_answers_for_question


def fetch_and_post_question():
    question, tag = fetch_question()

    timestamp = int(time.time())
    id, title, link = question["question_id"], question["title"], question["link"]

    insert_question(id=id, title=title, link=link, timestamp=timestamp, tag=tag)

    post_question_to_slack(question, tag=tag)

def escalate(qid: int):
    question = select_question(id=qid)
    new_escalation_lvl = increment_escalation_level(id=qid)

    post_question_to_slack(question=question, escalation_level=new_escalation_lvl)


def congratulate_user_and_add_point(slack_id: str):
    increment_points(slack_id=slack_id, year=time.localtime().tm_year, month=time.localtime().tm_mon)
    congratulate_user(slack_id=slack_id)


def check_for_responses():
    unanswered_questions = select_unanswered_question_ids()
    registered_users = fetch_all_user_so_ids()
    registered_user_so_ids = [user["so_id"] for user in registered_users]

    for question_id in unanswered_questions:
        # Check if the question has been answered by registered users
        # Answers will be sorted by votes - relevant when calculating points
        responses = fetch_answers_for_question(q_id=question_id)
        response_owner_ids = fetch_owner_ids_from_responses(responses=responses)

        answered = False

        for owner_id in response_owner_ids:
            if owner_id in registered_user_so_ids:
                mark_question_as_answered(id=question_id)
                answered = True
                answerer_slack_id = next(user["slack_id"] for user in registered_users if user["so_id"] == owner_id)
                congratulate_user_and_add_point(slack_id=answerer_slack_id)
                break

        if not answered:
            # If the question is still unanswered, escalate it
            escalate(qid=question_id)



fetch_and_post_question()
check_for_responses()

# schedule.every(5).minutes.do(fetch_and_post_question)
#
# while True:
#     schedule.run_pending()
#     time.sleep(60)
#