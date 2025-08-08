from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

from src.db.questions import insert_designated_answerer, set_question_as_wont_answer
from src.db.users import fetch_random_user_slack_id, fetch_user_manager, fetch_user_phone_number
from src.utils.constants import SLACK_TOKEN, CHANNEL_ID
from src.utils.twilio_utils import call_phone_number

log = logging.getLogger(__name__)

client = WebClient(token=SLACK_TOKEN)

def post_question_to_slack(question, escalation_level: int = 0, tag: str = None):
    post_text = modify_post_by_escalation_level(question, escalation_level, tag)

    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=post_text)
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])


def modify_post_by_escalation_level(question, escalation_level: int, tag: str = None) -> str:
    title = question["title"]
    link = question["link"]

    # Tag is provided in the function if this is the first time it has been posted
    # On repeated escalations, the tag is retrieved from the database
    if not tag:
        tag = question.get("tag", None)
        if not tag:
            raise ValueError("Tag is required but not provided in the question data.")

    # Friendly message on escalation level 0
    if escalation_level == 0:
        post_text = (f"*New unanswered `{tag}` question!*\n🆕🆕🆕\n>{title}\n🔗 <{link}|Be a helpful developer and "
                     f"answer it now!>")

    # More urgent message on escalation level 1
    elif escalation_level == 1:
        post_text = (f"*URGENT!*\n🛎️🛎️🛎️\nNo one has answered this `{tag}` question yet...\n>{title}\n"
                     f"🔗 <{link}|Don't let your team down and answer it now!>")

    # Tagging someone random on escalation level 2
    elif escalation_level == 2:
        question_id = question["qid"]
        random_user = fetch_random_user_slack_id()
        insert_designated_answerer(id=question_id, slack_id=random_user)

        post_text = (f"*IMPORTANT!!!*\n🚨🚨🚨\nBecause you all decided to ignore my previous posts, the gods have "
                     f"picked... <@{random_user}> to answer this `{tag}` question!>\n{title}\n🔗 <{link}|Answer it now "
                     f"or you'll regret it!>")

    # Tagging your manager on escalation level 3
    elif escalation_level == 3:
        designated_answerer_id = question.get("designated_answerer_id")
        if not designated_answerer_id:
            raise ValueError("Designated answerer not found in the question data.")

        manager = fetch_user_manager(slack_id=designated_answerer_id)

        post_text = (f"*YOU'RE IN TROUBLE!!!*\n🚓🚓🚓🚓🚓\nTagging your manager now since you can't seem to manage "
                     f"your own responsibilities. <{manager}>, your employee <@{designated_answerer_id}> is slacking "
                     f"off!!\n>{title}\n🔗 <{link}|Don't say I didn't warn you. Answer this `{tag}` question now.>")

    # Calling you on escalation level 4
    elif escalation_level == 4:
        designated_answerer_id = question.get("designated_answerer_id")
        if not designated_answerer_id:
            raise ValueError("Designated answerer not found in the question data.")

        phone_number = fetch_user_phone_number(slack_id=designated_answerer_id)
        call_phone_number(phone_number=phone_number)

        post_text = (f"*I'M CALLING YOU!!!*\n🆘☎️🆘☎️🆘\n<@{designated_answerer_id}>, you have been summoned to answer "
                     f"this `{tag}`question NOW!\n>{title}\n🔗 <{link}|PLEASEEEEE answer this!>")

    # Giving up and sending a sad message
    else:
        post_text = (f"*I give up...*\n💔💔💔\nMarking <{link}|this `{tag}` question> as 'won't answer' because no one "
                     f"seems to care.")
        set_question_as_wont_answer(id=question["qid"])

    return post_text


def congratulate_user(slack_id: str):
    post_text = (f"🎉🎉🎉🎉🎉🎉🎉🎉🎉\nCongratulations <@{slack_id}>! 🥳\nYou got a point for answering "
                 f"a StackOverflow question. Thank you for your contribution!\n🎉🎉🎉🎉🎉🎉🎉🎉🎉")

    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=post_text)
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])

