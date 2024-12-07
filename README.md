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

# Email Auto-Response System with Confluence Integration

## Description
This application is an automated email response system that integrates Gmail, Confluence, and Amazon Bedrock (Claude) to provide intelligent responses to incoming emails. The system searches relevant information from Confluence and uses Claude to generate contextual responses.

## Features
- Automatically processes unread emails from Gmail
- Searches Confluence for relevant documentation
- Generates intelligent responses using Amazon Bedrock (Claude)
- Sends automated replies
- Marks processed emails as read

## Prerequisites
- Python 3.7+
- Google Cloud Platform account with Gmail API enabled
- Atlassian Confluence account
- AWS account with Bedrock access
- Required API credentials and tokens

## Required Credentials
1. Gmail API credentials (`credentials.json`)
2. Confluence API token
3. AWS credentials configured for Bedrock access

## Installation

1. Clone the repository
```bash
git clone [repository-url]
```

2. Install required packages
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client atlassian-python-api boto3 langchain
```

3. Configure credentials:
   - Place `credentials.json` from Google Cloud Console in the root directory
   - Update Confluence credentials in the code
   - Configure AWS credentials using AWS CLI or environment variables

## Configuration
Update the following variables in the code:
- Confluence URL
- Confluence username and API token
- AWS region
- LLM parameters (temperature, max tokens)

## Usage
Run the script:
```bash
python main.py
```

The script will:
1. Authenticate with Gmail
2. Check for unread emails
3. Search Confluence for relevant information
4. Generate responses using Claude
5. Send automated replies
6. Mark processed emails as read

## File Structure
- `main.py`: Main application code
- `credentials.json`: Gmail API credentials
- `token.json`: Generated OAuth token (created automatically)

## Security Notes
- Keep all API credentials and tokens secure
- Don't commit sensitive credentials to version control
- Use environment variables for sensitive information

## Dependencies
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- atlassian-python-api
- boto3
- langchain

## Error Handling
The script includes basic error handling for:
- Authentication failures
- API rate limits
- Message processing errors

