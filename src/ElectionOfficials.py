import json
import boto3
import os

electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def officialbooth(event, context):
    
    path = event["path"]    
    array_path = path.split("/")
    person_id = array_path[-2]
    body_temp = event["body"]
    body = json.loads(body_temp)
    
    
    table.put_item(
        Item={
            'pk':'Official_' + body["school"],
            'sk':body["booth"],
            'city':body["city"],
            'missing':body["missing"],
            'link':body['link'],
            'voted':body["voted"],
            'yes':body["yes"],
            'no':body["no"]
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Votante registrado correctamente.'
    }