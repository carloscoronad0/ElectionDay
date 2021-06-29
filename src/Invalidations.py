import json
import boto3
import os
from boto3.dynamodb.conditions import Key

electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def invalidateBooth(event, context):
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    booth_id = array_path[-2]
    
    body = event["body"]
    body_object = json.loads(body)
    
    table.put_item(
       Item = {
            'pk': 'Inv_' + body_object['city_id'],
            'sk': booth_id,
            'school': body_object['school_id']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Invalidated booth {booth_id}")
    }
    
def showInvalidBooths(event, context):
    print(json.dumps(event))
    
    cities = table.query(
        KeyConditionExpression = Key('pk').eq('CityReg')
    )
    
    cities_items= cities['Items']
    print(json.dumps(cities_items))
    
    booths = []
    
    for eachcity in cities_items:
        aux = 'Inv_' + eachcity['id']
        temp = table.query(
            KeyConditionExpression = Key('pk').eq(aux)
        )
        booths.extend(temp['Items'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(booths)
    }
    
def showInvalidBoothsByCity(event, context):
    print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps("ShowInvalidBoothsByCity")
    }
    
def showInvalidBoothsBySchool(event, context):
    print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps("ShowInvalidBoothsBySchool")
    }