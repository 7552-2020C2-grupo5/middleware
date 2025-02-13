import logging
import requests
import os

from bookbnb_middleware.exceptions import InvalidEnvironment, ServerTokenError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _patch_env_vars(env_vars):
    heroku_app = os.getenv("HEROKU_APP_NAME", None)
    heroku_api_key = os.getenv("HEROKU_API_KEY", None)
    result = requests.patch(
        f"https://api.heroku.com/apps/{heroku_app}/config-vars",
        json=env_vars,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.heroku+json; version=3",
            "Authorization": f"Bearer {heroku_api_key}",
        },
    )
    result.raise_for_status()


def add_env_var(key, val):
    if os.getenv("ENV", "DEV") == "DEV":
        raise InvalidEnvironment
    try:
        env_vars = {key.upper(): val}
        _patch_env_vars(env_vars)
    except Exception as e:
        raise ServerTokenError from e


def remove_env_var(key):
    if os.getenv("ENV", "DEV") == "DEV":
        raise InvalidEnvironment
    try:
        env_vars = {key.upper(): "_"}
        _patch_env_vars(env_vars)
    except Exception as e:
        raise ServerTokenError from e
