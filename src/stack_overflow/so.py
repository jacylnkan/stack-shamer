import requests
import random

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
        return random.choice(data["items"]), tag

    raise Exception("No unanswered questions found for the tag.")


def fetch_user_id_from_username(username: str) -> str:
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
