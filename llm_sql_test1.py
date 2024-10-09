import boto3
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set up Boto3 client for Bedrock
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your desired region
)

# Initialize Bedrock LLM
llm = Bedrock(
    model_id="anthropic.claude-v2",  # Or another suitable model
    client=bedrock_runtime,
    model_kwargs={
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "top_p": 1,
    }
)

# NLP to SQL function
def nlp_to_sql(question, table_ddl):
    prompt_template = """
    Given the following Athena table DDL:
    {table_ddl}
    
    Generate an SQL query to answer the following question:
    {question}
    
    SQL Query:
    """
    
    prompt = PromptTemplate(
        input_variables=["table_ddl", "question"],
        template=prompt_template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(table_ddl=table_ddl, question=question)
    return result.strip()

# NLP to GitHub query function
def nlp_to_github_query(description):
    prompt_template = """
    Convert the following description into a GitHub search query:
    {description}
    
    GitHub Search Query:
    """
    
    prompt = PromptTemplate(
        input_variables=["description"],
        template=prompt_template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(description=description)
    return result.strip()

# Example usage
if __name__ == "__main__":
    # Example for NLP to SQL
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
    print("Generated SQL Query:")
    print(sql_query)
    print()
    
    # Example for NLP to GitHub query
    description = "Find Python repositories that implement machine learning algorithms for image classification"
    
    github_query = nlp_to_github_query(description)
    print("Generated GitHub Query:")
    print(github_query)