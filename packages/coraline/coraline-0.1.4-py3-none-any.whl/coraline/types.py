from enum import Enum


class BillingMode(str, Enum):
    PAY_PER_REQUEST = "PAY_PER_REQUEST"
    PROVISIONED = "PROVISIONED"


class HashType(str, Enum):
    HASH = "HASH"
    RANGE = "RANGE"
