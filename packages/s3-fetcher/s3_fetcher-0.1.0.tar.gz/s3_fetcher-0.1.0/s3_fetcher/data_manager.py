import os
import boto3
import json
import logging

from datetime import datetime, timedelta


class S3DataManager:
    S3_SERVICE_NAME = 's3'
    PAGINATOR_TYPE = 'list_objects_v2'

    def __init__(
        self, 
        aws_access_key_id, 
        aws_secret_access_key, 
        aws_region_name, 
        s3_bucket_name
    ):
        self.s3_client = self.connect_s3(aws_access_key_id, aws_secret_access_key, aws_region_name)
        self.s3_bucket_name = s3_bucket_name
        self._timeframe = []
    
    def connect_s3(self, aws_access_key_id, aws_secret_access_key, aws_region_name):
        try:
            s3_client = boto3.client(
                self.S3_SERVICE_NAME,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region_name
            )
            print("S3 client connected successfully!")
            return s3_client
        except Exception as e:
            print("Error connecting to S3:", e)
        return 

    def set_timeframe(self, dates):
        self._timeframe = dates

    def list_objects(self, prefix=''):
        objects = []
        paginator = self.s3_client.get_paginator(self.PAGINATOR_TYPE)
        page_iterator = paginator.paginate(Bucket=self.s3_bucket_name, Prefix=prefix)

        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    objects.append(key)
        return objects

    def _within_timeframe(self, text):
        if not self._timeframe:
            return True

        for date in self._timeframe:
            if date in text:
                return True
        return False

    def list_objects_recursive(self, prefix):
        prefix = prefix.strip()
        if prefix.startswith('/'):
            prefix = prefix[1:]

        all_objects = []
        objects = self.list_objects(prefix)
        for obj in objects:
            if obj.endswith('/'):
                subfolder = obj[len(prefix):]
                subfolder_objects = self.list_objects_recursive(obj)
                subfolder_objects_with_prefix = [subfolder + o for o in subfolder_objects]
                all_objects.extend(subfolder_objects_with_prefix)
            else:
                all_objects.append(obj)
        return all_objects

    def read_json(self, object_key):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket_name, Key=object_key)
            json_data = response['Body'].read().decode('utf-8')
            json_obj = json.loads(json_data)
            return json_obj

        except Exception as e:
            print('Error:', e)
            return None

    def download_json(self, filename, local_path):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket_name, Key=filename)
            json_data = response['Body'].read()
            with open(local_path, 'wb') as f:
                f.write(json_data)
            logging.info(f'Downloaded {filename} to {local_path}')
            json_obj = json.loads(json_data.decode('utf-8'))
            return json_obj
        except Exception as e:
            logging.error('Error:', e)
        return

    def download_file(self, filename, local_path):
        try:
            self.s3_client.download_file(self.s3_bucket_name, filename, local_path)
            print(f'Downloaded {filename} to {local_path}')
        except Exception as e:
            print('Error:', e)

    def upload_json_to_s3(self, data_path="", s3_prefix="", data={}):
        s3_key = ""
        try:
            if data_path:
                with open(data_path, 'r') as file:
                    data = json.load(file)

                filename = os.path.basename(data_path)
                s3_key = f"{s3_prefix}/{filename}"

            response = self.s3_client.put_object(
                Bucket=self.s3_bucket_name,
                Key=s3_key or s3_prefix,
                Body=json.dumps(data),
                ContentType='application/json'
            )
            return response
        except Exception as e:
            return f"Error uploading JSON to S3: {str(e)}"

    def delete_file_from_s3(self, s3_key):
        try:
            response = self.s3_client.delete_object(
                Bucket=self.s3_bucket_name,
                Key=s3_key
            )
            return response
        except Exception as e:
            return f"Error deleting file from S3: {str(e)}"