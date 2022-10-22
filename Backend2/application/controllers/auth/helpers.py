"""Various helpers for auth. Mainly about tokens blocklisting

Heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime
import os
from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound
import json
from application.extensions import db
# from application.models import TokenBlocklist
import redis
# from bson import loads, dumps


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return (str(z))
        else:
            return super().default(z)


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.

    :param identity_claim: configured key to get nhan_vien identity
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    dbRedis = {
        "jti": jti,
        "token_type": token_type,
        "user_id": user_identity,
        "expires": expires,
        "revoked": revoked,
    }


    # db_token = TokenBlocklist(
    #     jti=jti,
    #     token_type=token_type,
    #     user_id=user_identity,
    #     expires=expires,
    #     revoked=revoked,
    # )
    # db.session.add(db_token)
    # db.session.commit()

def to_dict(row):
    d = {}
    for column in row.__table__.columns:
        if str(getattr(row, column.name)) == 'None':
            d[column.name] = None
        else:
            d[column.name] = str(getattr(row, column.name))

    return d
