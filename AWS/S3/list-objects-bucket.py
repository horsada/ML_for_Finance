import boto3
from botocore.exceptions import NoCredentialsError
import sys

def list_objects_in_bucket(aws_profile, aws_region, bucket_name, folder=None):
    try:
        # Initialize S3 client with credentials and region loaded from AWS configuration files
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        s3 = session.client('s3')

        # List objects in the specified S3 bucket and folder
        prefix = f"{folder}/" if folder else ""
        response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

        # Print the object names
        if 'Contents' in response:
            print(f"Objects in S3 bucket '{bucket_name}', folder '{folder}':")
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print(f"S3 bucket '{bucket_name}', folder '{folder}' is empty.")

        return True
    except NoCredentialsError:
        print("AWS credentials not found. Make sure your credentials are configured.")
        return False
    except Exception as e:
        # Handle other error cases
        print(f"Error listing objects in S3 bucket: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python script_name.py <aws_profile> <aws_region> <bucket_name> [folder]")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]
    s3_bucket_name = sys.argv[3]
    folder = sys.argv[4] if len(sys.argv) == 5 else None

    # List objects in the specified S3 bucket and folder using the provided credentials
    list_objects_in_bucket(aws_profile, aws_region, s3_bucket_name, folder)
