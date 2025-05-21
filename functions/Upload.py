# Single JSON file upload to S3 with KMS key

# Load libraries
import boto3
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def upload_to_s3(aws_access_key,aws_secret_key, local_file, bucket_name,  bucket_filename):

    # Create S3 Client using AWS Credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    print('s3 client created')

    # Upload file to S3 Bucket
    s3_client.upload_file(
            Filename = local_file, 
            Bucket = bucket_name, 
            Key = bucket_filename
            )
    print(local_file+' uploaded to s3')

# # Set file start and end points
# local_file = "sample.json"
# bucket_file_path = os.getenv('aws_bucket_filepath')
# aws_access_key=os.getenv('aws_access_key')
# aws_secret_key=os.getenv('aws_secret_key')
# bucket_name=os.getenv('aws_bucket')
# bucket_filename = bucket_file_path+'/campaign/'+ local_file

# upload_to_s3(aws_access_key,aws_secret_key,local_file, bucket_name, bucket_file_path,  bucket_filename)
    