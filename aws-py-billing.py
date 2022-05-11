#!/usr/bin/env python3

# Programa para listar o tipo de intancias em uma conta
#
#  Voce passa o profile da conta (-p) e ele vai coletar:
#
#  -- Conta, Regiao, ID da instancia, Tipo da instancia, Lifecycle, Plataforma, Hostname e Status


import boto3
import os
import argparse
import sys
from error_handler import exception


@exception
def list_billing(region, get_profile):
 session = boto3.session.Session(profile_name = str(gprofile), region_name = region)
 conn=session.client('ce')
 
 response = conn.get_cost_and_usage(
  TimePeriod={
   'Start': start_date,
   'End': end_date
  },
  Granularity='MONTHLY',
   Metrics=[
    'AmortizedCost'
   ]
 )
    
 return {
  'start': response['ResultsByTime'][0]['TimePeriod']['Start'],
  'end': response['ResultsByTime'][0]['TimePeriod']['End'],
  'billing': response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'],
 }


 #print(
 # f" \
 # {get_profile}, \
 # {region}, \
 # {i['InstanceId']},\
 # {i['InstanceType']},\
 # {instancelifecycle},\
 # {platform},\
 # {t['Value']},\
 # {i['State']['Name']},\
 # {ptag}"
 #)
 
# return

@exception
def get_regions():
 session = boto3.session.Session(profile_name = str(gprofile))
 print("account","region","instanceid","instancetype","lifecycle","platform","hostname","state","tags",sep=",")
 client = session.client('ce')
 regions = client.describe_regions()
 
 for i in regions['Regions']:
  list_billing(i['RegionName'], gprofile)


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
