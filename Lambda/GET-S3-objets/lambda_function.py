import base64
import boto3


s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event ["pathParameters"]["bucket"]
    file_name = event ["queryStringParameters"]["file"]
    fileObj = s3.get_object(Bucket=bucket_name, Key=file_name) #boto3 module
    file_content = fileObj["Body"].read()
    # print
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/jpg",
            "Content-Disposition": f"attachment; filename={file_name}"
        },
        "body": base64.b64encode(file_content), #encode the response with base64
        "isBase64Encoded": True
    }
