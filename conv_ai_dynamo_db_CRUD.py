import json
import boto3

dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table('conv_ai_hotel_booking_table')


def lambda_handler(event, context):
    print(json.dumps(event))

    item = event.get("item")

    if event.get('operation') == 'create':
        table.put_item(
            Item=item
        )

    if event.get('operation') == 'read':
        item = table.get_item(
            Key={
                'reservationId': item.get('reservationId')
            },
        ).get("Item")

    if event.get('operation') == 'delete':
        table.delete_item(
            Key={
                'reservationId': item.get('reservationId')
            },
        )

    if event.get('operation') == 'update':
        reservationId = item.get('reservationId')
        del item['reservationId']
        table.update_item(
            Key={
                'reservationId': reservationId
            },
            AttributeUpdates={
                "city": {
                    "Value": item.get('city'),
                    "Action": "PUT"
                }
            }
        )

    return item