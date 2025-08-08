from twilio.rest import Client

from src.utils.constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def call_phone_number(phone_number: str):
    """
    Initiates a call to the specified phone number using Twilio.
    """
    try:
        call = client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url="https://929c40cc75ff.ngrok-free.app/outbound_call"  # URL for TwiML instructions
        )
        return call.sid
    except Exception as e:
        print(f"Failed to make a call: {e}")
        return None

