#!/usr/bin/env python3

#programa para listar o tipo de intancias em uma conta
# precise que voce passe o nome do profile da conta

import boto3
import os
import argparse
import sys
from error_handler import exception

@exception
def list_region(region, get_profile):
 session = boto3.session.Session(profile_name = str(gprofile), region_name = region)
 conn=session.client('ec2')
 
 response = conn.describe_instances()
 
 for r in response['Reservations']:
  for i in r['Instances']:
   if "InstanceLifecycle" in i and "Platform" in i:
    instancelifecycle = i['InstanceLifecycle']
    platform = i['Platform']
   elif "Platform" in i:
    instancelifecycle = "ondemand"
    platform = i['Platform']
   elif "InstanceLifecycle" in i:
    instancelifecycle = i['InstanceLifecycle']
    platform = "linux/unix"
   else:
    instancelifecycle = "ondemand"
    platform = "linux/unix"
   
   if "Tags" in i:
    for t in i['Tags']:
     if t['Key'] == 'Name':
      print(f"{get_profile},{region},{i['InstanceId']},{i['InstanceType']},{instancelifecycle},{platform},{t['Value']},{i['State']['Name']}")
   else: 
    print(f"{get_profile},{region},{i['InstanceId']},{i['InstanceType']},{instancelifecycle},{platform},Sem Hostname,{i['State']['Name']}")
 
 return

@exception
def get_regions():
   session = boto3.session.Session(profile_name = str(gprofile))
   #ROADMAP - Passar isso para uma funcao
   print("account","region","instanceid","instancetype","lifecycle","platform","hostname","state",sep=",")
   client = session.client('ec2')
   regions = client.describe_regions()
   
   for i in regions['Regions']:
      list_region(i['RegionName'], gprofile)


#==============================================================================
# ---- Inicio do programa
#==============================================================================

if __name__ == '__main__':

   try:
      #Limpa a tela
      #os.system('cls' if os.name == 'nt' else 'clear')

      #ArgParse
      parser = argparse.ArgumentParser(
                        description = 'Modulo para coleta de informacoes em instancias EC2',
                        prog ='Jarvis do Sagara',
                        epilog = 'Contato: thiagosagara@gmail.com\n')

      parser.add_argument('-f','--file', action='store',
                        dest='gfile',default = 'notdefined',
                        required = False,
                        help = 'Digite o nome do arquivo onde estão os profiles')

      parser.add_argument('-p','--profile', action='store',
                        dest='gprofile',default = 'Sandbox',
                        required = True,
                        help = 'Digite o nome do profile (~/.aws/credentials)')
                        
      parser.add_argument('-d','--debug', action='store', type=int,
                        dest='pshow', default = 0,
                        required = False,
                        help = 'adicione -d 1 para mostrar em modo debug')

      #Instancia das opcoes

      gfile=parser.parse_args().gfile
      gprofile=parser.parse_args().gprofile
      pshow=parser.parse_args().pshow

      # --------------- Processo em caso de arquivo com os ICs ------------
      # Valida se foi passado o argumento de arquivo
      if gfile != "notdefined":
         quit("Feature em desenvolvimento")
      else:
         get_regions()
   except KeyboardInterrupt:
      print("Finalizando o script a pedido do user...")
      sys.exit(0)