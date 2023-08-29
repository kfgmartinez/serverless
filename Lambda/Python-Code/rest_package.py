import boto3
import logging
import json
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = "dogbar-customers"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodbTableName)


def getCustomer(customer_id):
    try:
        response = table.get_item(
            Key={"customer_id": customer_id}
        )
        if "Item" in response:
            return buildResponse(200, response["Item"])
        else:
            return buildResponse(404, {"Message": "customer_id: {0}s not found".format(customer_id)})
    except:
        logger.exception("Error occured while retrieving a customer")


def getCustomers():
    try:
        response = table.scan()
        result = response["Items"]

        while "LastEvaluateKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])

        body = {
            "customer": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Error occured while retrieving all customers ")


def saveCustomer(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS",
            "Item": requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception("Error occured while posting your data")


def modifyCustomer(customer_id, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                "customer_id": customer_id
            },

            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ":value": updateValue
            },
            ReturnValues="UPDATED_NEW"
        )
        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdatedAttributes": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Error occured while modifying your data")

def deleteCustomer(customer_id):
    try:
        response = table.delete_item(  # boto3 module
            Key={
                "customer_id": customer_id
            },
            ReturnValues="ALL_OLD"
        )
        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "deletedItem": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Error occured while deleting your data")


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            'Access-Control-Allow-Headers': "Content-Type",
            'Access-Control-Allow-Methods': "OPTIONS, POST, PATCH, DELETE, PUT"  # Add the allowed HTTP methods
        }
    }
    if body is not None:
        response["body"] = json.dumps(body, cls=CustomEncoder)
    return response