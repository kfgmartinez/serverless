import boto3
import json
import logging

from rest_package import getCustomer
from rest_package import getCustomers
from rest_package import saveCustomer
from rest_package import modifyCustomer
from rest_package import deleteCustomer
from rest_package import buildResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    logger.info(event)
    print(event)
    http_Method=event["httpMethod"]
    path = event["path"]
    if http_Method == "GET" and path == healthPath:
        response = buildResponse(200)
    elif http_Method == "GET" and path == "/customer":
        response = getCustomer(event["queryStringParameters"]["customer_id"])
    elif http_Method == "GET" and path == "/customers":
        response = getCustomers()
    elif http_Method == "POST" and path == "/customer":
        response = saveCustomer(json.loads(event["body"]))
    elif http_Method == "PATCH" and path == "/customer":
        requestBody = json.loads(event["body"])
        response = modifyCustomer(requestBody["customer_id"], requestBody["updateKey"], requestBody["updateValue"])
    elif http_Method == "DELETE" and path == "/customer":
        requestBody = json.loads(event["body"])
        response = deleteCustomer(requestBody["customer_id"])
    else:
        response = buildResponse(404, "Not Found")
    return response

