import json
from downloader import DynamoDownloader
from decimal_encoder import DecimalEncoder


def handler(event, context):
    ymd = event["queryStringParameters"]["ymd"]
    result = DynamoDownloader().load_from_dynamo_table(ymd)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, cls=DecimalEncoder),
    }
