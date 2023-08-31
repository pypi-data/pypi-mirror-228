import json
import uuid
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Type

import boto3
import botocore
from lamina.helpers import async_
from loguru import logger
from pydantic import BaseModel, PrivateAttr
from stela import env

from coraline.config import CoralConfig
from coraline.exceptions import NotFound
from coraline.types import BillingMode, HashType

try:
    from mypy_boto3_dynamodb import DynamoDBClient
except ImportError:
    from botocore.client import BaseClient as DynamoDBClient


class CoralModel(BaseModel):
    model_config: CoralConfig
    _client: Optional[DynamoDBClient] = PrivateAttr(default=None)
    _table_name: Optional[str] = PrivateAttr(default=None)

    def get_client(self) -> DynamoDBClient:
        if not self._client:
            self._client = self.__class__._get_client()
        return self._client

    def table_name(self) -> str:
        if not self._table_name:
            self._table_name = self.__class__.get_table_name()
        return self._table_name

    @classmethod
    def get_table_name(cls):
        return cls.model_config.get("table_name") or cls.__name__

    @classmethod
    def _get_client_parameters(cls, env_key: str):
        if env_key == "region_name":
            env_key = "aws_region"

        # Try Model Config. Ex. model_config["aws_region"]
        value = cls.model_config.get(env_key, None)

        # Try Coraline env variables. Ex. CORALINE_AWS_REGION
        # AWS Config did not exists as Environment Variable
        if not value and env_key not in ["config"]:
            key = env_key if env_key.startswith("aws_") else f"aws_{env_key}"
            value = env.get(f"CORALINE_{key.upper()}", raise_on_missing=False)

        # Try AWS env variables. Ex. AWS_REGION
        # AWS Config and DynamoDB Endpoint URL does not exist as AWS Environment Variable
        if not value and env_key not in ["config", "endpoint_url"]:
            value = env.get(env_key.upper(), raise_on_missing=False)

        if value:
            return value

    @classmethod
    def _get_client(cls):
        # First Case: User passes a Config instance
        if cls._get_client_parameters("aws_config"):
            client_args = {
                env_key: cls._get_client_parameters(env_key)
                for env_key in ["region_name", "config"]
                if cls._get_client_parameters(env_key) is not None
            }
        else:
            # Using data from ModelConfig > Coraline Envs > AWS Envs
            client_args = {
                env_key: cls._get_client_parameters(env_key)
                for env_key in [
                    "region_name",
                    "aws_secret_access_key",
                    "aws_access_key_id",
                    "aws_session_token",
                    "endpoint_url",
                ]
                if cls._get_client_parameters(env_key) is not None
            }
        message = "Creating AWS DynamoDB client."
        if client_args.get("region_name"):
            message += f" Region: {client_args['region_name']},"
        if client_args.get("endpoint_url"):
            message += f" Endpoint: {client_args['endpoint_url']}"
        if client_args.get("config"):
            message += " Using Config instance."
        logger.debug(message)
        return boto3.client("dynamodb", **client_args)

    @classmethod
    def _convert_type(cls, annotation: Optional[Type[Any]]) -> Any:
        dynamo_types = {
            int: "N",
            float: "N",
            str: "S",
            Decimal: "N",
            bool: "BOOL",
            None: "NULL",
            List[dict]: "L",
            Dict[str, Any]: "M",
            uuid.UUID: "S",
            bytes: "B",
            List[bytes]: "BS",
            List[str]: "SS",
            List[int]: "NS",
            List[float]: "NS",
            List[Decimal]: "NS",
            Any: "S",
            Enum: "S",
        }
        return dynamo_types.get(annotation, "S")

    def __eq__(self, other):
        this_hash_key = None
        other_hash_key = None
        this_range_key = None
        other_range_key = None
        for field_name, field_info in self.model_fields.items():
            if (
                field_info.json_schema_extra is None
                or field_info.json_schema_extra.get("dynamodb_key") is False
            ):
                continue
            if field_info.json_schema_extra.get("dynamodb_hash_type") == HashType.HASH:
                this_hash_key = getattr(self, field_name)
                other_hash_key = getattr(other, field_name)
            if field_info.json_schema_extra.get("dynamodb_hash_type") == HashType.RANGE:
                this_range_key = getattr(self, field_name)
                other_range_key = getattr(other, field_name)
        if this_hash_key is None or other_hash_key is None:
            return False
        return this_hash_key == other_hash_key and this_range_key == other_range_key

    ###################################
    #                                 #
    # Sync methods                    #
    #                                 #
    ###################################

    @classmethod
    def get_or_create_table(cls):
        try:
            client = cls._get_client()
            table = client.describe_table(TableName=cls.get_table_name())
            return table
        except botocore.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                return cls.create_table()
            raise exc

    @classmethod
    def create_table(cls):
        table_name = cls.get_table_name()

        # Get Attribute Definition from Pydantic custom KeyFields
        attribute_definitions = [
            {
                "AttributeName": field_info.alias or field_name,
                "AttributeType": cls._convert_type(field_info.annotation),
            }
            for field_name, field_info in cls.model_fields.items()
            if field_info.json_schema_extra is not None
            and field_info.json_schema_extra.get("dynamodb_key") is True
        ]

        # Get Key Schema from Pydantic custom KeyFields
        key_schema = [
            {
                "AttributeName": field_info.alias or field_name,
                "KeyType": field_info.json_schema_extra.get("dynamodb_hash_type").value,
            }
            for field_name, field_info in cls.model_fields.items()
            if field_info.json_schema_extra is not None
            and field_info.json_schema_extra.get("dynamodb_key") is True
        ]

        # Get Billing mode from Pydantic Model Config
        provisioned_throughput = None
        billing_mode = (
            cls.model_config.get("billing_mode") or BillingMode.PAY_PER_REQUEST
        )
        if billing_mode == BillingMode.PROVISIONED:
            provisioned_throughput = {
                "ReadCapacityUnits": cls.model_config.get("read_capacity_units", 1),
                "WriteCapacityUnits": cls.model_config.get("write_capacity_units", 1),
            }

        create_table_kwargs = {
            "TableName": table_name,
            "AttributeDefinitions": attribute_definitions,
            "KeySchema": key_schema,
            "BillingMode": billing_mode,
        }
        if provisioned_throughput:
            create_table_kwargs.update(provisioned_throughput)

        logger.debug(f"Creating table {table_name}...")
        client = cls._get_client()
        table = client.create_table(
            **create_table_kwargs,
            **cls.model_config.get("extra_table_params", {}),
        )

        # wait until table is created
        waiter = client.get_waiter("table_exists")
        waiter.wait(TableName=table_name, WaiterConfig={"Delay": 1, "MaxAttempts": 25})
        return table

    def save(self, **kwargs):
        dump_data = json.loads(self.model_dump_json())
        item = {
            field_info.alias
            or field_name: {
                self._convert_type(field_info.annotation): dump_data[field_name]
            }
            for field_name, field_info in self.model_fields.items()
        }
        return self.get_client().put_item(
            TableName=self.table_name(), Item=item, **kwargs
        )

    @classmethod
    def exists(cls, **kwargs):
        client, key_query, kwargs = cls._get_key_query(**kwargs)
        response = client.get_item(
            TableName=cls.get_table_name(), Key=key_query, **kwargs
        )
        return "Item" in response

    @classmethod
    def get(cls, **kwargs):
        client, key_query, kwargs = cls._get_key_query(**kwargs)
        response = client.get_item(
            TableName=cls.get_table_name(), Key=key_query, **kwargs
        )

        if "Item" not in response:
            raise NotFound(
                f"Item not found in table {cls.get_table_name()}: {key_query}"
            )

        item_payload = {
            key: data[list(data.keys())[0]] for key, data in response["Item"].items()
        }
        return cls(**item_payload)

    @classmethod
    def _get_key_query(cls, **kwargs):
        def get_query_dict(field_info, field_name):
            convert_type = cls._convert_type(field_info.annotation)
            convert_data = kwargs.pop(field_name)
            if convert_type == "S":
                convert_data = str(convert_data)
            return {convert_type: convert_data}

        client = cls._get_client()
        key_query = {
            field_info.alias or field_name: get_query_dict(field_info, field_name)
            for field_name, field_info in cls.model_fields.items()
            if field_info.json_schema_extra is not None
            and field_info.json_schema_extra.get("dynamodb_key") is True
        }
        return client, key_query, kwargs

    ###################################
    #                                 #
    # Async methods                   #
    #                                 #
    ###################################

    @classmethod
    async def aget_or_create_table(cls):
        return await async_(cls.get_or_create_table)()

    async def acreate_table(self):
        return await async_(self.create_table)()

    @classmethod
    async def aget(cls, **kwargs):
        return await async_(cls.get)(**kwargs)

    async def asave(self, **kwargs):
        return await async_(self.save)(**kwargs)

    @classmethod
    async def aexists(cls, **kwargs):
        return await async_(cls.exists)(**kwargs)
