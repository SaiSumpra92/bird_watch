import boto3
import requests
from datetime import datetime
import json
import os
from botocore.exceptions import ClientError


def get_api_key():
    if 'AWS_EXECUTION_ENV' in os.environ:
        # We're in AWS, use Parameter Store
        try:
            ssm = boto3.client('ssm')
            response = ssm.get_parameter(Name='/ebird/api_key', WithDecryption=True)
            return response['Parameter']['Value']
        except ClientError as e:
            print(f"Error fetching from Parameter Store: {e}")
            raise
    else:
        # We're running locally, use environment variable
        api_key = os.environ.get('EBIRD_API_KEY')
        if not api_key:
            raise ValueError("EBIRD_API_KEY environment variable is not set")
        return api_key

def get_parameter():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name='/ebird/api_key',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def fetch_ebird_data(region):
    api_key = get_api_key()
    url = f"https://api.ebird.org/v2/data/obs/{region}/recent"
    headers = {"X-eBirdApiToken": api_key}
    print(f"Requesting URL: {url}")
    print(f"Headers: {{'X-eBirdApiToken': '[REDACTED]'}}")
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print(f"403 Forbidden Error. Response content: {response.text}")
    response.raise_for_status()
    return response.json()


def process_ebird_data(data):
    """Process eBird data"""
    # Add any data processing logic here
    # For example, filtering, transforming, or enriching the data
    return data

def upload_to_s3(bucket_name, key, data):
    """Upload data to S3"""
    s3 = boto3.client('s3',region_name='us-east-1')
    try:
        print(f"Attempting to upload to S3 bucket: {bucket_name}, key: {key}")
        # Convert the data to a JSON string
        json_data = json.dumps(data)
        s3.put_object(Bucket=bucket_name, Key=key, Body=json_data)
        print("Upload successful")
    except ClientError as e:
        print(f"An error occurred while uploading to S3: {e}")
        # Log the full error for debugging
        import traceback
        traceback.print_exc()
        raise


def handler(event, context):
    """Lambda handler function"""
    try:
        # Configuration (in a real scenario, these would be environment variables)
        region = "KZ"  # Example region
        bucket_name = "bird-conservation-bucket"

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Fetch data
        raw_data = fetch_ebird_data(region)

        # Process data
        processed_data = process_ebird_data(raw_data)

        # Upload to S3
        key = f"raw/{current_date}/ebird_data.json"
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
