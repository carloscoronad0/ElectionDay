import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

electionDay_table = os.environ['ELECTIONDAY_TABLE']

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def invalidateBooth(event, context):
    path = event["path"]
    array_path = path.split("/")
    booth_id = array_path[-2]
    
    body_temp = event["body"]
    body = json.loads(body_temp)
    
    invalid_booth = table.get_item(
        Key = {
            'pk': 'Sch_' + body['school_id'],
            'sk': booth_id
        }
    )
    
    newPkPut = 'Inv_' + body['city_id']
    newPkUpdate = 'Av_' + body['city_id']
    school = body['school_id']
    
    val = str(invalid_booth['Item']['missing'])
    
    response = client.transact_write_items(
        TransactItems=[
            {
                'Put': {
                    'TableName': 'election-day-table',
                    'Item': {
                        'pk': { 'S': newPkPut },
                        'sk': { 'S': booth_id },
                        'school': { 'S': school }
                    }
                }
            },
            {
                'Update': {
                    'TableName': 'election-day-table',
                    'Key': {
                        'pk': { 'S': newPkUpdate },
                        'sk': { 'S': school }
                    },
                    'UpdateExpression': 'SET #miss = #miss - :val',
                    'ExpressionAttributeNames': {
                        '#miss': 'missing'
                    },
                    'ExpressionAttributeValues': {
                      ':val': { 'N': val }
                    }
                }
            }
        ]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Invalidated booth {booth_id}")
    }
    
def showInvalidBooths(event, context):
    cities = table.query(
        KeyConditionExpression = Key('pk').eq('CityReg')
    )
    
    cities_items= cities['Items']
    
    invalids = []
    for eachcity in cities_items:
        aux = 'Inv_' + eachcity['id']
        temp = table.query(
            KeyConditionExpression = Key('pk').eq(aux)
        )
        invalids.extend(temp['Items'])
        
    booths = []
    for eachbooth in invalids:
        temp = table.get_item(
            Key = {
                'pk': 'Sch_' + eachbooth['school'],
                'sk': eachbooth['sk']
            }
        )
        item = {
            "booth_id": temp['Item']['sk'],
            "registered": str(temp['Item']['registered']),
            "missing": str(temp['Item']['missing']),
            "voted": str(temp['Item']['voted'])
        }
        booths.append(item)
    
    return {
        'statusCode': 200,
        'body': json.dumps(booths)
    }
    
def showInvalidBoothsByCity(event, context):
    cities = table.query(
        KeyConditionExpression = Key('pk').eq('CityReg')
    )
    
    cities_items= cities['Items']
    
    invalids = []
    for eachcity in cities_items:
        aux = 'Inv_' + eachcity['id']
        temp = table.query(
            KeyConditionExpression = Key('pk').eq(aux)
        )
        item={
            "city_id": eachcity['id'],
            "city_name": eachcity['sk'],
            "invalids_count": str(temp['Count'])
        }
        invalids.append(item)
    
    invalids.sort(reverse=True, key=criteria)
    
    print(json.dumps(invalids))
    return {
        'statusCode': 200,
        'body': json.dumps(invalids)
    }
    
def showInvalidBoothsBySchool(event, context):
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    city_id = array_path[-2]
    
    aux = f"Av_{city_id}"
    schools = table.query(
        KeyConditionExpression = Key('pk').eq(aux)
    )
    
    invalids = []
    for eachschool in schools['Items']:
        invCity = f"Inv_{city_id}"
        temp = eachschool['sk']
        booths = table.query(
            KeyConditionExpression = Key('pk').eq(invCity),
            FilterExpression = "school = :sch",
            ExpressionAttributeValues={
                ':sch': temp
            }
        )
        
        item={
            "school_id": eachschool['sk'],
            "city_id": city_id,
            "invalids_count": str(temp['Count'])
        }
        invalids.append(item)
        
    invalids.sort(reverse=True, key=criteria)
    
    print(json.dumps(invalids))
    return {
        'statusCode': 200,
        'body': json.dumps(invalids)
    }
    
def criteria(e):
    return Decimal(e["invalids_count"])