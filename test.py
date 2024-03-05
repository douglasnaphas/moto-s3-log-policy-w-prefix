import boto3
from moto import mock_aws


@mock_aws
def test():
    s3_client = boto3.client("s3", region_name="us-east-1")
    assert len(s3_client.list_buckets()["Buckets"]) == 0
    s3_client.create_bucket(Bucket="my-bucket1234")
    assert len(s3_client.list_buckets()["Buckets"]) == 1
    bucket_logging1 = s3_client.get_bucket_logging(Bucket="my-bucket1234")
    print(bucket_logging1)
    s3_client.create_bucket(Bucket="logging-bucket1234")
    logging_bucket1234_policy = """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "S3ServerAccessLogsPolicy",
                "Effect": "Allow",
                "Principal": {"Service": "logging.s3.amazonaws.com"},
                "Action": ["s3:PutObject"],
                "Resource": "arn:aws:s3:::logging-bucket1234/*"
            }
        ]
    }"""
    put_bucket_policy_response = s3_client.put_bucket_policy(
        Bucket="logging-bucket1234", Policy=logging_bucket1234_policy
    )
    print(f"{put_bucket_policy_response=}")
    s3_client.put_bucket_logging(
        Bucket="my-bucket1234",
        BucketLoggingStatus={
            "LoggingEnabled": {
                "TargetBucket": "logging-bucket1234",
                "TargetPrefix": "my-bucket1234/",
            }
        },
    )
    bucket_logging2 = s3_client.get_bucket_logging(Bucket="my-bucket1234")
    print(bucket_logging2)

