
from actions import Action

# For performance and simplicity's sake, the configuration of chance is saved as "config as code".
# We can re-evaluate this approach in the future.

VERSION = "0.0.2"

ACTION_SETTINGS = [
    {
        "action": Action.TIMEOUT,
        "weight": 250,
        "timeout": {
            "lower_bound": "1m",
            "upper_bound": "1h"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 250,
        "timeout": {
            "lower_bound": "1h",
            "upper_bound": "2h"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 200,
        "timeout": {
            "lower_bound": "2h",
            "upper_bound": "4h"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 150,
        "timeout": {
            "lower_bound": "4h",
            "upper_bound": "6h"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 75,
        "timeout": {
            "lower_bound": "6h",
            "upper_bound": "12h"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 25,
        "timeout": {
            "lower_bound": "12h",
            "upper_bound": "1d",
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 25,
        "timeout": {
            "lower_bound": "1d",
            "upper_bound": "4d"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 24,
        "timeout": {
            "lower_bound": "4d",
            "upper_bound": "4w"
        }
    },
    {
        "action": Action.TIMEOUT,
        "weight": 1,
        "timeout": {
            "lower_bound": "4w",
            "upper_bound": "8w"
        }
    }
]

# Compute a list of weights for selection for the type of action to return.
ACTION_WEIGHTS = [action.get("weight", 0) for action in ACTION_SETTINGS]