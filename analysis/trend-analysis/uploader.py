import os
import boto3


def push_trend_table(trending_tweets):
    table_name = os.getenv("dynamo_table")
    region_name = os.getenv("region")
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    trend_table = dynamodb.Table(table_name)
    for tweet in trending_tweets:
        trend_table.put_item(Item=tweet)
