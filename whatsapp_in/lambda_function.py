import json
import boto3
import time


def lambda_handler(event, context):

    print (event)
    #connect_config=json.loads(get_config(CONFIG_PARAMETER))

    WHATS_VERIFICATION_TOKEN = "uy2vdi66as"
    WHATS_TOKEN = "Bearer EAAOkFENOXy0B"
    PHONE_ID = "34555498529"

    if event['httpMethod'] == 'GET':
        return build_response(200, 
            #validate_healthcheck(event, connect_config['WHATS_VERIFICATION_TOKEN']))
            validate_healthcheck(event, WHATS_VERIFICATION_TOKEN)) #TODO extract from secret 

    if event.get("body") is None: 
        build_response(200,"bye bye")

    
    if event['httpMethod'] == 'POST':

        print("Se recibio un POST")
        print(event['body'])

        body = json.loads(event['body'])
        print(body)

        entry = body['entry'][0]
        message = entry['changes'][0]['value']['messages'][0]['text']['body']
        phone = entry['changes'][0]['value']['messages'][0]['from']


        lambda_post_request(message, phone,  WHATS_TOKEN, PHONE_ID)

        print("Se envio el mensaje")
        return build_response(200, "OK")        
        


def lambda_post_request(message, phone_number, whats_token, phone_id):

    ia_function_name = 'bedrock_agent'

    print("Calling lambda Bedrock Agent "+time.strftime("%c"))

    client = boto3.client('lambda')

    response = client.invoke(
        FunctionName=ia_function_name,
        InvocationType='Event',
        Payload=json.dumps({'whats_message': message, 'phone': phone_number, 'whats_token':whats_token, 'phone_id':phone_id})
    )

    print("Response from lambda")
    print(response)    
          

def build_response(status_code, json_content):
        return {
        'statusCode': status_code,
        "headers": {
            "Content-Type": "text/html;charset=UTF-8",
            "charset": "UTF-8",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json_content
    }

def validate_healthcheck(event, WHATS_VERIFICATION_TOKEN ):
    if('queryStringParameters' in event and 'hub.challenge' in event['queryStringParameters']):
        print(event['queryStringParameters'])
        print("Token challenge")
        if(event['queryStringParameters']['hub.verify_token'] == WHATS_VERIFICATION_TOKEN):
            print("Token verified")
            print(event['queryStringParameters']['hub.challenge'])
            response = event['queryStringParameters']['hub.challenge']
        else:
            response = ''
    else:
        print("Not challenge related")
        response = '<html><head></head><body> No key, no fun!</body></html>'
    return response