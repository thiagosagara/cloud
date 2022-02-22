#!/usr/bin/env python3

#programa para listar o tipo de intancias em uma conta
# precise que voce passe o nome do profile da conta

import boto3
from botocore.config import Config
import os


profile = str(input("Digite o profile: "))
os.system('cls' if os.name == 'nt' else 'clear')

session = boto3.session.Session(profile_name = profile)
client = session.client('ec2')

regions = client.describe_regions()
print("account","region","instanceid","instancetype","hostname",sep=",")

def list_region(region, get_profile):
 mc=Config( region_name = region )
 conn=boto3.client('ec2', config=mc)
 
 response = conn.describe_instances()
 
 for r in response['Reservations']:
  for i in r['Instances']:
   if "KeyName" in i:
    print(f"{profile},{region},{i['InstanceId']},{i['InstanceType']},{i['KeyName']}")
   else:
    print(f"{profile},{region},{i['InstanceId']},{i['InstanceType']},Sem Hostname")

for i in regions['Regions']:
 list_region(i['RegionName'], profile)
