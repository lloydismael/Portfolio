"""
Azure Functions (Python) HTTP trigger for the portfolio contact form.

Route (via Static Web Apps):  POST /api/contact
Body (JSON): { "name": "...", "email": "...", "message": "..." }

By default this validates and logs the message. To actually deliver mail, set
either:
  * ACS_CONNECTION_STRING + SENDER_ADDRESS + TO_ADDRESS   (Azure Communication Services), or
  * plug in your own provider in `deliver()`.
"""
import json
import logging
import os
import re

import azure.functions as func

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def deliver(name: str, email: str, message: str) -> None:
    """Send the message. No-op unless Azure Communication Services is configured."""
    conn = os.environ.get("ACS_CONNECTION_STRING")
    sender = os.environ.get("SENDER_ADDRESS")
    to = os.environ.get("TO_ADDRESS")
    if not (conn and sender and to):
        logging.info("ACS not configured; message logged only.")
        return
    try:
        from azure.communication.email import EmailClient  # type: ignore

        client = EmailClient.from_connection_string(conn)
        client.begin_send({
            "senderAddress": sender,
            "recipients": {"to": [{"address": to}]},
            "content": {
                "subject": f"Portfolio enquiry from {name}",
                "plainText": f"From: {name} <{email}>\n\n{message}",
            },
        })
    except Exception as exc:  # pragma: no cover
        logging.exception("Email delivery failed: %s", exc)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return _json({"error": "Invalid JSON"}, 400)

    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip()
    message = (body.get("message") or "").strip()

    if not name or not message or not EMAIL_RE.match(email):
        return _json({"error": "Please provide a name, valid email and message."}, 400)
    if len(message) > 5000:
        return _json({"error": "Message too long."}, 400)

    logging.info("Contact form: %s <%s>", name, email)
    deliver(name, email, message)
    return _json({"ok": True, "message": "Message received. I'll get back to you soon."}, 200)


def _json(payload: dict, status: int) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(payload),
        status_code=status,
        mimetype="application/json",
    )
