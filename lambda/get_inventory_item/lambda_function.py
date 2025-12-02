import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def lambda_handler(event, context):
    table = dynamodb.Table('Inventory')

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']

    # Get the item from the table
    try:
        response = table.query(
            KeyConditionExpression=Key('_id').eq(key_value)
        )

        items = response.get('Items', [])


        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
        
        items = convert_decimal(items)
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))

        }



    return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
