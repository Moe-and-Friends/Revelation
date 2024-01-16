
from enum import Enum

# Types of supported Actions. Usable as string objects.
class Action(str, Enum):
    BAN = "BAN"
    KICK = "KICK"
    DO_NOTHING = "DO_NOTHING"
    TIMEOUT = "TIMEOUT"