# Bird Species Monitoring and Conservation Analysis

## Project Overview

This project aims to collect, process, and analyze global bird population data to provide insights for researchers, conservationists, and policymakers. By combining data from eBird and social media sources, we create a comprehensive view of bird populations, migration patterns, and public engagement with bird conservation efforts.

## Architecture

1. **Data Collection**: Daily extraction of eBird data and social media mentions
2. **Data Storage**: Amazon S3 for raw and processed data
3. **Data Processing**: AWS Glue for ETL jobs
4. **Data Querying**: Amazon Athena for SQL-based analysis
5. **Visualization**: Jupyter Notebooks for creating insightful visualizations

## Technologies Used

- Apache Airflow: Workflow orchestration
- Amazon S3: Data lake storage
- AWS Glue: ETL jobs
- Amazon Athena: SQL querying
- Jupyter Notebooks: Data analysis and visualization
- Python: Programming language (Pandas, Matplotlib, Seaborn)
- Git: Version control

## Data Pipeline

1. **Data Ingestion**:
    - Daily eBird data collection via API
    - Social media data collection (Twitter API)

2. **Data Storage**:
    - Raw data stored in S3 buckets

3. **Data Processing**:
    - AWS Glue jobs transform raw data into analyzable format
    - Processed data stored back in S3 in Parquet format

4. **Data Analysis**:
    - Amazon Athena queries processed data
    - Results exported to S3 for visualization

5. **Visualization**:
    - Jupyter Notebooks read data from S3
    - Creation of insightful plots and charts

## Airflow DAG Structure

```python
fetch_ebird_data >> upload_to_s3 >> trigger_glue_job >> export_athena_results