import random

from cerberus import Validator

from actions import Action
from settings import ACTION_SETTINGS, ACTION_WEIGHTS, VERSION

# Cerberus Schema
REQUEST_SCHEMA = {
    'supported_actions': {
        'type': 'list',
        'allowed': [Action.TIMEOUT, Action.KICK, Action.BAN, Action.DO_NOTHING],
        'required': False,
    },
    'metadata': {
        'type': 'dict',
        'required': False,
        'schema': {
            'user_id': {'type': 'integer', 'required': False},
            'guild_id': {'type': 'integer', 'required': False},
            'channel_id': {'type': 'integer', 'required': False}
        }
    }
}

def main(event):
    validator = Validator(REQUEST_SCHEMA, allow_unknown=True, require_all=True)
    if not validator.validate(event):
        return {
            "body": {"error": validator.errors},
            "statusCode": 406
        }

    response_metadata = {
        "is_manual_value": False,
        "version": VERSION
    }

    action = random.choices(ACTION_SETTINGS, weights=ACTION_WEIGHTS, k=1)[0]

    response_action = {
        "type": action["action"]
    }
    if action["action"] == Action.TIMEOUT:
        response_action.update(
            {"timeout": {
                "lower_bound_str": action["timeout"]["lower_bound"],
                "upper_bound_str": action["timeout"]["upper_bound"]}
            })

    return {
        "body": {
            "action": response_action,
            "metadata": response_metadata
        },
        "statusCode": 200
    }
