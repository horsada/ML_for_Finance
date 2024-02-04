import boto3
from botocore.exceptions import NoCredentialsError
import sys

def delete_s3_bucket(bucket_name, aws_profile='horsada', aws_region='eu-west-2'):
    try:
        # Initialize S3 client with credentials and region loaded from AWS configuration files
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        s3 = session.client('s3')

        # Delete S3 bucket
        s3.delete_bucket(Bucket=bucket_name)

        print(f"S3 bucket '{bucket_name}' deleted successfully.")
        return True
    except NoCredentialsError:
        print(f"AWS credentials not found for profile '{aws_profile}'. Make sure your credentials are configured.")
        return False
    except Exception as e:
        # Handle other error cases
        print(f"Error deleting S3 bucket: {e}")
        return False

if __name__ == "__main__":
    # Check if AWS region, bucket name, and profile name are provided as command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <aws_profile> <aws_region> <bucket_name>")
        sys.exit(1)

    # Extract AWS profile, region, and bucket name from command-line arguments
    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]
    bucket_name_to_delete = sys.argv[3]

    # Delete the S3 bucket using the specified profile, region, and bucket name
    delete_s3_bucket(bucket_name_to_delete, aws_profile=aws_profile, aws_region=aws_region)
