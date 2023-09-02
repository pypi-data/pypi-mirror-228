from flask import current_app


def get_db():
    return current_app.extensions['dh-potluck']._db


def is_truthy(value):
    if isinstance(value, str):
        return value.lower() in ['true', '1']
    return bool(value)
