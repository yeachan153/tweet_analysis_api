import boto3
import botocore.session
from utils.exceptions import TableInUseException


class CreateTableUtils:
    """Utility class to create tables"""

    def _create_generic_template(self, partition, secondary, table_name, tags):
        return {
            "AttributeDefinitions": [
                {"AttributeName": partition, "AttributeType": "S"},
                {"AttributeName": secondary, "AttributeType": "S"},
            ],
            "TableName": table_name,
            "KeySchema": [
                {"AttributeName": partition, "KeyType": "HASH"},  # Partition key
                {"AttributeName": secondary, "KeyType": "RANGE"},  # Sort key
            ],
            "BillingMode": "PAY_PER_REQUEST",
            "Tags": tags,
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "version_index",
                    "KeySchema": [{"AttributeName": secondary, "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
        }

    def _base_create(self, region, table_name, table_logic):
        dynamodb = boto3.resource("dynamodb", region_name=region)
        dynamodb_client = boto3.client("dynamodb", region_name=region)
        session = botocore.session.get_session()
        dynamodb = session.create_client("dynamodb", region_name=region)
        waiter = dynamodb.get_waiter("table_exists")
        try:
            dynamodb.create_table(**table_logic)
            waiter.wait(TableName=table_name)
        except dynamodb_client.exceptions.ResourceInUseException:
            raise TableInUseException(f"Table: {table_name} already in use in {region}")

    def create_trend_table(
        self, partition: str, secondary: str, table_name: str, region: str, tags: list
    ):
        """
        Creates DynamoDB tables.
        Arguments:
            partition (str) -- name of partition hash key
            secondary (str) -- name of secondary range key
            table_name (str) -- name of table to create.
            region (str) -- dynamoDB region.
            tags (list) -- AWS tags
        """
        template = self._create_generic_template(partition, secondary, table_name, tags)
        self._base_create(region, table_name, template)


def create_tags(app, env, name, office, owner):
    return [
        {"Key": "Application", "Value": app},
        {"Key": "Environment", "Value": env},
        {"Key": "Name", "Value": name},
        {"Key": "Office", "Value": office},
        {"Key": "Owner", "Value": owner},
    ]


def create_trend_table():
    """Creates the analysis table
    under a hard-coded template
    """
    table_name = "twitter_analysis_fedex"
    partition = "ymd"
    secondary = "hour"
    region = "eu-central-1"

    app = "fedex case"
    env = "production"
    name = table_name
    office = "ams"
    owner = "yeachan"

    tags = create_tags(app, env, name, office, owner)
    CreateTableUtils().create_trend_table(
        partition, secondary, table_name, region, tags
    )
