import boto3
import sys

def invoke_lambda_function(aws_profile, aws_region, lambda_function_name):
    # Initialize Lambda client with credentials and region
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    lambda_client = session.client('lambda')

    try:
        # Invoke Lambda function
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
            LogType='Tail'
        )

        # Print the response
        print(response)

        # Optionally, print the logs
        if 'LogResult' in response:
            print(f"Lambda Function Logs:\n{response['LogResult'].decode('base64')}")

    except Exception as e:
        # Handle errors
        print(f"Error invoking Lambda function: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <aws_profile> <aws_region> <lambda_function_name>")
        sys.exit(1)

    aws_profile, aws_region, lambda_function_name = sys.argv[1:4]
    invoke_lambda_function(aws_profile, aws_region, lambda_function_name)
