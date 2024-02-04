import boto3
from botocore.exceptions import NoCredentialsError
import sys

def create_s3_resources(bucket_name, folder_name=None, aws_profile='horsada', aws_region='eu-west-2'):
    try:
        # Initialize S3 client with credentials and region loaded from AWS configuration files
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        s3 = session.client('s3')

        # Determine the appropriate location constraint based on the AWS region
        location_constraint = aws_region if aws_region != 'us-east-1' else ''

        # Create S3 bucket with location constraint
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location_constraint})

        if folder_name:
            # Create a placeholder object to simulate a folder (prefix) in S3
            folder_placeholder_key = f'{folder_name}/placeholder.txt'
            s3.put_object(Bucket=bucket_name, Key=folder_placeholder_key, Body='')

            print(f"Folder '{folder_name}' created in S3 bucket '{bucket_name}'.")
        else:
            print(f"S3 bucket '{bucket_name}' created successfully.")

        return True
    except NoCredentialsError:
        print(f"AWS credentials not found for profile '{aws_profile}'. Make sure your credentials are configured.")
        return False
    except Exception as e:
        # Handle other error cases
        print(f"Error creating S3 resources: {e}")
        return False

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) not in [4, 5]:
        print("Usage: python script_name.py <aws_profile> <aws_region> <bucket_name> [<folder_name>]")
        sys.exit(1)

    # Extract AWS profile, region, bucket name, and optional folder name from command-line arguments
    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]
    bucket_name_to_create = sys.argv[3]
    folder_name_to_create = sys.argv[4] if len(sys.argv) == 5 else None

    # Create S3 resources using the specified profile, region, bucket name, and optional folder name
    create_s3_resources(bucket_name_to_create, folder_name_to_create, aws_profile=aws_profile, aws_region=aws_region)
