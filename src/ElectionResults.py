import json
import boto3
import os

electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def putCalculateResults(event, context):
    print(json.dumps(event))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),

      
    }


def getNationwideResults(event, context):
    print(json.dumps(event))

    # Get the input
    path = event["path"] # "/results/xxx/yyy"
    array_path = path.split("/") # ["", "results","xxx","yyy"]
    object_type = array_path[2]
    object_id = array_path[3] 
    
    #make info
    pk = "results_" + object_type

    #serach info
    response = table.get_item(
        Key={
            'pk':pk,
            'sk': object_id
        } 
    )
    item = response['Item']
    YES = item["YES"]
    NO  = item["NO"]
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'YES':YES,
        'NO':NO
      
    }
    
def getCityResults(event, context):
    print(json.dumps(event))

    # Get the input
    path = event["path"] # "/results/xxx/yyy"
    array_path = path.split("/") # ["", "results","xxx","yyy"]
    object_type = array_path[2]
    object_id = array_path[3] 
    
    #make info
    pk = "results_" + object_type

    #serach info
    response = table.get_item(
        Key={
            'pk':pk,
            'sk': object_id
        } 
    )
    item = response['Item']
    YES = item["YES"]
    NO  = item["NO"]
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'YES':YES,
        'NO':NO
      
    }
    
def getSchoolResults(event, context):
    print(json.dumps(event))

    # Get the input
    path = event["path"] # "/results/xxx/yyy"
    array_path = path.split("/") # ["", "results","xxx","yyy"]
    object_type = array_path[2]
    object_id = array_path[3] 
    
    #make info
    pk = "results_" + object_type

    #serach info
    response = table.get_item(
        Key={
            'pk':pk,
            'sk': object_id
        } 
    )
    item = response['Item']
    YES = item["YES"]
    NO  = item["NO"]
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'YES':YES,
        'NO':NO
      
    }
    
def getPersonPlace(event, context):
    print(json.dumps(event))

    # Get the input
    path = event["path"] # "/results/xxx/yyy"
    array_path = path.split("/") # ["", "results","xxx","yyy"]
    object_type = array_path[2]
    object_id = array_path[3] 
    
    #make info
    pk = "results_" + object_type

    #serach info
    response = table.get_item(
        Key={
            'pk':pk,
            'sk': object_id
        } 
    )
    item = response['Item']
    YES = item["YES"]
    NO  = item["NO"]
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'YES':YES,
        'NO':NO
      
    }