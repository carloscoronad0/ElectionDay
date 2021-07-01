import json
import boto3
import os
import pandas as pd
import dynamodb_json as dynamodb_json

from boto3.dynamodb.conditions import Key, Attr
electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def putCalculateResults(event, context):
    response = table.scan(
        FilterExpression=Attr('pk').begins_with('Sch_')
    )
    data = response['Items']
    df  = pd.DataFrame(json.loads(data))
    # Conteo por mesa
    mesa = df.groupby('nombre-columna-mesa').sum().reset_index()
    mesa['total'] = mesa['voto_si'] + mesa['voto_si']
    save_to_db(mesa, 'mesa', table)
    
    # Conteo por colegio
    school = df.groupby('pk').sum().reset_index()
    school['total'] = school['voto_si'] + school['voto_si']
    save_to_db(school, 'school', table)
    
    # Conteo por ciudad
    city = df.groupby('city').sum().reset_index()
    city['total'] = city['voto_si'] + city['voto_si']
    save_to_db(city, 'city', table)
    return {
        'statusCode': 200,
        'body': json.dumps('votes counted')
      
    }
    
    
def save_to_db(df, index_name, table):
    """ Save panda data frame to dynamo db"""
    for item in df.to_dict(orient='records'):
        result_name = 'result_' + index_name
        table.put_item(
            Item={
                'pk': result_name,
                'sk': item[index_name],
                'yes': item['yes'],
                'no': item['no']
            }
        )


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
    path = event["path"] # "/persons/{person_id}/verify"
    array_path = path.split("/") # ["", "person","xxx","verify"]
    person_id = array_path[2]
    pk = person_id
    response = table.get_item(
        Key={
            'pk':pk,
            'sk':pk
        } 
    )
    item = response['Item']
    
    place = (item["school"])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'place':place,

      
    }