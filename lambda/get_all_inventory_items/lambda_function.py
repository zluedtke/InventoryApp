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
    # Initialize a DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Scan the table
    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        items = convert_decimals(items)
        
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
