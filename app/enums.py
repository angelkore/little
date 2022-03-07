from enum import Enum


class TapType(Enum):
    ON = "ON"
    OFF = "OFF"


class TripStatus(Enum):
    COMPLETE = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"
    CANCELLED = "CANCELLED"