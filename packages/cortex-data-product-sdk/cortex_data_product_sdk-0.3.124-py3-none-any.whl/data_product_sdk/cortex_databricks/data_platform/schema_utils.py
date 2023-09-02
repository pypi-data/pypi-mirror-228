from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3
from urllib.parse import urlparse

import json


def __get_schema_from_s3(
    s3_bucket, s3_key, region_name='us-east-1'
) -> dict:
    s3_client = S3(bucket_name=s3_bucket, region_name=region_name)
    obj = s3_client.get_object(s3_path=s3_key)
    obj = obj.read().decode('utf-8')
    js_obj = json.loads(obj)
    return js_obj


def get_schema_from_s3(
    s3_path: str,
    region_name: str = "us-east-1"
)  -> dict:
    if s3_path is None:
        return None
    url = urlparse(s3_path, allow_fragments=False)
    s3_bucket, s3_key = url.netloc, url.path.lstrip('/')
    return __get_schema_from_s3(s3_bucket=s3_bucket, s3_key=s3_key, region_name=region_name)
