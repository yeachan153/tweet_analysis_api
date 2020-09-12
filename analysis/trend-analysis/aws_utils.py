import boto3
import os
import json


class AWSUtils:

    BUCKET = os.getenv("bucket_name")

    def get_all_s3_keys(self):
        """Get a list of all keys in an S3 bucket."""
        s3 = boto3.client("s3")
        keys = []

        kwargs = {"Bucket": self.BUCKET}
        while True:
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp["Contents"]:
                keys.append(obj["Key"])

            try:
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            except KeyError:
                break

        return keys

    def get_json_from_s3(self, key: str):
        """Gets json data from s3"""
        s3 = boto3.resource("s3")
        content_object = s3.Object(self.BUCKET, key)
        file_content = content_object.get()["Body"].read().decode()
        json_content = json.loads(file_content)
        return json_content
