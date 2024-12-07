# NLP Query Generator

This Python application provides natural language processing capabilities to generate SQL queries and GitHub search queries using Amazon Bedrock and LangChain.

## Features

- Convert natural language questions to SQL queries
- Transform descriptions into GitHub search queries
- Utilizes Amazon Bedrock's Claude v2 model
- Built with LangChain for prompt engineering

## Prerequisites

- Python 3.x
- AWS account with Bedrock access
- Required Python packages:
  - boto3
  - langchain

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install boto3 langchain
```

3. Configure AWS credentials with appropriate Bedrock access

## Configuration

Update the AWS region in the code according to your setup:

```python
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Update this to your region
)
```

## Usage

### NLP to SQL Query

```python
table_ddl = """
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
    id INT,
    date DATE,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2)
)
STORED AS PARQUET
LOCATION 's3://your-bucket/sales/';
"""

question = "What is the total sales amount for each product in the last month?"
sql_query = nlp_to_sql(question, table_ddl)
```

### NLP to GitHub Query

```python
description = "Find Python repositories that implement machine learning algorithms for image classification"
github_query = nlp_to_github_query(description)
```

## Functions

### nlp_to_sql(question, table_ddl)
Converts a natural language question into an SQL query based on the provided table DDL.

### nlp_to_github_query(description)
Transforms a natural language description into a GitHub search query.

## Model Configuration

The Bedrock model (Claude v2) is configured with the following parameters:
- max_tokens_to_sample: 500
- temperature: 0.5
- top_p: 1

## Contributing

Feel free to submit issues and enhancement requests!


## Acknowledgments

- Amazon Bedrock
- LangChain
- Anthropic's Claude v2 model

---
