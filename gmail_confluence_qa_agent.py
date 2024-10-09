import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.llms.bedrock import Bedrock
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from atlassian import Confluence
import base64
import email

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Confluence setup
confluence = Confluence(
    url='https://your-domain.atlassian.net/wiki',
    username='your-email@example.com',
    password='your-api-token'
)

# Bedrock Claude setup
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # replace with your preferred region
)

llm = Bedrock(
    model_id="anthropic.claude-v2",
    client=bedrock_runtime,
    model_kwargs={"temperature": 0.7, "max_tokens_to_sample": 500}
)

# LangChain setup
template = """
Based on the following question from an email:
{question}

And the following information from Confluence:
{confluence_info}

Please draft a response to the email:
"""

prompt = PromptTemplate(template=template, input_variables=["question", "confluence_info"])
chain = LLMChain(llm=llm, prompt=prompt)

def search_confluence(query):
    results = confluence.search(query, limit=5)
    content = ""
    for result in results:
        if 'content' in result:
            content += result['content']['body']['storage']['value'] + "\n\n"
    return content

def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    
    subject = ""
    sender = ""
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']
    
    if parts:
        for part in parts:
            if part['mimeType'] == "text/plain":
                data = part['body']["data"]
                body = base64.urlsafe_b64decode(data).decode()
                return subject, sender, body
    
    return subject, sender, ""

def send_reply(service, message_id, to, subject, body):
    message = email.message.EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = f"Re: {subject}"
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    service.users().messages().send(
        userId='me',
        body={
            'raw': raw_message,
            'threadId': message_id
        }
    ).execute()

def main():
    service = gmail_authenticate()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    for message in messages:
        subject, sender, body = read_message(service, message)
        confluence_info = search_confluence(body)
        
        response = chain.run(question=body, confluence_info=confluence_info)
        
        send_reply(service, message['id'], sender, subject, response)
        
        # Mark the message as read
        service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    main()
