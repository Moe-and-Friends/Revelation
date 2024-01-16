import random

from cerberus import Validator
from enum import Enum


# Types of supported Actions. Usable as string objects.
class Action(str, Enum):
    BAN = "BAN"
    KICK = "KICK"
    DO_NOTHING = "DO_NOTHING"
    TIMEOUT = "TIMEOUT"


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

CONFIG = [
    {
        "action": Action.TIMEOUT,
        "weight": 999,
        "timeout": {
            "lower_bound": "1m",
            "upper_bound": "20m"
        }
    },
    {
        "action": Action.KICK,
        "weight": 1,
    }
]

# Compute a list of weights for selection for the type of action to return.
WEIGHTS = [action.get("weight", 0) for action in CONFIG]


def main(event):
    # Validate for correct data.
    validator = Validator(REQUEST_SCHEMA, allow_unknown=True, require_all=True)
    if not validator.validate(event):
        return {
            "body": {"error": validator.errors},
            "statusCode": 406
        }

    action = random.choices(CONFIG, weights=WEIGHTS, k=1)# # #
    return {
        "body": {"action": action},
        "statusCode": 200
    }
