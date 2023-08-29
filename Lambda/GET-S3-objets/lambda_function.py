import base64
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event["pathParameters"]["bucket"]
    file_name = event["queryStringParameters"]["file"]

    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response["Body"].read()

    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')

    headers = {
        "Content-Type": "application/jpg",
        "Content-Disposition": "attachment; filename={}".format(file_name)
    }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": base64_encoded_content,
        "isBase64Encoded": True
    }
