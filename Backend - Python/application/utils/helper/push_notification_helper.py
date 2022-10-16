import base64
from typing import List
from firebase_admin import messaging
from application.extensions import db, redisdb
from flask import current_app
from sqlalchemy.sql.expression import func


def send_push_notification(title: str, msg: str, registration_tokens: List[str] = None, to_all=True, data_object=None):
    tokens = []
    if registration_tokens:
        tokens = registration_tokens
        tokens = [base64.b64decode(token).decode() for token in tokens]
    elif to_all:
        with current_app.app_context():
            tokens = redisdb.mget(redisdb.keys("fcm_token:"+"*:*"))
            tokens = [base64.b64decode(token).decode() for token in tokens]
    else:
        print("Fail to push notification, there are no tokens to push to")
        return
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=data_object,
        tokens=tokens
    )
    print(tokens)
    messaging.send_multicast(message)
