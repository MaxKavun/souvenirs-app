import boto3
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Class with CRUD methods for Artifacts table.
class Artifacts():
    def __init__(self):
        self.table = dynamodb.Table('artifacts')
    # Create DynamoDB table
    def createTable(self):
        table = dynamodb.create_table(
            TableName = 'artifacts',
            KeySchema=[
                {
                    'AttributeName': 'Type',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Type',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='artifacts')
        return "Table was created"

    # Add new item to DynamoDB table
    def addItem(self,type,name):
        self.table.put_item(
            Item={
                'Type': type,
                'Name': name
            }
        )
    
    # Getting an item from table
    def getItem(self,type,name):
        '''
        response = self.table.query(
            KeyConditionExpression=Key('Type').eq(type)
        )
        items = response['Items']
        return items
        '''
        response = self.table.get_item(
            Key={
                'Type': type,
                'Name': name
            }
        )
        item = response.get('Item')
        return item

    def updateItem(self,type,name):
        self.table.update_item(
            Key={
                'Type': type,
                'Name': name
            },
            UpdateExpression='SET age = :val1',
            ExpressionAttributeValues={
                ':val1' : 24
            }
        )

    # Remove item from DynamoDB table
    def removeItem(self,type,name):
        self.table.delete_item(
            Key={
                'Type': type,
                'Name': name
            }
        )

    # Delete table from DynamoDB
    def deleteTable(self):
        self.table.delete()
        return "Table was deleted"