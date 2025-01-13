
# Bird Watch Data Pipeline

## Project Overview
This project implements a data pipeline for collecting and storing bird observation data using AWS serverless technologies. It fetches recent bird data for a specified region from the eBird API.

## Technologies Used
- AWS Lambda
- Amazon S3
- AWS CDK (Cloud Development Kit)
- Python 3.11
- Boto3
- Requests library

## Project Structure

bird_conservation_project/
├── lambda_function/
│   ├── __init__.py
│   ├── lambda_function.py
│   └── requirements.txt
├── tests/
│   └── test_lambda_function.py
├── infrastructure/
│   ├── app.py
│   └── bird_conservation_stack.py
├── README.md
└── cdk.json



## Features
- Fetches recent bird observation data for a specified region from eBird API
- Stores data in Amazon S3
- Infrastructure defined and deployed using AWS CDK

## Setup and Deployment
1. Clone the repository
2. Install dependencies:

pip install -r requirements.txt

3. Configure AWS credentials
4. Deploy the stack:

cdk deploy

## How It Works
1. Lambda function is triggered (currently manual trigger)
2. Function fetches recent bird observation data from eBird API for the specified region
3. Data is stored in an S3 bucket

## TODO
- Implement orchestration using Apache Airflow
- Add monitoring and alerting

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes.

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contact 
Sai Krishna K- [saifeatherweight@gmail.com]
Project Link: [https://github.com/SaiSumpra92/bird_watch]