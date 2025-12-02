import boto3
import json


# Function to convert Decimal to int/float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    return obj

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']

    # Prepare the key for DynamoDB
    key = {
        'id': {'S': key_value}
    }

    # Get the item from the table
    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
        items = convert_decimals(items)
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))

        }



    return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
