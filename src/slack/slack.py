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
    blocks = modify_post_by_escalation_level(question, escalation_level, tag)

    try:
        client.chat_postMessage(channel=CHANNEL_ID, blocks=blocks)
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])

def generate_escalation_blocks(
    header: str,
    title: str,
    link: str,
    link_text: str,
    additional_text: str = None
) -> list[dict]:
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": header
            }
        },
        {
            "type": "divider"
        }]

    if additional_text:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": additional_text
            }
        })

    blocks += [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f">{title}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"🔗 <{link}|{link_text}>"
            }
        }
    ]

    return blocks


def modify_post_by_escalation_level(question, escalation_level: int, tag: str = None) -> list[dict]:
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
        blocks = generate_escalation_blocks(
            header=f"🆕 NEW Unanswered {tag} Question",
            title=title,
            link=link,
            link_text="Be a helpful developer and answer it now!"
        )

    # More urgent message on escalation level 1
    elif escalation_level == 1:
        blocks = generate_escalation_blocks(
            header=f"🛎️ URGENT! Question on {tag} needs your attention 🛎️",
            title=title,
            link=link,
            link_text="Don't let your team down and answer it now!",
            additional_text="This is your friendly reminder to answer this question before it escalates further!"
        )

    # Tagging someone random on escalation level 2
    elif escalation_level == 2:
        question_id = question["qid"]
        random_user = fetch_random_user_slack_id()
        insert_designated_answerer(id=question_id, slack_id=random_user)

        blocks = generate_escalation_blocks(
            header=f"🚨 IMPORTANT! Time is running out for this question 🚨",
            title=title,
            link=link,
            link_text="Answer it now or you'll regret it!",
            additional_text=f"Because you all decided to ignore my previous posts, the gods have picked... "
                            f"<@{random_user}> to answer this `{tag}` question!"
        )

    # Tagging your manager on escalation level 3
    elif escalation_level == 3:
        designated_answerer_id = question.get("designated_answerer_id")
        if not designated_answerer_id:
            raise ValueError("Designated answerer not found in the question data.")

        manager = fetch_user_manager(slack_id=designated_answerer_id)

        blocks = generate_escalation_blocks(
            header=f"⚡🚓⚡ YOU'RE IN TROUBLE! Question is still unanswered ⚡🚓⚡",
            title=title,
            link=link,
            link_text="Don't say I didn't warn you... answer this question ASAP!",
            additional_text=f"<{manager}>, your employee <@{designated_answerer_id}> is slacking off!"
        )

    # Calling you on escalation level 4
    elif escalation_level == 4:
        designated_answerer_id = question.get("designated_answerer_id")
        if not designated_answerer_id:
            raise ValueError("Designated answerer not found in the question data.")

        phone_number = fetch_user_phone_number(slack_id=designated_answerer_id)
        call_phone_number(phone_number=phone_number)

        blocks = generate_escalation_blocks(
            header=f"☎️🆘☎️️️ I'M CALLING YOU!!! ️🆘☎️🆘☎",
            title=title,
            link=link,
            link_text="PLEASEEEEE answer this!",
            additional_text=f"<@{designated_answerer_id}>, I'm resorting to calling you because this `{tag}` question is still unanswered!"
        )

    # Giving up and sending a sad message
    else:
        blocks = generate_escalation_blocks(
            header=f"Giving up on this question 💔",
            title=title,
            link=link,
            link_text=f"Marking this `{tag}` question as 'won't answer' because no one seems to care.",
            additional_text="Goodbye, Stack Overflow..."
        )
        set_question_as_wont_answer(id=question["qid"])

    return blocks


def congratulate_user(slack_id: str):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🎉🎉🎉 CONGRATULATIONS 🎉🎉🎉"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Congratulations <@{slack_id}>! 🥳\nYou got a point for answering a StackOverflow question. "
                        f"Thank you for your contribution!"
            }
        }
    ]

    try:
        client.chat_postMessage(channel=CHANNEL_ID, blocks=blocks)
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])


def post_leaderboard(sorted_leaderboard: list[tuple], date: str):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🏆🏆🏆 {date} LEADERBOARD 🏆🏆🏆"
            }
        },
        {
            "type": "divider"
        }
    ]

    emojis = ["🥇", "🥈", "🥉"]
    for i in range(len(emojis)):
        try:
            current = sorted_leaderboard[i]
            text = f"{emojis[i]} <@{current[0]}> with {current[1]} points"
        except IndexError:
            text = f"{emojis[i]}❌ No one else has answered questions yet 😭"

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        })

    try:
        client.chat_postMessage(
            channel=CHANNEL_ID,
            blocks=blocks
        )
    except SlackApiError as e:
        log.error("Slack error:", e.response["error"])
