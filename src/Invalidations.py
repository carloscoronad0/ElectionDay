import json
import boto3
import os

electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def invalidateBooth(event, context):
    print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps("InvalidateBooth")
    }
    
def showInvalidBooths(event, context):
    print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps("ShowInvalidBooths")
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