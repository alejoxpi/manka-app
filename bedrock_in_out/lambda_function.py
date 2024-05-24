import json
import requests
from os import environ
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def add_text(role, content, history):
    logger.info("expand history items into new_history")
    # expand history items into new_history
    new_history = [h for h in history]
    new_history.append({"role":role,"content":content})
    return new_history
    
def invoke_model(model_id, anthropic_version, text, max_tokens, history):
    
    bedrock_agent = boto3.client('bedrock-agent-runtime')
    content = [{"type":"text","text":text}]
    new_history = add_text("user",content, history)
    
    #################################
    # Invoke Bedrock knowledge base # 
    #################################
    # Replace with your Bedrock agent ID and version
    # agent_id = "your_agent_id"
    # agent_version = "your_agent_version"
    
    # Replace with your query
    query = text
    print(f'Mensaje del usuario: {query}')

    message_response = ""
    

    try:
        response = bedrock_agent.invoke_agent(
            agentId='LF3QQYZVWL',
            agentAliasId='XK7WYSP8UC',
            sessionId='mytest',
            inputText=query,
        )

        print("Response from Bedrock: ")
        print(response)
    
        for event in response.get("completion"):
            chunk = event["chunk"]
            message_response += chunk["bytes"].decode()
    
    except Exception as e:
        print("Error invoking Bedrock: ")
        print(e.response['Error']['Message'])
    
    return message_response

def whats_out(phone, whats_token, phone_id, message):
        
    # https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#reply-to-message    
    URL = 'https://graph.facebook.com/v19.0/'+phone_id+'/messages'    

    headers = {'Authorization': whats_token, 'Content-Type': 'application/json'}
    data = { 
        "messaging_product": "whatsapp", 
        "to": phone, 
        # "context":  json.dumps({ "message_id": in_reply_to}), TODO: enable when reply_to_message is supported
        "type": "text",
        "text": json.dumps({ "preview_url": False, "body": message})
    }
    
    print("Sending message")
    
    response = requests.post(URL, headers=headers, data=data)
    responsejson = response.json()
    print("Responses: "+ str(responsejson)
    )
    
def lambda_handler(event, context):
    
    print("Received event: " + json.dumps(event, indent=2))    

    message = event['whats_message']
    whats_token = event['whats_token']    
    phone = event['phone']
    phone_id = event['phone_id']
        
    print("PROMPT: ", message)
    
    model_id = environ["MODEL_ID"]
    anthropic_version = environ["ANTHROPIC_VERSION"]
    max_tokens=1000
    history = ["history"]
    
    response = invoke_model(model_id, anthropic_version, message, max_tokens, history)
    
    print("RESPONSE BEDROCK: ", response)    
    
    whats_out(phone, whats_token, phone_id, response)
    
    return {
        'statusCode': 200,
        'body': "OK"
    }