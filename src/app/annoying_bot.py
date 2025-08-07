import time
import schedule

from src.slack.slack import post_question_to_slack
from src.stack_overflow.so import fetch_question


def fetch_and_post_question():
    question, tag = fetch_question()
    post_question_to_slack(question, tag)


fetch_and_post_question()
# schedule.every(5).minutes.do(fetch_and_post_question)
#
# while True:
#     schedule.run_pending()
#     time.sleep(60)
#
