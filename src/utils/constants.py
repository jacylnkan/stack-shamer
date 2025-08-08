import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_LOCATION = os.environ["DATABASE_LOCATION"]
DATABASE_NAME = "database.db"

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
