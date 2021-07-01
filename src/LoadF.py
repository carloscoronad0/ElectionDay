import boto3
import csv
import os

bucketName = os.environ['ELECTIONDAY_BUCKET']
electionDay_table = os.environ['ELECTIONDAY_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(electionDay_table)

def loadData(event, context):
    recList=[]
    s3=boto3.client('s3')            
    confile= s3.get_object(Bucket=bucketName, Key='election-day-table.csv')
    recList = confile['Body'].read().split('\n')
    firstrecord=True
    csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
    for row in csv_reader:
        if (firstrecord):
            firstrecord=False
            continue
        empid = row[0]
        name = row[1].replace(',','').replace('$','') if row[1] else '-'
        salary = row[2].replace(',','').replace('$','') if row[2] else 0
        response = table.put_item(
            Item={
            'empid' : {'N':str(empid)},
            'name': {'S':name},
            'salary': {'N':str(salary)},
            'parttime': {'BOOL':False},
            }
        )