# Import Coraline field model and types here
from asbool import asbool
from loguru import logger
from stela import env

from coraline.config import CoralConfig
from coraline.field import KeyField
from coraline.model import CoralModel
from coraline.types import BillingMode, HashType

__version__ = "0.1.4"

__all__ = [
    "CoralModel",
    "KeyField",
    "BillingMode",
    "HashType",
    "CoralConfig",
]

if asbool(env.get_or_default("CORALINE_SHOW_LOGS", True)):
    logger.enable("coraline")
else:
    logger.disable("coraline")
