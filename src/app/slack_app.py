import re

from fastapi import FastAPI, Form
import uvicorn

from src.db.tables import create_all_tables
from src.db.tags import insert_tag
from src.db.users import insert_user
from src.stack_overflow.so import fetch_user_id_from_username

app = FastAPI(title="Stack Shamer API")

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a simple message indicating the API is healthy.
    """
    return {"message": "API is healthy!!"}


@app.post("/add_tag")
def add_tag(text: str = Form(...)):
    """Endpoint to add a tag to the database."""
    tag = text.strip()

    # Check if there are whitespaces in tag
    if " " in tag:
        return {
            "response_type": "ephemeral",
            "text": "Tag cannot contain whitespace. Please try again.",
        }

    insert_tag(tag)
    return {
        "response_type": "ephemeral",
        "text": f"Tag `{tag}` has been added successfully.",
    }


@app.post("/add_user")
def add_user(text: str = Form(...), user_id: str = Form(...)):
    slack_id = user_id.strip()

    info = text.strip()
    matches = re.findall(r'(\w+):\s*(\S+)', info)

    required_keys = {"so_username", "manager", "ph"}
    parsed_data = {key: value.strip('"') for key, value in matches}
    missing = required_keys - parsed_data.keys()
    if missing:
        return {
            "response_type": "ephemeral",
            "text": f"Missing required fields: {', '.join(missing)}. Please try again.",
        }

    # Get SO user ID
    user_id = fetch_user_id_from_username(username=parsed_data["so_username"])

    insert_user(slack_id=slack_id, so_id=user_id, manager_id=parsed_data["manager"], ph=parsed_data["ph"])
    return {
        "response_type": "in_channel",
        "text": f"User `{parsed_data['so_username']}` has been added successfully! You will now be forced to answer Stack Overflow questions forever.",
    }


if __name__ == "__main__":
    # Create all DB tables
    create_all_tables()

    uvicorn.run("slack_app:app", host="0.0.0.0", port=8080, reload=True)