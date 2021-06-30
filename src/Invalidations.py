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
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'
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
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'
                }
            }
        ]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def showInvalidBooths(event, context):
    cities = table.query(
        KeyConditionExpression = Key('pk').eq('CityReg')
    )
    
    invalid_booths = []
    for eachcity in cities['Items']:
        pkQuery = f"Inv_{eachcity['id']}"
        invalids = table.query(
            KeyConditionExpression = Key('pk').eq(pkQuery)
        )
        invalid_booths.extend(invalids['Items'])
        
    booths_info = []
    for eachbooth in invalid_booths:
        info = table.get_item(
            Key = {
                'pk': 'Sch_' + eachbooth['school'],
                'sk': eachbooth['sk']
            }
        )
        item = {
            "booth_id": info['Item']['sk'],
            "school_id": eachbooth['school'],
            "registered": str(info['Item']['registered']),
            "missing": str(info['Item']['missing']),
            "voted": str(info['Item']['voted'])
        }
        booths_info.append(item)
    
    return {
        'statusCode': 200,
        'body': json.dumps(booths_info)
    }
    
def showInvalidBoothsByCity(event, context):
    cities = table.query(
        KeyConditionExpression = Key('pk').eq('CityReg')
    )
    
    cities_items= cities['Items']
    
    city_invalids = []
    for eachcity in cities_items:
        pkQuery = 'Inv_' + eachcity['id']
        invalids = table.query(
            KeyConditionExpression = Key('pk').eq(pkQuery)
        )
        item={
            "city_id": eachcity['id'],
            "city_name": eachcity['sk'],
            "invalids_count": str(invalids['Count'])
        }
        city_invalids.append(item)
    
    city_invalids.sort(reverse=True, key=criteria)
    
    print(json.dumps(city_invalids))
    return {
        'statusCode': 200,
        'body': json.dumps(city_invalids)
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
    
    school_invalids = []
    for eachschool in schools['Items']:
        pkQuery = f"Inv_{city_id}"
        school_id = eachschool['sk']
        invalids = table.query(
            KeyConditionExpression = Key('pk').eq(pkQuery),
            FilterExpression = "school = :sch",
            ExpressionAttributeValues={
                ':sch': school_id
            }
        )
        
        item={
            "school_id": eachschool['sk'],
            "city_id": city_id,
            "invalids_count": str(invalids['Count'])
        }
        school_invalids.append(item)
        
    school_invalids.sort(reverse=True, key=criteria)
    
    print(json.dumps(school_invalids))
    return {
        'statusCode': 200,
        'body': json.dumps(school_invalids)
    }
    
def criteria(e):
    return Decimal(e["invalids_count"])