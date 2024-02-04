import boto3
import yfinance as yf
from botocore.exceptions import NoCredentialsError

def fetch_snp500_data(num_points=100):
    try:
        # Download historical data for S&P 500 using yfinance
        snp500_data = yf.download('^GSPC', period='1y')['Close'].tail(num_points)
        return snp500_data
    except Exception as e:
        # Handle error cases
        print(f"Error fetching S&P 500 data: {e}")
        return None

def upload_snp500_data_to_s3(bucket_name, folder_name, data):
    try:
        # Initialize S3 client with credentials loaded from AWS configuration files
        session = boto3.Session()
        s3 = session.client('s3')

        # Create S3 key based on folder and file name
        s3_key = f'{folder_name}/snp500_data.csv'

        # Upload S&P 500 data to S3 bucket
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=data.to_csv())

        print(f"S&P 500 data uploaded to S3 bucket '{bucket_name}' in folder '{folder_name}'.")
        return True
    except NoCredentialsError:
        print("AWS credentials not found. Make sure your credentials are configured.")
        return False
    except Exception as e:
        # Handle other error cases
        print(f"Error uploading S&P 500 data to S3: {e}")
        return False

def handler(event, context):
    # Fetch the last 100 data points for the S&P 500
    snp500_data = fetch_snp500_data()

    if snp500_data is not None:
        # Print the fetched S&P 500 data
        print("Last 100 S&P 500 Data Points:")
        print(snp500_data)

        # Specify AWS credentials and region
        aws_profile = 'your_aws_profile'
        aws_region = 'your_aws_region'

        # Specify the S3 bucket and folder to store the data
        s3_bucket_name = 'your_s3_bucket'
        s3_folder_name = 'your_s3_folder'

        # Upload S&P 500 data to the specified S3 bucket and folder
        upload_snp500_data_to_s3(s3_bucket_name, s3_folder_name, snp500_data)

        return 'S&P 500 data printed and uploaded to S3 successfully.'
    else:
        return 'Failed to fetch S&P 500 data.'
