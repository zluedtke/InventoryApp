import boto3
import json
from decimal import Decimal


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Scan the table
    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        items = convert_decimal(items)
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))

        }
        
    return {
            'statusCode': 200,
            'body': json.dumps(items)  # Use str to handle any special types like Decimal
        }
