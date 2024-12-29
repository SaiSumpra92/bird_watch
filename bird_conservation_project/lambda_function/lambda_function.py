import boto3
import requests
from datetime import datetime
import json
import os
from botocore.exceptions import ClientError


def get_api_key():
    if 'AWS_EXECUTION_ENV' in os.environ:  # Running in Lambda
        return get_parameter()
    else:  # Local development
        return os.environ.get('EBIRD_API_KEY') or "test_api_key"

def get_parameter():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name='/ebird/api_key',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def fetch_ebird_data(region, date):
    api_key = get_api_key()
    # Use api_key in your request
    url = f"https://api.ebird.org/v2/data/obs/{region}/historic/{date}"
    headers = {"X-eBirdApiToken": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def process_ebird_data(data):
    """Process eBird data"""
    # Add any data processing logic here
    # For example, filtering, transforming, or enriching the data
    return data

def upload_to_s3(bucket_name, key, data):
    """Upload data to S3"""
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))

def handler(event, context):
    """Lambda handler function"""
    try:
        # Configuration (in a real scenario, these would be environment variables)
        api_key = get_api_key()
        region = "us-east-1"  # Example region
        bucket_name = "bird-conservation-bucket"

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Fetch data
        raw_data = fetch_ebird_data(api_key, region, current_date)

        # Process data
        processed_data = process_ebird_data(raw_data)

        # Upload to S3
        key = f"raw/ebird_data_{current_date}.json"
        upload_to_s3(bucket_name, key, raw_data)

        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully fetched and uploaded to S3')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

# For local testing
if __name__ == "__main__":
    result = handler(None, None)
    print(result)
