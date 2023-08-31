import boto3
import datetime
import pandas as pd
import io

AWS_PROFILE='gaia_admin'

class S3Service:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        if AWS_PROFILE:
            boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.s3_client = boto3.client('s3')

    def _read_object_content(self, key):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        content = response['Body'].read()
        return content

    def upload_dataframe_csv(self, dataframe, key):
        csv_buffer = dataframe.to_csv(index=False)
        response = self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=csv_buffer.encode('utf-8')
        )
        return response

    def upload_dataframe_json(self, dataframe, key):
        json_buffer = dataframe.to_json(index=False)
        response = self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json_buffer.encode('utf-8')
        )
        return response

    def upload_dataframe_parquet(self, dataframe, key):
        parquet_buffer = io.BytesIO()
        dataframe.to_parquet(parquet_buffer, index=False)
        response = self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=parquet_buffer.getvalue()
        )
        return response

    def download_dataframe_csv(self, key):
        content = self._read_object_content(key)
        dataframe = pd.read_csv(io.BytesIO(content))
        return dataframe

    def download_dataframe_json(self, key):
        content = self._read_object_content(key)
        dataframe = pd.read_json(content)
        return dataframe

    def download_dataframe_parquet(self, key):
        content = self._read_object_content(key)
        dataframe = pd.read_parquet(io.BytesIO(content))
        return dataframe


