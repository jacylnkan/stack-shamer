from fastapi import FastAPI, Response
import uvicorn

app = FastAPI(title="Twilio API that serves TwiML files")


@app.post("/outbound_call")
def outbound_call():
    """
    Endpoint to handle outbound calls.
    Returns a TwiML response that instructs Twilio to read a message.
    """
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
          <Say voice="alice">Hello! This is an automated reminder. You need to answer the Stack Overflow question. 
          This is your last warning. Do not ignore this message, or face the consequences.</Say>
        </Response>"""
    return Response(content=xml_content, media_type="application/xml")


if __name__ == "__main__":
    uvicorn.run("twilio_app:app", host="0.0.0.0", port=8081, reload=True)
