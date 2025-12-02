import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Inventory')

    # Extract the '_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = str(event['pathParameters']['id'])


    # Attempt to delete the item from the table
    try:
        response = table.query(
            KeyConditionExpression=Key('_id').eq(key_value)
        )

        items = response.get('Items', [])
        
        for item in items:
            table.delete_item(
                Key={
                    '_id': item['_id'],
                    'location_id': item['location_id'] 
                }
            )
            
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {key_value} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
