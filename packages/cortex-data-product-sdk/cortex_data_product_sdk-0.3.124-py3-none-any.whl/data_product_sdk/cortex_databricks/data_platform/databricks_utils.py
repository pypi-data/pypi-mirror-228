from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3

import data_product_sdk.cortex_databricks.data_platform.loader_utils as loader_utils


def __delete_checkpoint_location(
    *,
    bucket_name,
    checkpoint_location,
    s3_client=None,
    region_name: str = "us-east-1"
):
    if s3_client is None:
        s3_client = S3(bucket_name=bucket_name, region_name=region_name)
    s3_bucket, s3_key = s3_client.get_bucket_key_from_s3_url(s3_url=checkpoint_location)
    return s3_client.delete_files(prefix=s3_key)


def reset_autoloader_checkpoint(
    *,
    bucket_name,
    data_pack_name,
    dataset_name,
    input_table_name='',
    region_name='us-east-1',
    custom_checkpoint_location=None
):
    checkpoint_location = custom_checkpoint_location if custom_checkpoint_location else loader_utils.build_checkpoint_path(
        bucket_name=bucket_name,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
        input_table_name=input_table_name
    )
    return __delete_checkpoint_location(bucket_name=bucket_name, checkpoint_location=checkpoint_location, region_name=region_name)
