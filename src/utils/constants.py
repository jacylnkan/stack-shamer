import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_LOCATION = "/home/jackie/etb/stack-shamer/src/db"
DATABASE_NAME = "database.db"

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
