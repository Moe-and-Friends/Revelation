import random

from cerberus import Validator
from enum import Enum


# Types of supported Actions
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
    validator = Validator(REQUEST_SCHEMA, allow_unknown=True, require_all=True)
    validated = validator.validate(event)

    if validated:
        return {
            "statusCode": 200
        }

    return {
        "statusCode": 406,
        "body": {
            "errorMessage": validator.errors
        }
    }

    # action = random.choices(CONFIG, weights=WEIGHTS, k=1)# # #
    # return {
     #   "body": {"action": action},
     #   "statusCode": 200
    # }
