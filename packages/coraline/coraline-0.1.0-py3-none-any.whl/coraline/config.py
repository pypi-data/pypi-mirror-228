from typing import Optional

from botocore.config import Config
from pydantic import ConfigDict

from coraline.types import BillingMode


class CoralConfig(ConfigDict):
    table_name: Optional[str]
    billing_mode: Optional[BillingMode]
    aws_region: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_access_key_id: Optional[str]
    aws_session_token: Optional[str]
    aws_config: Optional[Config]
    aws_endpoint_url: Optional[str]
    read_capacity_units: Optional[int]
    write_capacity_units: Optional[int]
    extra_table_params: Optional[dict]
