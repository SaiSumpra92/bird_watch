# tests/test_lambda_function.py

import pytest
from unittest.mock import patch, MagicMock
import json
from lambda_function.lambda_function import fetch_ebird_data, process_ebird_data, upload_to_s3, handler, get_api_key

@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("EBIRD_API_KEY", "test_api_key")

def test_get_api_key(mock_env_variables):
    assert get_api_key() == "test_api_key"

@patch('lambda_function.lambda_function.get_api_key', return_value="test_api_key")
@patch('lambda_function.lambda_function.requests.get')
def test_fetch_ebird_data(mock_get, mock_get_api_key):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"speciesCode": "amecro", "comName": "American Crow"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_ebird_data("US-NY", "2023-05-01")
    assert result == [{"speciesCode": "amecro", "comName": "American Crow"}]
    mock_get.assert_called_once_with(
        "https://api.ebird.org/v2/data/obs/US-NY/historic/2023-05-01",
        headers={"X-eBirdApiToken": "test_api_key"}
    )
    mock_get_api_key.assert_called_once()

def test_process_ebird_data():
    input_data = [{"speciesCode": "amecro", "comName": "American Crow"}]
    result = process_ebird_data(input_data)
    assert result == input_data  # Assuming no processing is done, update this test if you add processing logic

@patch('lambda_function.lambda_function.boto3.client')
def test_upload_to_s3(mock_boto3_client):
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3

    upload_to_s3("test-bucket", "test-key", {"test": "data"})
    mock_s3.put_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="test-key",
        Body='{"test": "data"}'
    )

@patch('lambda_function.lambda_function.fetch_ebird_data')
@patch('lambda_function.lambda_function.process_ebird_data')
@patch('lambda_function.lambda_function.upload_to_s3')
def test_handler(mock_upload, mock_process, mock_fetch):
    mock_fetch.return_value = [{"speciesCode": "amecro", "comName": "American Crow"}]
    mock_process.return_value = [{"speciesCode": "amecro", "comName": "American Crow", "processed": True}]

    result = handler(None, None)

    assert result['statusCode'] == 200
    assert "Data successfully fetched and uploaded to S3" in result['body']
    mock_fetch.assert_called_once()
    mock_process.assert_called_once()
    mock_upload.assert_called_once()

@patch('lambda_function.lambda_function.fetch_ebird_data')
def test_handler_error(mock_fetch):
    mock_fetch.side_effect = Exception("API Error")

    result = handler(None, None)

    assert result['statusCode'] == 500
    assert "Error: API Error" in result['body']

def test_get_api_key_local(monkeypatch):
    monkeypatch.setenv("EBIRD_API_KEY", "env_api_key")
    assert get_api_key() == "env_api_key"

def test_get_api_key_local_fallback(monkeypatch):
    monkeypatch.delenv("EBIRD_API_KEY", raising=False)
    assert get_api_key() == "test_api_key"

@patch('lambda_function.lambda_function.get_parameter', return_value="ssm_api_key")
def test_get_api_key_lambda(mock_get_parameter, monkeypatch):
    monkeypatch.setenv("AWS_EXECUTION_ENV", "AWS_Lambda_python3.8")
    assert get_api_key() == "ssm_api_key"
