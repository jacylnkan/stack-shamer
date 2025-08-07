from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

from src.utils.constants import SLACK_TOKEN, CHANNEL_ID

log = logging.getLogger(__name__)

client = WebClient(token=SLACK_TOKEN)

def post_question_to_slack(question, tag):
    title = question["title"]
    link = question["link"]
    post_text = f"*Unanswered {tag} question!*\n>{title}\n🔗 <{link}|Answer it now!>"

    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=post_text)
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])