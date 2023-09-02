from flask import current_app
from werkzeug.local import LocalProxy


def __get_current_settings():
    if current_app:
        return current_app.config.get("SETTINGS", {})

    # Raise a 'Working outside of application context.' error
    return current_app.config


def _get_current_settings():
    return __get_current_settings()


# A level of indirection is needed for the mock to work.
# pylint: disable=unnecessary-lambda
current_settings = LocalProxy(lambda: _get_current_settings())
