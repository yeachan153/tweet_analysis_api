import os
from aws_utils import AWSUtils
import boto3
from boto3.dynamodb.conditions import Key


class S3Downloader:

    LOCATION = os.getenv("filter_location").lower()
    KEEP_KEYS = ["retweets", "text", "time", "location"]

    def __init__(self):
        self.aws_utils = AWSUtils()

    def _get_keys(self):
        keys = self.aws_utils.get_all_s3_keys()
        return keys

    def download(self, filter_download=True):
        tweets = []
        keys = self._get_keys()
        for key in keys:
            tweet = self.aws_utils.get_json_from_s3(key)
            if self._download_filter(tweet, filter_download) is True:
                tweet = {key: tweet[key] for key in self.KEEP_KEYS}
                tweets.append(tweet)
        return tweets

    def _download_filter(self, tweet, filter_download=True):
        if filter is False:
            return True
        else:
            tweet_location = str(tweet["location"]).lower()
            if self.LOCATION not in tweet_location:
                return False
            return True


class DynamoDownloader:

    REGION = os.getenv("region")
    TBL_NAME = os.getenv("dynamo_table")

    def load_from_dynamo_table(self, ymd):
        """Load data from chosen dynamodb table

        Args:
            tbl_name (str): DynamoDB Table to retrieve data from
            ymd (str): year month Dated

        Returns:
            dict: Downloaded data
        """
        dynamodb = boto3.resource("dynamodb", region_name=self.REGION)
        table = dynamodb.Table(self.TBL_NAME)
        items = []

        response = table.query(KeyConditionExpression=Key("ymd").eq(ymd))
        items = items + response["Items"]

        while "LastEvaluatedKey" in response:
            response = table.query(
                KeyConditionExpression=Key("ymd").eq(ymd),
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            items = items + response["Items"]

        return items
