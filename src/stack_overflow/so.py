import requests
import random

from src.db.questions import check_if_question_exists
from src.db.tags import select_random_tag


def fetch_question():
    tag = select_random_tag()

    url = "https://api.stackexchange.com/2.3/questions/unanswered"
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": 10
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if "items" in data:
        random_q = random.choice(data["items"])

        # Checks if we have already posted this question
        if check_if_question_exists(id=random_q["question_id"]):
            return fetch_question()

        return random_q, tag

    raise Exception("No unanswered questions found for the tag.")


def fetch_user_id_from_username(username: str) -> int:
    """Fetches the Stack Overflow user ID from their username."""
    url = "https://api.stackexchange.com/2.3/users"
    params = {
        "order": "desc",
        "sort": "name",
        "inname": username,
        "site": "stackoverflow"
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    if "items" in data and len(data["items"]) > 0:
        for item in data["items"]:
            if item["display_name"].lower() == username.lower():
                return str(item["user_id"])

    raise ValueError(f"User '{username}' not found on Stack Overflow.")


def fetch_answers_for_question(q_id: int):
    """Fetches answers for a given question ID. Sorted by votes in descending order."""
    url = f"https://api.stackexchange.com/2.3/questions/{q_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow"
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    if "items" in data:
        return data["items"]

    return []  # No answers found


def fetch_owner_ids_from_responses(responses: list[dict]) -> list[int]:
    """Extracts owner IDs from a list of Stack Overflow responses."""
    owner_ids = []
    for response in responses:
        if "owner" in response and "user_id" in response["owner"]:
            owner_ids.append(response["owner"]["user_id"])
    return owner_ids

