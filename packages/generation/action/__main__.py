import random

from cerberus import Validator

from actions import Action
from intervals import convert_interval_str_to_minutes, convert_minutes_to_display_str
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

        lower_bound_str = action["timeout"]["lower_bound"]
        lower_bound_mins = convert_interval_str_to_minutes(lower_bound_str)

        upper_bound_str = action["timeout"]["upper_bound"]
        upper_bound_mins = convert_interval_str_to_minutes(upper_bound_str)

        timeout_duration_mins = random.randint(lower_bound_mins, upper_bound_mins)
        timeout_duration_str = convert_minutes_to_display_str(timeout_duration_mins)

        response_action.update(
            {"timeout": {
                "duration_mins": timeout_duration_mins,
                "duration_display_str": timeout_duration_str,
                "lower_bound_mins": lower_bound_mins,
                "lower_bound_display_str": action["timeout"]["lower_bound"],
                "upper_bound_mins": upper_bound_mins,
                "upper_bound_display_str": action["timeout"]["upper_bound"]}
            })

    return {
        "body": {
            "action": response_action,
            "metadata": response_metadata
        },
        "statusCode": 200
    }
