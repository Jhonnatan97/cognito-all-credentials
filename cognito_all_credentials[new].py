import csv
import boto3
import time
from datetime import datetime

# from file_handler import FileHandler
session = boto3.Session(profile_name='your_profile')
cognito = session.client("cognito-idp", region_name='us-east-1')
userpoolid = '<YOUR USERPOOLID>'
clients = []
row_list = []

with open('secret_id - secret.csv', 'r') as csvfile:
    readit = csv.reader(csvfile, delimiter=' ', quotechar='|')

    dataHora = datetime.now ()
    dataHora = dataHora.strftime ('%H%M')
    geradoSucesso = open (dataHora + 'cognito.csv', 'w')
    geradoSucesso.write ("client_name,client_id,scopo\n") #client_name, client_id, scopo

count2 = 0
cognito_response = cognito.list_user_pool_clients(UserPoolId=userpoolid)
pool_list = []

if count2 == 0:
    count2 +=1
    for response in cognito_response["UserPoolClients"]:
        pool_list.append(response)

while 'NextToken' in cognito_response:
    completou = False
    retries = 0
    max_retries = 10
    while not completou and retries<=max_retries:
        try:
            cognito_response = cognito.list_user_pool_clients (UserPoolId=userpoolid,
                                                               NextToken=cognito_response["NextToken"])
            completou = True
        except:
            time.sleep(5)
            completou = False
            retries += 1
    for response in cognito_response["UserPoolClients"]:
        pool_list.append(response)

count = 1
# print(len(pool_list))
for pool in pool_list:
    client = 'ClientId:', pool['ClientId']
    secret = 'ClientName:', pool['ClientName']

    completou = False
    retries = 0
    max_retries = 10
    response = {}
    while not completou and retries<=max_retries:
        try:
            response = cognito.describe_user_pool_client (
                UserPoolId=userpoolid,
                ClientId=pool['ClientId']
            )['UserPoolClient']

            completou = True
        except:
            completou = False
            retries += 1
    scopes = {}
    if 'AllowedOAuthScopes' in response:
        scopes = response['AllowedOAuthScopes']
        client_name = response['ClientName']
        client_id = response['ClientId']
        scopo = scopes
        print(client_name)

        geradoSucesso.write ("{},{},{}\n".format (client_name, client_id,scopo))

    else:
        client_nome = pool['ClientName']
        client_id2 = pool['ClientId']
        scopo2 = 'sem escopo associado'

        geradoSucesso.write ("{},{},{}\n".format (client_nome, client_id2,scopo2))
        print(pool['ClientName'], 'sem escopo associado')

   
    count +=1
    print(count)