import json
import boto3
import os

electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def registerparticipant(event, context):
    
    path = event["path"]    
    array_path = path.split("/")
    person_id = array_path[-2]
    body_temp = event["body"]
    body = json.loads(body_temp)
    
    if body["vote"] == "yes":
        y = 1
        n = 0
    else: 
        y = 0
        n = 1
        
    table.put_item(
       Item={
            'pk':person_id,
            'sk':body["time"],
            'school':body["school"] ,
            'booth':body["booth"],
            'city':body["city"],
            'name':body["name"],
            'lastname':body["lastname"],
            'vote':body["vote"]
        }
    )
    
    table.update_item(
        Key={
            'pk':'Sch_' + body["school"],
            'sk':body["booth"]
        },
        UpdateExpression='SET #g= #g-:val1, #h= #h+:val1, #i= #i+:val2, #j= #j+:val3',
        ExpressionAttributeNames={
            "#g": "missing",
            "#h": "voted",
            "#i": "yes",
            "#j": "no"
        },
        ExpressionAttributeValues={
            ':val1': 1, 
            ':val2': y,
            ':val3': n
        }
    )
    table.update_item(
        Key={
            'pk':'Av_' + body["city"],
            'sk':body["school"]
        },
        UpdateExpression='SET #g= #g-:a, #h= #h+:a, #i= #i+:b, #j= #j+:c',
        ExpressionAttributeNames={
            "#g": "missing",
            "#h": "voted",
            "#i": "yes",
            "#j": "no"
        },
        ExpressionAttributeValues={
            ':a': 1, 
            ':b': y,
            ':c': n
        }
    )
    table.update_item(
        Key={
            'pk':'Nat_wide',
            'sk':"Bolivia"
        },
        UpdateExpression='SET #g= #g-:d, #h= #h+:d, #i= #i+:e, #j= #j+:f',
        ExpressionAttributeNames={
            "#g": "missing",
            "#h": "voted",
            "#i": "yes",
            "#j": "no"
        },
        ExpressionAttributeValues={
            ':d': 1, 
            ':e': y,
            ':f': n
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Votante registrado correctamente.'
    }